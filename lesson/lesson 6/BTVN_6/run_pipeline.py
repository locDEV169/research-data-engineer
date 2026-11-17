import subprocess
import sys


def run(command):
    print("\n$", " ".join(command))
    subprocess.run(command, check=True)


def main():
    python = sys.executable
    try:
        run([python, "00_check_connection.py"])
        run([python, "01_init_bronze.py"])
        run([python, "02_load_bronze.py"])
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode)

    print("\nBronze pipeline complete.")


if __name__ == "__main__":
    main()
