# Laporan Analisis Eksplorasi Data (EDA)
**Mata Kuliah:** Data Mining  
**Topik:** Web Scraping & Exploratory Data Analysis Statistik Performa Pemain Sepak Bola (Understat)  
**Kompetisi & Periode:** English Premier League (EPL), La Liga, dan Serie A (Musim 2023/2024, 2024/2025, 2025/2026)  

---

## 1. Deskripsi Dataset

Dataset ini diperoleh melalui proses *web scraping* langsung dari endpoint AJAX internal platform analitik sepak bola [Understat](https://understat.com). Data mencakup statistik performa individu pemain dari tiga kompetisi sepak bola kasta teratas Eropa (EPL, La Liga, dan Serie A) selama tiga musim kompetisi berturut-turut (2023/2024 hingga 2025/2026).

### Karakteristik Umum:
- **Jumlah Observasi:** 5.232 baris data.
- **Rincian per Musim:** 2023/2024 (1.758 baris), 2024/2025 (1.751 baris), 2025/2026 (1.723 baris).
- **Entitas:** 2.812 pemain unik dari 213 klub berbeda.
- **Jumlah Atribut:** 19 atribut mentah dan 8 atribut turunan (*engineered features*).

### Ringkasan Atribut Utama:
1. **Identitas & Konteks:** `id` (ID unik), `player_name` (nama), `team_title` (klub), `league` (liga), `position` (kode peran bermain).
2. **Kuantitas Partisipasi:** `games` (jumlah laga), `time` (total menit bermain).
3. **Produktivitas Gol & Kualitas Peluang:**
   - `goals` (gol aktual total), `xG` (*Expected Goals* - peluang gol kumulatif).
   - `npg` (*Non-Penalty Goals*), `npxG` (*Non-Penalty Expected Goals*).
4. **Kreasi Peluang:** `assists` (assist aktual), `xA` (*Expected Assists*), `shots` (total tembakan), `key_passes` (umpan kunci berujung tembakan).
5. **Disiplin:** `yellow_cards` (kartu kuning), `red_cards` (kartu merah).
6. **Kontribusi Progresi Taktis:**
   - `xGChain`: Total xG dari seluruh rangkaian penguasaan bola yang melibatkan pemain dan berujung pada tembakan.
   - `xGBuildup`: Nilai xG rangkaian serangan yang melibatkan pemain tanpa menghitung tembakan dan umpan kunci langsung dari pemain bersangkutan (murni fase persiapan serangan).

---

## 2. Statistik Deskriptif

### A. Atribut Numerik
Sebagian besar metrik ofensif menunjukkan karakteristik distribusi menceng ke kanan (*right-skewed*), di mana mayoritas pemain mencatatkan angka rendah dan hanya sebagian kecil pemain elite yang mencatatkan nilai ekstrem:

| Atribut | Mean | Std Dev | Min | Median (Q2) | Q3 | Max |
|---|---|---|---|---|---|---|
| `games` | 20,25 | 11,85 | 1,00 | 22,00 | 31,00 | 39,00 |
| `time` | 1.292,76 | 1.004,73 | 1,00 | 1.156,00 | 2.120,25 | 3.504,00 |
| `goals` | 1,73 | 3,15 | 0,00 | 0,00 | 2,00 | 31,00 |
| `xG` | 1,97 | 3,19 | 0,00 | 0,79 | 2,37 | 31,65 |
| `npg` | 1,58 | 2,78 | 0,00 | 0,00 | 2,00 | 24,00 |
| `npxG` | 1,82 | 2,84 | 0,00 | 0,77 | 2,29 | 26,44 |
| `shots` | 16,42 | 20,32 | 0,00 | 10,00 | 23,00 | 161,00 |
| `key_passes` | 12,22 | 14,88 | 0,00 | 7,00 | 18,00 | 137,00 |
| `xGChain` | 5,65 | 5,73 | 0,00 | 4,17 | 8,21 | 48,54 |
| `xGBuildup` | 3,46 | 3,69 | 0,00 | 2,41 | 5,05 | 26,29 |

### B. Atribut Kategorikal
- **Distribusi Liga:** La Liga (1.788 observasi / 34,2%), Serie A (1.775 observasi / 33,9%), EPL (1.669 observasi / 31,9%). Distribusi seimbang antar-kompetisi (~560–600 pemain per musim).
- **Distribusi Posisi Pemain:** Dari 16 kombinasi peran, frekuensi tertinggi didominasi oleh peran rotasi dengan kode `S` (*Substitute*):
  1. `D S` (Bek cadangan): 1.172 pemain.
  2. `M S` (Gelandang cadangan): 1.061 pemain.
  3. `F M S` (Penyerang/Gelandang serang rotasi): 683 pemain.
  4. `S` (Pemain pengganti murni): 655 pemain.
  5. `F S` (Penyerang cadangan): 438 pemain.
  6. `GK` (Penjaga gawang): 321 pemain.

---

## 3. Penanganan Data (Data Cleaning & Preprocessing)

### A. Identifikasi dan Penanganan Nilai Hilang (*Missing Values*)
Pemeriksaan dilakukan menggunakan fungsi `df.isnull().sum()` pada seluruh 19 kolom. Ditemukan **0 nilai hilang (0%)** di seluruh baris. Data dari Understat terstruktur secara lengkap karena pemain yang tidak mencatatkan aksi tertentu diberi nilai numerik `0` atau `0.0`.

### B. Identifikasi dan Penanganan Outlier serta Bias Durasi
Pemeriksaan distribusi menunjukkan keberadaan *outlier* statistik ekstrem pada variabel `goals`, `xG`, dan `shots`. Misalnya, Erling Haaland (31,65 xG; 161 tembakan) dan Mohamed Salah (48,54 xGChain).
- **Analisis Kontekstual Outlier:** Nilai-nilai ekstrem ini **bukan kesalahan entri data (*data entry error*)**, melainkan representasi akurat performa atlet elite di level tertinggi. Menghapus baris-baris ini menggunakan metode statistik standar (seperti IQR trimming) akan menghilangkan esensi analisis performa pemain sepak bola.
- **Langkah Penanganan yang Diambil:**
  1. **Thresholding Menit Bermain:** Diterapkan filter ambang batas $time \ge 900$ menit (ekuivalen 10 laga penuh) untuk eliminasi *noise* statistik dari pemain muda/cadangan yang hanya bermain beberapa menit tetapi memiliki rasio semu yang tinggi.
  2. **Standardisasi Metrik per 90 Menit:** Mengonversi metrik absolut menjadi laju performa per satuan waktu standar:
     $$\text{xG90} = \frac{\text{xG}}{\text{time}} \times 90, \quad \text{npxG\_xA90} = \frac{\text{npxG} + \text{xA}}{\text{time}} \times 90$$
     Langkah ini mengoreksi bias menit bermain sehingga pemain reguler dan pemain rotasi dapat diperbandingkan secara adil.
  3. **Thresholding Percobaan Tembakan:** Filter minimum 30 percobaan tembakan diterapkan saat menghitung rasio kualitas tembakan (`xG / shots`) untuk menghindari bias rasio 100% dari pemain yang hanya menembak 1 kali lalu berbuah gol.

---

## 4. Visualisasi Data dan Interpretasi Temuan

### A. Efisiensi Ancaman Non-Penalti per 90 Menit (Diagram Batang)
- **Visualisasi:** Diagram batang horizontal peringkat 10 pemain teratas metrik `npxG_xA90`.
- **Temuan & Interpretasi:** Normalisasi durasi mengungkap efisiensi tinggi dari pemain rotasi. Alexander Sørloth (2024/2025) mencatatkan **1,24 npxG+xA per 90** dalam 1.525 menit bermain, mengungguli penyerang utama dengan menit bermain penuh. Darwin Núñez (2023/2024, 1,08 per 90) dan Ferran Torres (2024/2025, 1,09 per 90) teridentifikasi sebagai pencipta ancaman elite per menit bermain.

### B. Kualitas Seleksi Tembakan: xG per Tembakan (Scatter Plot)
- **Visualisasi:** Scatter plot total tembakan terhadap total xG dengan pewarnaan gradasi nilai `xg_per_shot`.
- **Temuan & Interpretasi:**
  - **Penembak Selektif / Peluang Jarak Dekat:** Thiago (0,294 xG/shot), Callum Wilson (0,289), dan Alexander Isak (0,283) mencatatkan rata-rata probabilitas gol mendekati 30% per tembakan, hampir tiga kali lipat rata-rata kompetisi (0,10–0,11 xG/shot), yang mengindikasikan seleksi peluang dengan nilai konversi tinggi.
  - **Penembak Spekulatif:** Ruslan Malinovskiy (0,025 xG/shot dari 39 tembakan) dan Unai López (0,027 dari 32 tembakan) menghabiskan volume tembakan dari jarak jauh dengan peluang konversi rata-rata di bawah 3%, yang secara taktis membuang kepemilikan bola tim.

### C. Keberlanjutan Overperformance: Uji Regresi ke Rerata (Dual Scatter Plot)
- **Visualisasi:** Dua scatter plot berdampingan yang menguji korelasi selisih gol terhadap ekspektasi (`goals - xG`) pada dua transisi musim berturut-turut.
- **Temuan & Interpretasi:**
  - Korelasi transisi 2023/2024 ke 2024/2025 adalah **r = 0,016** ($n = 634$).
  - Korelasi transisi 2024/2025 ke 2025/2026 adalah **r = 0,092** ($n = 656$).
  - Pelacakan kohort 454 pemain selama 3 musim penuh menunjukkan pemain dengan overperformance ekstrem musim 2023/2024 (Phil Foden +7,69; Alexander Sørloth +7,57; Jude Bellingham +6,03) seluruhnya mengalami penurunan drastis mendekati atau melampaui angka nol di musim-musim berikutnya.
  - **Kesimpulan Statistik:** Fenomena overperformance gol dalam rentang satu musim tunggal terbukti didominasi oleh fluktuasi variansi acak (*sample size noise*) dan perubahan peran taktis, bukan kemampuan konversi yang berkelanjutan.

### D. Peran Taktis Penyerang: Rasio Buildup terhadap Chain (Scatter Plot)
- **Visualisasi:** Scatter plot `xGChain` vs `xGBuildup` dengan rasio `xGBuildup / xGChain`.
- **Temuan & Interpretasi:**
  - *Poacher Murni* (rasio $< 0,10$): Chris Wood (0,06), Jamie Vardy (0,07), Moise Kean (0,07). Pemain-pemain ini memiliki keterlibatan minimal pada fase sirkulasi bola dan berfungsi murni sebagai target akhir.
  - *Playmaking Forward* (rasio $> 0,75$): Federico Valverde (0,80), Yan Couto (0,85). Beroperasi di lini serang namun aktif mengalirkan progresi bola dari sepertiga awal lapangan.

### E. Karakteristik Komparatif Antar-Liga (Tabel Agregat & Diagram Batang Disiplin)
- **Visualisasi:** Diagram batang akumulasi kartu kuning dan kartu merah per musim per kompetisi.
- **Temuan & Interpretasi:**
  - **Pola Taktis:** EPL mencatat rata-rata kualitas tembakan tertinggi (**0,113 xG/shot**), merefleksikan peluang tembakan yang secara rata-rata memiliki probabilitas gol lebih tinggi dibanding La Liga (0,104) dan Serie A (0,102).
  - **Tingkat Pelanggaran:** La Liga secara konsisten mencatatkan jumlah kartu tertinggi di setiap musim (puncak 99 kartu merah di musim 2025/2026), mengindikasikan intensitas pelanggaran dan standar ketegasan wasit yang jauh lebih ketat dibanding EPL (44 kartu merah) dan Serie A (65 kartu merah).

---

## 5. Ringkasan Kesimpulan

1. Model xG Understat terbukti merepresentasikan kualitas peluang secara akurat (korelasi Pearson `goals` vs `xG` $r = 0,933$).
2. Analisis performa berbasis total gol bias terhadap durasi bermain; standardisasi per 90 menit berhasil mengungkap pemain dengan efisiensi tinggi pada menit bermain terbatas.
3. Overperformance gol musiman terbukti secara empiris tidak berkelanjutan (*regresses to the mean*), dengan korelasi antar-musim nyaris nol ($r \le 0,092$).
4. Metrik dekomposisi rantai serangan (`xGChain` dan `xGBuildup`) mampu membedakan profil taktis penyerang (*poacher* vs *playmaker*) secara kuantitatif.
5. Terdapat disparitas gaya antar-kompetisi: EPL mencatatkan nilai xG per tembakan tertinggi (0,113), sedangkan La Liga memiliki frekuensi pelanggaran dan hukuman kartu tertinggi.

