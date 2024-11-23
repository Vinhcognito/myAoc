from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from shared.util import clear_terminal


def download_inputs():
    # Get current date
    current_date = datetime.now()

    # Ensure we're in December
    if current_date.month != 12:
        print("Not in December, exiting.")
        return

    # Loop through days 1 to current day
    for day in range(1, current_date.day + 1):
        # Construct filenames
        input_filename = f"inputs\\day{day}.txt"
        example_filename = f"inputs\\day{day}example.txt"

        # Download puzzle input
        if not os.path.exists(input_filename):
            command = f"aocd {day} {current_date.year} > {input_filename}"
            subprocess.run(command, shell=True, check=True)
            print(f"Downloaded input for day {day}, year {current_date.year}")
        else:
            print(f"Input file for day {day}, year {current_date.year} already exists.")

        # Download example
        if not os.path.exists(example_filename):
            command = f"aocd {day} {current_date.year} --example > {example_filename}"
            subprocess.run(command, shell=True, check=True)
            print(f"Downloaded example for day {day}, year {current_date.year}")
        else:
            print(
                f"Example file for day {day}, year {current_date.year} already exists."
            )


def start_day():
    parser = argparse.ArgumentParser(description="Run a day")
    parser.add_argument(
        "day_number", type=int, nargs="?", default=None, help="Day number"
    )
    args = parser.parse_args()

    # Get the absolute path of the current directory
    current_dir = Path(__file__).parent

    # Define the subfolders to check
    subfolders_to_check = ["completed", "current"]

    # Save the original sys.path
    original_sys_path = sys.path.copy()

    ## STARTUP methods
    # get missing advent inputs
    download_inputs()
    # clean the terminal
    clear_terminal()

    try:
        # Add both directories to sys.path
        for subfolder in subfolders_to_check:
            subfolder_path = current_dir / subfolder
            sys.path.append(str(subfolder_path))

        if args.day_number is None:
            # Run tester.py if no day number is provided
            tester_script = current_dir / "current" / "tester.py"

            if tester_script.exists():
                print("Running tester.py ...\n")
                spec = importlib.util.spec_from_file_location(
                    "tester", str(tester_script)
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules["tester"] = module
                spec.loader.exec_module(module)

            else:
                print(f"Tester script not found at {tester_script}")
        else:
            # Search for the day's script in the subfolders
            script_found = False

            for subfolder in subfolders_to_check:
                script_path = current_dir / subfolder / f"day{args.day_number}.py"

                if script_path.exists():
                    script_found = True
                    print(f"Running {script_path}")

                    spec = importlib.util.spec_from_file_location(
                        f"day{args.day_number}", str(script_path)
                    )
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[f"day{args.day_number}"] = module
                    spec.loader.exec_module(module)

            if not script_found:
                print(f"Script for Day {args.day_number} not found.")

    finally:
        # Restore the original sys.path
        sys.path = original_sys_path
        print("\n")


if __name__ == "__main__":
    start_day()
