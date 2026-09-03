from pathlib import Path
import duckdb

# Chemins
DATA_DIR = Path("data")
DB_PATH = "airbnb_paris.duckdb"

def ingest_raw_data():
    conn = duckdb.connect(DB_PATH)

    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    # Ingestion directe des fichiers compressés
    print("Ingestion de listings.csv.gz...")
    conn.execute("""
        CREATE OR REPLACE TABLE raw.raw_listings AS
        SELECT * FROM read_csv_auto('data/listings.csv.gz', ignore_errors=true);
    """)

    print("Ingestion de calendar.csv.gz...")
    conn.execute("""
        CREATE OR REPLACE TABLE raw.raw_calendar AS
        SELECT * FROM read_csv_auto('data/calendar.csv.gz', ignore_errors=true);
    """)

    print("Ingestion de reviews.csv.gz...")
    conn.execute("""
        CREATE OR REPLACE TABLE raw.raw_reviews AS
        SELECT * FROM read_csv_auto('data/reviews.csv.gz', ignore_errors=true);
    """)

    print("Ingestion de neighbors.csv..")
    conn.execute("""
        CREATE OR REPLACE TABLE raw.raw_neighbors AS
        SELECT * FROM read_csv_auto('data/neighbors.csv', ignore_errors=true);
    """)


    # Vérification
    listings_count = conn.execute("SELECT count(*) FROM raw.raw_listings;").fetchone()[0]
    calendar_count = conn.execute("SELECT count(*) FROM raw.raw_calendar;").fetchone()[0]
    reviews_count = conn.execute("SELECT count(*) FROM raw.raw_reviews;").fetchone()[0]
    neighbors_count = conn.execute("SELECT count(*) FROM raw.raw_neighbors;").fetchone()[0]

    print(f" Ingestion terminée !")
    print(f"• raw_listings : {listings_count:,} lignes")
    print(f"• raw_calendar : {calendar_count:,} lignes")
    print(f"• raw_reviews : {reviews_count:,} lignes")
    print(f"• raw_neighbors : {neighbors_count:,} lignes")

    conn.close()

if __name__ == "__main__":
    ingest_raw_data()
