import os

def main():
    os.makedirs("data/raw", exist_ok=True)

    messy_data = """
    Product Name , QTY , price
    Laptop, "12" , 599
    dESk, "10", 120.00
    LAPTOP bag, "12 ", 25.50
    Mouse, "", 15.00
    Keyboard, "0", 40
    Monitor, "-2", 250
    Chair, "2.5", 80
    Cable, "3", "KES 120"
    , "4", 10
    Webcam, "1", 
    Headset, " 7 ", 0
    Tablet, "five", 300"""

    file_path = "data/raw/week04_sales_dirty.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(messy_data.strip())

    print(f"Messy CSV created at: {file_path}")

if __name__ == '__main__':
    main()