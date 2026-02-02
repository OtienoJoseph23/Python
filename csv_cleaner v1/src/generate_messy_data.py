# === Creating a messy CSV ===
import os #imports a toolset that allows python to interact with the computer's operating system

#create a folder data/raw if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

#Define the messy content as a string
messy_data = """   Product Name , QTY ,    price
Laptop, " 12" , 599
dESk, "10", 120.00
LAPTOP bag, "12 ", 25.50"""

#Write content to the specified file
file_path = "data/raw/week03_sales_raw.csv"
with open(file_path, "w") as file:
    file.write(messy_data.strip())

print("Messy CSV created at data/raw/week03_sales_raw.csv")