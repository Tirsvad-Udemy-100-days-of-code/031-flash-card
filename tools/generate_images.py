"""Generate the PNG assets of the flash card program.

@file generate_images.py
@brief Draws card_front, card_back, right and wrong as antialiased RGBA PNGs.
Uses the standard library only; run it to regenerate the assets.
"""

import argparse
import math
import struct
import sys
import zlib
from collections.abc import Callable, Sequence
from pathlib import Path

_SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from flash_card.constants import (  # noqa: E402
    ASSETS_DIR,
    CARD_BACK_IMAGE_NAME,
    CARD_FRONT_IMAGE_NAME,
    CARD_HEIGHT,
    CARD_WIDTH,
    RIGHT_IMAGE_NAME,
    WRONG_IMAGE_NAME,
)

Color = tuple[int, int, int]
Point = tuple[float, float]
Segment = tuple[Point, Point]
Box = tuple[float, float, float, float]
Span = tuple[float, float] | None

_SUPERSAMPLE = 4
_CARD_RADIUS = 60
_CARD_INSET = 2
_SHADOW_OFFSET = 10
_SHADOW_BLUR = 5
_SHADOW_COLOR: Color = (70, 70, 70)
_SHADOW_OPACITY = 0.4
_CARD_FRONT_COLOR: Color = (255, 255, 255)
_CARD_BACK_COLOR: Color = (0x91, 0xC2, 0xAF)
_BUTTON_SIZE = 100
_BUTTON_RADIUS = 28
_STROKE_WIDTH = 11.0
_WHITE: Color = (255, 255, 255)
_RIGHT_GRADIENT: tuple[Color, Color] = ((0xA5, 0xE0, 0x60), (0x2F, 0xBF, 0x71))
_WRONG_GRADIENT: tuple[Color, Color] = ((0xFF, 0x6B, 0x8B), (0xD9, 0x5A, 0x55))
_CHECK_SEGMENTS: tuple[Segment, ...] = (
    ((27.0, 52.0), (43.0, 68.0)),
    ((43.0, 68.0), (74.0, 33.0)),
)
_CROSS_SEGMENTS: tuple[Segment, ...] = (
    ((32.0, 32.0), (68.0, 68.0)),
    ((68.0, 32.0), (32.0, 68.0)),
)
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class _Canvas:
    """Premultiplied float RGBA canvas that shapes are composited onto."""

    def __init__(self, width: int, height: int) -> None:
        """Create a fully transparent canvas.

        @param width Width in pixels.
        @param height Height in pixels.
        """
        self.width = width
        self.height = height
        size = width * height
        self.red = [0.0] * size
        self.green = [0.0] * size
        self.blue = [0.0] * size
        self.alpha = [0.0] * size

    def paint(
        self,
        mask: list[float],
        color_at: Callable[[int], Color],
        opacity: float = 1.0,
    ) -> None:
        """Composite a coverage mask over the canvas.

        @param mask Coverage per pixel in 0..1, row-major.
        @param color_at Colour for a pixel row index.
        @param opacity Extra opacity applied to the whole mask.
        """
        for y in range(self.height):
            r, g, b = color_at(y)
            for i in range(y * self.width, (y + 1) * self.width):
                a = min(1.0, mask[i]) * opacity
                if a <= 0.0:
                    continue
                keep = 1.0 - a
                self.red[i] = r * a + self.red[i] * keep
                self.green[i] = g * a + self.green[i] * keep
                self.blue[i] = b * a + self.blue[i] * keep
                self.alpha[i] = a + self.alpha[i] * keep

    def to_rgba_bytes(self) -> bytes:
        """Return the pixels as straight-alpha 8-bit RGBA rows.

        @return The raw RGBA bytes, row-major.
        """
        out = bytearray()
        pixels = zip(self.red, self.green, self.blue, self.alpha, strict=True)
        for r, g, b, a in pixels:
            if a <= 0.0:
                out += b"\x00\x00\x00\x00"
                continue
            out.append(min(255, round(r / a)))
            out.append(min(255, round(g / a)))
            out.append(min(255, round(b / a)))
            out.append(min(255, round(a * 255)))
        return bytes(out)


