# Pemasangan

🌐 [English](Install) · [Dansk](Install-da) · **Bahasa Malaysia**

## Keperluan

- Python 3.13 atau lebih baharu dengan Tkinter (pada Debian atau Ubuntu: `sudo apt install python3-tk`).
- `git`.
- Pilihan: sambungan internet dan tambahan `speech` jika anda mahu mendengar perkataan Melayu.

## Dapatkan kod

```bash
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card.git
cd 031-flash-card
```

## Cipta dan gunakan persekitaran maya setempat

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux dan macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

- `.[dev]` menambah `pytest`, `ruff`, `mypy` dan `import-linter`. Gunakan `.` jika anda hanya mahu menjalankan program.
- Jika PowerShell enggan menjalankan `Activate.ps1`, jalankan `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` sekali.
- Keluar daripada persekitaran dengan `deactivate`; padam folder `.venv` untuk bermula semula.

## Perkataan Melayu bersuara (pilihan)

```bash
python -m pip install -e ".[speech]"
```

Ini memasang `gTTS` dan `playsound==1.2.2`. Tanpa tambahan ini program berfungsi tanpa bunyi.

## Jalankan dan uji

```bash
python -m flash_card
python -m pytest
```

Ujian tetingkap dalam `tests/e2e/` dilangkau apabila tiada paparan.

## Bina fail boleh laku (Windows)

```powershell
python -m pip install -e ".[build,speech]"
python tools/build_executable.py
```

Skrip menggunakan PyInstaller dan menulis `dist/flash-card.exe`: satu fail tanpa tetingkap konsol, dengan imej, senarai perkataan dan suara di dalamnya. Klik dua kali untuk memulakan; Python tidak diperlukan untuk menjalankannya.

- Kemajuan anda disimpan dalam folder `data/` di sebelah fail boleh laku (`data/words_to_learn.csv`).
- `data/ms-da.csv` di sebelah fail boleh laku menggantikan senarai perkataan di dalamnya.
- `python tools/build_executable.py --no-speech` meninggalkan pakej suara; `--clean` membina semula dari awal.
- Fail boleh laku tidak disimpan dalam repositori. Bina di sistem tempat ia akan dijalankan; Windows mungkin menunjukkan amaran SmartScreen kerana fail tidak ditandatangani.

## Dokumentasi kod sumber

```bash
doxygen Doxyfile
```

HTML ditulis ke `docs/doxygen/html/index.html`.
