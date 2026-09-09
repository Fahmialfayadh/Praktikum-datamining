import argparse
from pathlib import Path
import pandas as pd
import requests

DEFAULT_LEAGUES = ["EPL", "La_liga", "Serie_A"]
DEFAULT_SEASONS = ["2023", "2024", "2025"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

COLUMNS_TO_KEEP = [
    "id",
    "player_name",
    "position",
    "team_title",
    "league",
    "games",
    "time",
    "goals",
    "xG",
    "npg",
    "npxG",
    "assists",
    "xA",
    "shots",
    "key_passes",
    "yellow_cards",
    "red_cards",
    "xGChain",
    "xGBuildup",
]


def scrape_season(season: str, leagues: list[str] = None, output_dir: Path = None) -> pd.DataFrame:
    """Scrape data pemain untuk satu musim kompetisi tertentu dari Understat."""
    if leagues is None:
        leagues = DEFAULT_LEAGUES
    if output_dir is None:
        output_dir = Path("data")

    output_dir.mkdir(parents=True, exist_ok=True)
    all_players = []

    print(f"\n--- Memulai scraping musim {season} ---")
    for league in leagues:
        url = f"https://understat.com/getLeagueData/{league}/{season}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code == 200:
                data = res.json()
                players = data.get("players", [])
                for p in players:
                    p["league"] = league
                    all_players.append(p)
                print(f"[{league}] Berhasil mengambil {len(players)} pemain.")
            else:
                print(f"[{league}] Gagal mengambil data, status HTTP: {res.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[{league}] Terjadi kesalahan jaringan: {e}")

    df = pd.DataFrame(all_players)
    if not df.empty:
        available_cols = [c for c in COLUMNS_TO_KEEP if c in df.columns]
        df_filtered = df[available_cols]

        output_path = output_dir / f"understat_players_xg_{season}.csv"
        df_filtered.to_csv(output_path, index=False)
        print(f"Musim {season}: {len(df_filtered)} baris disimpan ke {output_path}")
        return df_filtered
    else:
        print(f"Musim {season}: Tidak ada data yang berhasil dikumpulkan.")
        return df


def main():
    parser = argparse.ArgumentParser(
        description="Scraper data pemain dan metrik xG dari Understat (EPL, La Liga, Serie A)"
    )
    parser.add_argument(
        "seasons",
        nargs="*",
        default=DEFAULT_SEASONS,
        help="Daftar tahun musim kompetisi (contoh: 2023 2024 2025). Default: 2023 2024 2025",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("data"),
        help="Direktori penyimpanan file CSV (default: data/)",
    )
    args = parser.parse_args()

    for season in args.seasons:
        scrape_season(str(season), output_dir=args.output_dir)


if __name__ == "__main__":
    main()