def _rounded_rect_span(box: Box, radius: float, y: float) -> Span:
    """Return the horizontal extent of a rounded rectangle at height y.

    @param box Left, top, right, bottom of the rectangle.
    @param radius Corner radius.
    @param y Vertical sample position.
    @return The (start, end) x range, or None when y is outside.
    """
    left, top, right, bottom = box
    if y < top or y > bottom:
        return None
    if y < top + radius:
        centre_y = top + radius
    elif y > bottom - radius:
        centre_y = bottom - radius
    else:
        return (left, right)
    inset = radius - math.sqrt(max(0.0, radius * radius - (centre_y - y) ** 2))
    return (left + inset, right - inset)


def _rounded_rect_mask(width: int, height: int, box: Box, radius: float) -> list[float]:
    """Rasterise a rounded rectangle with 4x vertical supersampling.

    Horizontal coverage of each sub-row is computed exactly.

    @param width Mask width.
    @param height Mask height.
    @param box Left, top, right, bottom of the rectangle.
    @param radius Corner radius.
    @return Coverage per pixel in 0..1.
    """
    mask = [0.0] * (width * height)
    weight = 1.0 / _SUPERSAMPLE
    for py in range(height):
        base = py * width
        for sub in range(_SUPERSAMPLE):
            span = _rounded_rect_span(box, radius, py + (sub + 0.5) * weight)
            if span is None:
                continue
            start = max(span[0], 0.0)
            end = min(span[1], float(width))
            for px in range(int(start), min(width, math.ceil(end))):
                overlap = min(end, px + 1.0) - max(start, float(px))
                mask[base + px] += overlap * weight
    return mask


def _distance_to_segment(px: float, py: float, segment: Segment) -> float:
    """Return the distance from a point to a line segment.

    @param px Point x.
    @param py Point y.
    @param segment Segment start and end.
    @return The Euclidean distance.
    """
    a, b = segment
    dx, dy = b[0] - a[0], b[1] - a[1]
    length_sq = dx * dx + dy * dy
    t = ((px - a[0]) * dx + (py - a[1]) * dy) / length_sq if length_sq else 0.0
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (a[0] + t * dx), py - (a[1] + t * dy))


def _stroke_mask(
    width: int, height: int, segments: Sequence[Segment], stroke_width: float
) -> list[float]:
    """Rasterise thick round-capped lines with 4x4 supersampling.

    @param width Mask width.
    @param height Mask height.
    @param segments Line segments.
    @param stroke_width Line thickness in pixels.
    @return Coverage per pixel in 0..1.
    """
    mask = [0.0] * (width * height)
    half = stroke_width / 2.0
    weight = 1.0 / (_SUPERSAMPLE * _SUPERSAMPLE)
    for segment in segments:
        a, b = segment
        x_min = max(0, int(min(a[0], b[0]) - half) - 1)
        x_max = min(width, math.ceil(max(a[0], b[0]) + half) + 1)
        y_min = max(0, int(min(a[1], b[1]) - half) - 1)
        y_max = min(height, math.ceil(max(a[1], b[1]) + half) + 1)
        for py in range(y_min, y_max):
            for px in range(x_min, x_max):
                hits = 0
                for sy in range(_SUPERSAMPLE):
                    for sx in range(_SUPERSAMPLE):
                        x = px + (sx + 0.5) / _SUPERSAMPLE
                        y = py + (sy + 0.5) / _SUPERSAMPLE
                        if _distance_to_segment(x, y, segment) <= half:
                            hits += 1
                index = py * width + px
                mask[index] = max(mask[index], hits * weight)
    return mask


def _box_blur(mask: list[float], width: int, height: int, radius: int) -> list[float]:
    """Blur a mask with a separable box filter.

    @param mask Coverage per pixel.
    @param width Mask width.
    @param height Mask height.
    @param radius Blur radius in pixels.
    @return The blurred mask.
    """
    window = 2 * radius + 1
    horizontal = [0.0] * len(mask)
    for y in range(height):
        row = mask[y * width : (y + 1) * width]
        total = sum(row[: radius + 1])
        for x in range(width):
            horizontal[y * width + x] = total / window
            if x + radius + 1 < width:
                total += row[x + radius + 1]
            if x - radius >= 0:
                total -= row[x - radius]
    result = [0.0] * len(mask)
    for x in range(width):
        column = horizontal[x::width]
        total = sum(column[: radius + 1])
        for y in range(height):
            result[y * width + x] = total / window
            if y + radius + 1 < height:
                total += column[y + radius + 1]
            if y - radius >= 0:
                total -= column[y - radius]
    return result


