import subprocess
import sys


def run(command):
    print("\n$", " ".join(command))
    subprocess.run(command, check=True)


def main():
    python = sys.executable
    try:
        run([python, "01_init_bigquery.py"])
        run([python, "02_load_raw.py"])
        run([python, "03_transform_clean.py"])
        run([python, "04_check_result.py"])
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode)

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()
