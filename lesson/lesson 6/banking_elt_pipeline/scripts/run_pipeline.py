import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent


def run(script_name):
    command = [sys.executable, str(SCRIPTS_DIR / script_name)]
    print("\n$", " ".join(command))
    subprocess.run(command, check=True)


def main():
    try:
        run("01_init_bigquery.py")
        run("02_load_raw.py")
        run("03_transform_clean.py")
        run("04_check_result.py")
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode)

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()
