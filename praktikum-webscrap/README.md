# Praktikum 1: Web Scraping & EDA Understat xG

Implementasi scraping data sepak bola dari Understat dan analisis eksplorasi data (EDA) untuk tiga kompetisi utama (EPL, La Liga, Serie A) pada musim 2023/2024, 2024/2025, dan 2025/2026.

## Struktur Direktori

```text
praktikum-webscrap/
├── data/                         # Direktori dataset hasil scraping
│   ├── understat_players_xg_2023.csv
│   ├── understat_players_xg_2024.csv
│   └── understat_players_xg_2025.csv
├── eda.ipynb                     # Notebook Analisis Eksplorasi Data
├── webscrap.py                   # Skrip scraper data Understat (CLI modular)
└── requirements.txt              # Dependensi Python
```

## Instalasi dan Lingkungan

Gunakan `uv` untuk membuat virtual environment dan menginstal dependensi:

```bash
# 1. Buat virtual environment
uv venv

# 2. Aktifkan virtual environment
source .venv/bin/activate

# 3. Instal dependensi
uv pip install -r requirements.txt
```

## Penggunaan

### 1. Web Scraping
Mengambil data statistik pemain dari Understat via endpoint AJAX internal:

```bash
# Mengambil seluruh musim default (2023, 2024, 2025)
python webscrap.py

# Atau mengambil musim tertentu saja
python webscrap.py 2024 2025
```
Dataset disimpan secara otomatis di folder `data/` dengan format file `understat_players_xg_<tahun>.csv`.

### 2. Exploratory Data Analysis (EDA)
Jalankan notebook [eda.ipynb](eda.ipynb) untuk analisis:
- Normalisasi metrik per 90 menit (`xG90`, `xA90`, `npxG_xA90`).
- Evaluasi kualitas pemilihan tembakan (`xG / shot`).
- Uji regresi ke rerata pada selisih `goals - xG` lintas 3 musim berurutan.
- Profiling taktis penyerang menggunakan rasio `xGBuildup / xGChain`.
- Komparasi gaya permainan dan tingkat disiplin kartu antar-liga.

---

## Kamus Data (Data Dictionary)

Berikut definisi operasional setiap variabel pada dataset hasil scraping dan metrik turunan yang digunakan dalam analisis.

### 1. Fitur Mentah (Raw Features - 19 Kolom)

| Nama Kolom | Tipe Data | Definisi Operasional |
|---|---|---|
| `id` | Integer | ID unik pemain di sistem basis data Understat. |
| `player_name` | String | Nama lengkap pemain. |
| `position` | String | Posisi bermain pemain di lapangan (lihat rincian kode posisi di bawah). |
| `team_title` | String | Nama klub yang dibela pemain pada musim tersebut. Jika pemain pindah klub di musim yang sama, nama klub digabung dengan koma (contoh: `"Chelsea,Manchester City"`). |
| `league` | String | Nama kompetisi liga (`EPL`, `La_liga`, `Serie_A`). |
| `games` | Integer | Total jumlah pertandingan yang diikuti pemain, baik sebagai pemain mula (*starter*) maupun pemain pengganti (*substitute*). |
| `time` | Integer | Total durasi menit bermain pemain di lapangan sepanjang musim bersangkutan. |
| `goals` | Integer | Jumlah gol aktual yang dicetak pemain (mencakup gol dari permainan terbuka, bola mati, dan tendangan penalti; tidak menghitung gol bunuh diri lawan). |
| `xG` | Float | *Expected Goals*. Nilai probabilitas statistik (skala 0–1 per tembakan) bahwa suatu tembakan akan menghasilkan gol, dihitung berdasarkan koordinat jarak ke gawang, sudut tembakan, jenis umpan sebelumnya, dan situasi permainan. |
| `npg` | Integer | *Non-Penalty Goals*. Jumlah gol aktual yang dicetak murni dari situasi non-penalti. Formula: `goals - gol_penalti`. |
| `npxG` | Float | *Non-Penalty Expected Goals*. Total akumulasi nilai xG pemain setelah seluruh tembakan penalti dikeluarkan. Karena penalti bernilai statis sekitar ~0.76 xG, npxG merefleksikan kualitas peluang murni dari permainan terbuka atau bola mati non-penalti. |
| `assists` | Integer | Jumlah umpan aktual yang langsung diselesaikan menjadi gol oleh rekan setim. |
| `xA` | Float | *Expected Assists*. Nilai probabilitas bahwa sebuah umpan yang dilepaskan pemain akan berbuah menjadi gol, terlepas dari apakah rekan setim yang menerima umpan tersebut berhasil mencetak gol atau tidak. Mengukur kualitas kreasi peluang pemain pengumpan. |
| `shots` | Integer | Total percobaan tembakan yang dilepaskan pemain, mencakup tembakan tepat sasaran (*on target*), melenceng (*off target*), maupun yang diblok oleh bek lawan. |
| `key_passes` | Integer | Umpan kunci (*key passes*). Jumlah umpan terakhir yang langsung dilanjutkan dengan percobaan tembakan oleh rekan setim. |
| `yellow_cards` | Integer | Akumulasi kartu kuning yang diterima pemain sepanjang musim. |
| `red_cards` | Integer | Akumulasi kartu merah yang diterima pemain (baik kartu merah langsung maupun akumulasi dua kartu kuning dalam satu laga). |
| `xGChain` | Float | Total nilai xG dari seluruh rangkaian penguasaan bola (*possession sequences*) yang berujung pada tembakan di mana pemain tersebut ikut terlibat di dalamnya. Mengukur kontribusi pemain dalam alur serangan tim dari tahap awal hingga akhir. |
| `xGBuildup` | Float | Total nilai xG dari rangkaian serangan yang melibatkan pemain, **dengan mengecualikan** tembakan dan umpan kunci langsung yang dibuat oleh pemain tersebut. Mengukur kontribusi pemain murni pada fase persiapan serangan (*build-up play*), bukan sebagai penyelesai akhir. |

