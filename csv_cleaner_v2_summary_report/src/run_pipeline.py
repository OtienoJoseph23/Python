from generate_messy_data import main as generate_main
from clean_data import main as clean_main
from summary_report import main as summary_main

def main():
    generate_main()
    clean_main()
    summary_main()

if __name__ == '__main__':
    main()