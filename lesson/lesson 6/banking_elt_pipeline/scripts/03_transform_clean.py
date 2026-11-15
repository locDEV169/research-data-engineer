from etl import transform


def main():
    transform.run()
    print("Next step: python scripts/04_check_result.py")


if __name__ == "__main__":
    main()
