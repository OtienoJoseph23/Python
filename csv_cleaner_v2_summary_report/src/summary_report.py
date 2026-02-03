import csv
import json

def main():
    clean_path = 'data/processed/week04_sales_clean.csv'
    with open(clean_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total_rows = len(rows)

    unique_products = set()
    total_qty = 0
    total_revenue = 0.0

    qty_by_product = {}
    revenue_by_product = {}

    for row in rows:
        name = row["product_name"]
        qty = int(row["qty"])
        price = float(row["price"])

        unique_products.add(name)
        total_qty += qty

        rev = qty * price
        total_revenue += rev

        qty_by_product[name] = qty_by_product.get(name, 0) + qty
        revenue_by_product[name] = revenue_by_product.get(name, 0.0) + rev

    top_product = max(revenue_by_product, key=revenue_by_product.get) if revenue_by_product else None

    print("--- WEEK 4 SALES SUMMARY REPORT ---")
    print("Total rows:", total_rows)
    print("Unique products count:", len(unique_products))
    print("Total quantity:", total_qty)
    print("Total revenue:", total_revenue)
    print("Top product by revenue:", top_product)
    print("Per-product total quantity:", json.dumps(qty_by_product, indent=4))

if __name__ == '__main__':
    main()