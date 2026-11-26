from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from util import clear_terminal


def download_inputs():
    # Get current date
    current_date = datetime.now()

    # For testing:
    current_date = datetime(2025, 12, 2)

    # Ensure we're in December
    if current_date.month != 12:
        print("Not in December, exiting.")
        return

    input_dir = Path("_inputs")
    input_dir.mkdir(exist_ok=True)

    # Loop through days 1 to current day
    for day in range(1, current_date.day + 1):
        # Zero-pad days 1-9: 01, 02, ..., 09
        day_str = f"{day:02d}"

        input_filename = input_dir / f"{day_str}.txt"
        example_filename = input_dir / f"{day_str}example.txt"

        # Download puzzle input
        if not input_filename.exists():
            with input_filename.open("w", encoding="utf-8") as output:
                subprocess.run(
                    ["aocd", str(day), str(current_date.year)],
                    stdout=output,
                    check=True,
                    text=True,
                )

            print(f"Downloaded input for day {day_str}, year {current_date.year}")
        else:
            print(
                f"Input file for day {day_str}, "
                f"year {current_date.year} already exists."
            )

        # Download example
        if not example_filename.exists():
            with example_filename.open("w", encoding="utf-8") as output:
                subprocess.run(
                    [
                        "aocd",
                        str(day),
                        str(current_date.year),
                        "--example",
                    ],
                    stdout=output,
                    check=True,
                    text=True,
                )

            print(f"Downloaded example for day {day_str}, year {current_date.year}")
        else:
            print(
                f"Example file for day {day_str}, "
                f"year {current_date.year} already exists."
            )


def start_day():
    parser = argparse.ArgumentParser(description="Run a day")

    parser.add_argument(
        "day_number",
        type=int,
        nargs="?",
        default=None,
        help="Day number",
    )

    parser.add_argument(
        "--file",
        help="File to run",
    )

    args = parser.parse_args()

    # Get the absolute path of the current directory
    current_dir = Path(__file__).parent

    # Define the subfolders to check
    subfolders_to_check = ["solutions", "current"]

    # Save the original sys.path
    original_sys_path = sys.path.copy()

    # STARTUP methods
    download_inputs()
    clear_terminal()

    try:
        # Add both directories to sys.path
        for subfolder in subfolders_to_check:
            subfolder_path = current_dir / subfolder
            sys.path.append(str(subfolder_path))

        if args.file:
            script_path = Path(args.file)

            if script_path.exists():
                print(f"Running {script_path}\n")

                spec = importlib.util.spec_from_file_location(
                    "custom_script",
                    str(script_path),
                )

                if spec is None or spec.loader is None:
                    raise ImportError(f"Unable to load script: {script_path}")

                module = importlib.util.module_from_spec(spec)
                sys.modules["custom_script"] = module
                spec.loader.exec_module(module)

            else:
                print(f"Script not found at {script_path}")

        elif args.day_number is None:
            # Run tester.py if no day number is provided
            tester_script = current_dir / "solutions" / "tester.py"

            if tester_script.exists():
                print("Running tester.py ...\n")

                spec = importlib.util.spec_from_file_location(
                    "tester",
                    str(tester_script),
                )

                if spec is None or spec.loader is None:
                    raise ImportError(f"Unable to load tester: {tester_script}")

                module = importlib.util.module_from_spec(spec)
                sys.modules["tester"] = module
                spec.loader.exec_module(module)

            else:
                print(f"Tester script not found at {tester_script}")

        else:
            if not 1 <= args.day_number <= 25:
                parser.error("day_number must be between 1 and 25")

            # Zero-pad the requested day
            day_str = f"{args.day_number:02d}"
            module_name = f"{day_str}"

            # Search for the day's script in the subfolders
            script_found = False

            for subfolder in subfolders_to_check:
                script_path = current_dir / subfolder / f"{module_name}.py"

                if script_path.exists():
                    script_found = True
                    print(f"Running {script_path}\n")

                    spec = importlib.util.spec_from_file_location(
                        module_name,
                        str(script_path),
                    )

                    if spec is None or spec.loader is None:
                        raise ImportError(f"Unable to load script: {script_path}")

                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)

            if not script_found:
                print(f"Script for Day {day_str} not found.")

    finally:
        # Restore the original sys.path
        sys.path = original_sys_path
        print("\n")


if __name__ == "__main__":
    start_day()
