from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_gdrive, load_to_postgres

def main():
    try:
        print("Mulai \n")

        print("--- Extract ---\n")
        raw_data = extract_data()

        print("--- Transformasi ---\n")
        transformed_df = transform_data(raw_data)
        if transformed_df.empty:
            raise ValueError("Transformasi gagal")

        print("\nData yang bersih")
        print(transformed_df.head())
        print("\nInfo dataset:")
        print("- Kolom: {list(transformed_df.columns)}")
        print("- Tipe data:")
        print(transformed_df.dtypes)

        print("\n[CSV] Menyimpan ke CSV...")
        load_to_csv(transformed_df, "products.csv")
        
        print("\n[POSTGRES] Menyimpan ke PostgreSQL...")
        load_to_postgres(transformed_df)

        print("\n[Google Drive] Menyimpan ke Google Drive")
        load_to_gdrive(transformed_df, '1caB8rcwPs0TNvMMxG3vnKRxM3IU3336JelqeU5MfTiU', 'google-sheets-api.json')

        print(f"\nJumlah data akhir: {len(transformed_df)}")

    except Exception as e:
        print(f"\nError dalam proses ETL: {e}")

if __name__ == "__main__":
    main()