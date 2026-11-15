from etl import extract


def main():
    extract.run()
    print("Next step: python scripts/03_transform_clean.py")


if __name__ == "__main__":
    main()
