# Flash Card

🌐 [English](Home) · [Dansk](Home-da) · **Bahasa Malaysia**

Program kad imbas untuk mempelajari perkataan Melayu yang paling kerap digunakan beserta terjemahan Denmark. Ia ialah penyelesaian hari ke-31 kursus Udemy *100 Days of Code: The Complete Python Pro Bootcamp*.

![Bahagian depan kad: perkataan Melayu](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/raw/branch/main/docs/images/screenshot-front.png)
![Bahagian belakang kad selepas tiga saat: terjemahan Denmark](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card/raw/branch/main/docs/images/screenshot-back.png)

| Halaman | Baca apabila anda mahu |
| --- | --- |
| [Pemasangan](Install-ms) | Mencipta `.venv`, memasang program dan menjalankan ujian |
| [Penggunaan](Usage-ms) | Berlatih dengan kad, memahami fail kemajuan dan menggunakan pilihan |
| [Seni bina](Architecture-ms) | Melihat lapisan dan mencari kod bagi setiap langkah tugasan |

## Empat langkah tugasan

| Langkah | Apa yang program lakukan | Pencapaian |
| --- | --- | --- |
| 1. Antara muka pengguna | Tetingkap dengan satu kad dan dua butang | MIL-002 |
| 2. Kad imbas baharu | Satu perkataan rawak daripada senarai perkataan setiap kali butang ditekan | MIL-003 |
| 3. Terbalikkan kad | Selepas 3 saat kad menunjukkan terjemahan Denmark | MIL-004 |
| 4. Simpan kemajuan anda | Perkataan yang diketahui dibuang dan selebihnya disimpan dalam `words_to_learn.csv` | MIL-005 |
| Tambahan | Perkataan Melayu disebut (pilihan) | MIL-006 |

## Untuk peserta kursus

Nama fungsi tugasan dikekalkan: `next_card`, `flip_card`, `is_known`, serta atribut `flip_timer` dan `current_card`. Data dibaca dengan modul `csv` pustaka standard dan bukan `pandas`, jadi program teras tidak mempunyai kebergantungan semasa larian.

Repositori: <https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/031-flash-card>
