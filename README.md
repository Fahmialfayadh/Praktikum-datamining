# Praktikum Data Mining

Repositori ini memuat kumpulan pengerjaan praktikum mata kuliah Data Mining. Setiap praktikum tinggal di foldernya masing-masing dan punya dokumentasi sendiri.

## Daftar Praktikum

| Folder | Topik | Deskripsi |
|---|---|---|
| [`praktikum-webscrap/`](praktikum-webscrap/) | Web Scraping & EDA | Scraping data Understat (EPL, La Liga, Serie A 2023–2025) + EDA metrik xG. |

## Struktur Direktori

```text
Praktikum/
├── praktikum-webscrap/   # Praktikum 1: Web Scraping & EDA (lihat README di dalamnya)
├── .gitignore
└── README.md             # Indeks repo (file ini)
```

Praktikum berikutnya tinggal tambah folder baru sejajar, misal `praktikum-preprocessing/`, beserta `README.md`-nya sendiri.

## Cara Pakai Umum

Setiap folder praktikum bersifat mandiri (punya `requirements.txt` sendiri). Masuk ke foldernya dulu, lalu ikuti `README.md` di dalamnya:

```bash
cd praktikum-webscrap
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```