def _solid(color: Color) -> Callable[[int], Color]:
    """Return a colour function that always gives one colour.

    @param color The colour.
    @return A function from row index to colour.
    """
    return lambda _row: color


def _vertical_gradient(
    top: Color, bottom: Color, height: int
) -> Callable[[int], Color]:
    """Return a colour function for a top to bottom gradient.

    @param top Colour at the first row.
    @param bottom Colour at the last row.
    @param height Number of rows.
    @return A function from row index to colour.
    """

    def color_at(row: int) -> Color:
        t = (row + 0.5) / height
        r, g, b = (
            round(c0 + (c1 - c0) * t) for c0, c1 in zip(top, bottom, strict=True)
        )
        return (r, g, b)

    return color_at


def _render_card(fill: Color) -> _Canvas:
    """Draw a card with a soft drop shadow.

    @param fill Fill colour of the card.
    @return The canvas.
    """
    width, height = CARD_WIDTH, CARD_HEIGHT
    margin = _SHADOW_OFFSET + _SHADOW_BLUR + _CARD_INSET
    box: Box = (
        float(_CARD_INSET),
        float(_CARD_INSET),
        float(width - margin),
        float(height - margin),
    )
    shadow_box: Box = (
        box[0] + _SHADOW_OFFSET,
        box[1] + _SHADOW_OFFSET,
        box[2] + _SHADOW_OFFSET,
        box[3] + _SHADOW_OFFSET,
    )
    shadow = _rounded_rect_mask(width, height, shadow_box, _CARD_RADIUS)
    shadow = _box_blur(shadow, width, height, _SHADOW_BLUR)
    canvas = _Canvas(width, height)
    canvas.paint(shadow, _solid(_SHADOW_COLOR), _SHADOW_OPACITY)
    card = _rounded_rect_mask(width, height, box, _CARD_RADIUS)
    canvas.paint(card, _solid(fill))
    return canvas


def _render_button(
    gradient: tuple[Color, Color], segments: Sequence[Segment]
) -> _Canvas:
    """Draw a rounded gradient square with a white symbol.

    @param gradient Top and bottom colour.
    @param segments Line segments of the symbol.
    @return The canvas.
    """
    size = _BUTTON_SIZE
    canvas = _Canvas(size, size)
    box: Box = (0.0, 0.0, float(size), float(size))
    square = _rounded_rect_mask(size, size, box, _BUTTON_RADIUS)
    canvas.paint(square, _vertical_gradient(gradient[0], gradient[1], size))
    symbol = _stroke_mask(size, size, segments, _STROKE_WIDTH)
    canvas.paint(symbol, _solid(_WHITE))
    return canvas


def encode_png(width: int, height: int, rgba: bytes) -> bytes:
    """Encode raw RGBA pixels as a PNG file.

    @param width Image width.
    @param height Image height.
    @param rgba Row-major straight-alpha RGBA bytes.
    @return The PNG file content.
    """
    stride = width * 4
    raw = b"".join(b"\x00" + rgba[y * stride : (y + 1) * stride] for y in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (
        _PNG_SIGNATURE
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def generate_images(output_dir: Path) -> list[Path]:
    """Write the four PNG assets into a folder.

    @param output_dir Folder to write into; created when missing.
    @return The paths of the written files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    images = {
        CARD_FRONT_IMAGE_NAME: _render_card(_CARD_FRONT_COLOR),
        CARD_BACK_IMAGE_NAME: _render_card(_CARD_BACK_COLOR),
        RIGHT_IMAGE_NAME: _render_button(_RIGHT_GRADIENT, _CHECK_SEGMENTS),
        WRONG_IMAGE_NAME: _render_button(_WRONG_GRADIENT, _CROSS_SEGMENTS),
    }
    written: list[Path] = []
    for name, canvas in images.items():
        path = output_dir / name
        data = encode_png(canvas.width, canvas.height, canvas.to_rgba_bytes())
        path.write_bytes(data)
        written.append(path)
    return written


def main(argv: Sequence[str] | None = None) -> int:
    """Run the generator from the command line.

    @param argv Command line arguments, or None for sys.argv.
    @return The exit code, 0 on success.
    """
    parser = argparse.ArgumentParser(description="Generate the flash card images.")
    parser.add_argument(
        "--output-dir", type=Path, default=ASSETS_DIR, help="folder for the PNG files"
    )
    args = parser.parse_args(argv)
    for path in generate_images(args.output_dir):
        sys.stdout.write(f"wrote {path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
