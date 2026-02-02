# === Cleaning the CSV ===
import os
import csv

#clean the text by removing extra spaces and standardizing case
def normalize_text(text):
    return text.strip().lower() if text is not None else ""

#ensure quantity is a valid integer
def is_valid_qty(qty):
    try:
        return int(qty.strip().replace('"', '')) >= 1
    except (ValueError, AttributeError):
        return False

def clean_csv():
    #ensure the processed folder exists
    os.makedirs("data/processed", exist_ok=True)

    input_path = "data/raw/week03_sales_raw.csv"
    output_path = "data/processed/week03_sales_clean.csv"

    cleaned_rows = []
    with open(input_path, 'r') as f:
        #DictReader uses the first row as keys for each row dictionary
        reader = csv.DictReader(f)

        #clean column names: strip + lowercase + replace spaces with _
        new_header = [h.strip().lower().replace(" ", "_") for h in reader.fieldnames]

        for row in reader:
            row_qty = row.get(" QTY ")
            #match old messy headers to new clean ones while cleaning values
            clean_row = {
                "product_name": normalize_text(row.get("   Product Name ")),
                "qty": int(row_qty.strip().replace('"', '') if is_valid_qty(row_qty) else None),
                "price": float(row.get("    price").strip())
            }
            cleaned_rows.append(clean_row)

        #write the cleaned data to the new file
        with open(output_path, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=new_header)
            writer.writeheader()
            writer.writerows(cleaned_rows)

if __name__ == "__main__":
    clean_csv()
    print("Cleaned data saved to data/processed/week03_sales_clean.csv")