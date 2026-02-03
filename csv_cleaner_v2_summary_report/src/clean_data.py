import csv
import json
import os

def normalize_text(text):

    if not text:
        return None, "missing"

    return text.strip().lower(), None

def parse_qty(raw_qty):

    if raw_qty is None:
        return None, "empty"

    cleaned = str(raw_qty).strip().strip('"\'')

    if not cleaned:
        return None, "empty"

    try:
        if "." in cleaned:
            return None, "decimal"

        qty = int(cleaned)
        if qty == 0:
            return None, "zero"
        if qty < 0:
            return None, "negative"

        return qty, None
    except ValueError:
        return None, "text"

def parse_price(raw_price):
    if raw_price is None:
        return None, "empty"

    cleaned = str(raw_price).strip().strip('"\'')

    if cleaned == "":
        return None, "empty"

    try:

        if any(char.isalpha() for char in cleaned):
            return None, "text"

        price = float(cleaned)

        if price < 0:
            return None, "negative"

        return price, None

    except ValueError:
        return None, "invalid format"

def build_header_map(fieldnames):
    clean_headers = [header.strip().lower().replace(" ", '_') for header in fieldnames]
    return dict(zip(clean_headers, fieldnames))

def clean_csv(raw_rows, header_map):

    # containers
    clean_rows = []
    error_log = []

    # counters
    total_rows = 0
    used_rows = 0
    skipped_rows = 0
    reason_counts = {}

    # loop through each row (with row index)
    # extract raw values: raw product name, raw qty, raw price
    for index, raw in enumerate(raw_rows, 1):
        total_rows += 1

        raw_product_name = raw.get(header_map["product_name"])
        raw_qty = raw.get(header_map["qty"])
        raw_price = raw.get(header_map["price"])

        # clean + validate product name
        # we use the version that returns (value, error) to match with others
        clean_name, name_err = normalize_text(raw_product_name)
        if name_err:
            error_log.append({
                "row": index, "field": "product_name", "raw_value": raw_product_name,
                "reason": name_err, "product": clean_name
            })
            skipped_rows += 1
            reason_counts[name_err] = reason_counts.get(name_err, 0) + 1
            continue

        # parse + validate qty
        qty, qty_err = parse_qty(raw_qty)

        if qty_err:
            error_log.append({
                "row": index, "field": "qty", "raw_value": raw_qty,
                "reason": qty_err, "product": clean_name
            })
            skipped_rows += 1
            reason_counts[qty_err] = reason_counts.get(qty_err, 0) + 1
            continue

        # parse + validate price
        price, price_err = parse_price(raw_price)

        if price_err:
            error_log.append({
                "row": index, "field": "price", "raw_value": raw_price,
                "product": clean_name, "reason": price_err
            })
            skipped_rows += 1
            reason_counts[price_err] = reason_counts.get(price_err, 0) + 1
            continue

        # if all three are valid: build a clean row
        clean_row = {
            "product_name": clean_name,
            "qty": qty,
            "price": price
        }
        clean_rows.append(clean_row)
        used_rows += 1

    # build a summary
    summary = {
        "total_rows": total_rows,
        "used_rows": used_rows,
        "skipped_rows": skipped_rows,
        "skipped_by_reason": reason_counts
    }
    return clean_rows, error_log, summary

def write_clean_csv(clean_rows, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["product_name", "qty", "price"])
        writer.writeheader()
        writer.writerows(clean_rows)

def main():
    in_path = 'data/raw/week04_sales_dirty.csv'
    out_path = 'data/processed/week04_sales_clean.csv'
    log_path = 'data/processed/week04_error_log.json'

    with open(in_path, "r", encoding='utf-8', newline="") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)
        header_map = build_header_map(reader.fieldnames)


    # run the cleaning function
    clean_rows, error_log, summary = clean_csv(raw_rows, header_map)

    write_clean_csv(clean_rows, out_path)

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8", newline="") as f:
        json.dump(error_log, f, indent=4)

    print("--- SUMMARY ---")
    print(json.dumps(summary, indent=4))
    print(f"Clean CSV: {out_path}")
    print(f"Error log: {log_path}")


if __name__ == '__main__':
    main()