#### Rincian Kode Posisi (`position`):
- `GK`: *Goalkeeper* (Penjaga Gawang)
- `D`: *Defender* (Pemain Belakang/Bek)
- `M`: *Midfielder* (Gelandang)
- `F`: *Forward* (Penyerang)
- `S`: *Substitute* (Pemain Pengganti)
- *Kombinasi*: Menunjukkan pemain yang bermain di beberapa posisi berbeda sepanjang musim. Contoh:
  - `F S`: Penyerang yang sering bermain sebagai pengganti.
  - `F M S`: Pemain multi-peran (penyerang/gelandang serang/sayap) yang juga mengalami rotasi bangku cadangan.
  - `D M`: Pemain bertahan yang juga diturunkan sebagai gelandang bertahan.

---

### 2. Fitur Turunan (*Engineered Features* pada EDA)

Metrik berikut dihitung di dalam notebook [eda.ipynb](eda.ipynb) untuk standardisasi analisis performa:

| Nama Metrik | Rumus / Definisi | Tujuan Analisis |
|---|---|---|
| `season` | Label string (contoh: `'2023/2024'`) | Identifikator tahun musim kompetisi saat data digabungkan. |
| `xG90` | `(xG / time) * 90` | Rata-rata ekspektasi gol per 90 menit bermain. Menghilangkan bias total menit bermain antar-pemain. |
| `xA90` | `(xA / time) * 90` | Rata-rata ekspektasi assist per 90 menit bermain. |
| `shots90` | `(shots / time) * 90` | Rata-rata frekuensi percobaan tembakan per 90 menit bermain. |
| `npxG90` | `(npxG / time) * 90` | Rata-rata ekspektasi gol non-penalti per 90 menit bermain. |
| `npxG_xA90` | `npxG90 + xA90` | Total akumulasi ancaman gol non-penalti dan kreasi assist per 90 menit. Metrik komposit untuk mengukur daya serang murni pemain. |
| `xg_per_shot` | `xG / shots` | Kualitas rata-rata peluang per tembakan. Nilai tinggi (> 0.20) menandakan pemilihan tembakan selektif dari jarak dekat; nilai rendah (< 0.05) menandakan tembakan spekulatif jarak jauh. |
| `buildup_ratio` | `xGBuildup / xGChain` | Rasio keterlibatan pemain dalam fase persiapan serangan dibanding total rantai serangan. Nilai mendekati 0 mencirikan penyerang kotak penalti (*poacher*); nilai mendekati 1 mencirikan perancang serangan dari lini belakang/tengah. |
| `goals - xG` | `goals - xG` | Nilai selisih efisiensi penyelesaian peluang (*finishing over/underperformance*). Digunakan dalam uji regresi ke rerata (*regression to the mean*). |
