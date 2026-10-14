# Penggunaan

🌐 [English](Usage) · [Dansk](Usage-da) · **Bahasa Malaysia**

## Berlatih dengan kad

1. Mulakan program dengan `python -m flash_card`.
2. Kad menunjukkan satu perkataan Melayu. Cuba ingat terjemahan Denmarknya.
3. Selepas tiga saat kad terbalik dan menunjukkan terjemahan.
4. Tekan tanda semak hijau jika anda tahu perkataan itu, atau pangkah merah jika tidak.
5. Satu perkataan rawak baharu muncul. Ulang.

Perkataan yang anda tandakan sebagai diketahui dibuang dan tidak muncul lagi. Apabila tiada perkataan lagi, kad menunjukkan "Nothing left to learn".

## Kemajuan anda

- Kali pertama anda menekan tanda semak hijau, program menulis `data/words_to_learn.csv` dengan perkataan yang anda belum tahu.
- Permulaan seterusnya menggunakan fail itu. Jika ia tiada, program menggunakan senarai penuh `data/ms-da.csv`.
- Untuk bermula semula, padam `data/words_to_learn.csv`.
- Pangkah merah tidak pernah mengubah fail.

## Format fail

Kedua-dua fail ialah teks UTF-8 dengan satu kad setiap baris dan sel dipisahkan oleh koma bertitik. Baris pertama mengandungi dua kod bahasa.

```text
ms;da
aku;mig
yang;hvilke
```

## Pilihan

| Pilihan | Maksud |
| --- | --- |
| `--data-dir <folder>` | Folder yang mengandungi `ms-da.csv` dan `words_to_learn.csv` (lalai: `data/` dalam repositori) |
| `--no-speech` | Jangan sebut perkataan Melayu, walaupun tambahan suara dipasang |

## Gunakan pasangan bahasa lain

Letakkan fail dengan format yang sama dalam folder data dan namakannya `ms-da.csv`, atau ubah `VOCABULARY_FILE_NAME` dan `LANGUAGE_NAMES` dalam `src/flash_card/constants.py`. Kod pada baris pertama dipaparkan sebagai nama bahasa daripada `LANGUAGE_NAMES`; kod yang tidak dikenali dipaparkan dengan huruf besar.

## Penyelesaian masalah

| Masalah | Apa yang perlu dilakukan |
| --- | --- |
| `No module named tkinter` | Pasang Tkinter (`python3-tk` pada Debian dan Ubuntu) |
| Tiada bunyi | Pasang tambahan `speech` dan periksa rangkaian; program mencatat amaran apabila penyebutan gagal |
| Program berhenti dengan mesej tentang fail | Fail CSV tidak betul; mesej menyebut fail dan barisnya. Fail tidak ditulis ganti |
