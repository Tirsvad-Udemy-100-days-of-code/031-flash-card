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

## Keluaran dan fail boleh laku (Windows)

Halaman keluaran [v0.2.0](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/releases/tag/v0.2.0) dan [v0.1.0](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/releases/tag/v0.1.0) mempunyai nota keluaran. Fail boleh laku belum dilampirkan di sana kerana had muat naik pelayan menolak fail sebesar ini (HTTP 413); bina seperti yang diterangkan di bawah. Fail tidak ditandatangani, jadi Windows mungkin menunjukkan amaran SmartScreen.

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

## Semakan tanpa desktop (Docker)

Ujian, linter, tangkapan skrin dan ujian asap bagi binari Linux dijalankan dalam kontena Debian pada skrin maya, jadi tiada tetingkap dibuka pada desktop anda sendiri.

```bash
docker build -f docker/debian.Dockerfile -t flash-card-debian .
# linter dan seluruh suite ujian, termasuk ujian tetingkap sebenar
docker run --rm -v "$PWD:/repo:ro" flash-card-debian bash /repo/tools/docker/in-container.sh run-checks.sh
# tangkapan skrin ke ./build/container-out
docker run --rm -v "$PWD:/repo:ro" -v "$PWD/build/container-out:/out" flash-card-debian bash /repo/tools/docker/in-container.sh screenshots.sh /out
# bina binari Linux dan tekan butang "tahu" 5 kali (binari dan kod sumber)
docker run --rm -v "$PWD:/repo:ro" flash-card-debian bash /repo/tools/docker/in-container.sh smoke-binary.sh 5
```

Dalam Windows PowerShell tulis `${PWD}` untuk `$PWD`. Repositori dipasang baca sahaja dan disalin di dalam kontena.

- Desktop ialah Xvfb dengan pengurus tetingkap GNOME (mutter). GNOME Shell dicuba dahulu dan tidak bermula dalam kontena (ia memerlukan pengurus log masuk), jadi skrip beralih kepada mutter dan mencetak yang mana dijalankan.
- Fail boleh laku Windows disemak dalam **Windows Sandbox** (Windows 11 Pro, ciri diaktifkan): `powershell -File tools\sandbox\run.ps1 -Runs 5` selepas `python tools/build_executable.py`. Sandbox menunjukkan tetingkapnya sendiri semasa berjalan; klik dibuat di dalam sandbox.
- Tidak dilindungi: macOS (tidak boleh dijalankan dalam Docker pada Windows atau Linux dan lesen Apple hanya membenarkannya pada perkakasan Apple), dan Windows sebenar dalam kontena Debian.

## Dokumentasi kod sumber

```bash
doxygen Doxyfile
```

HTML ditulis ke `docs/doxygen/html/index.html`.
