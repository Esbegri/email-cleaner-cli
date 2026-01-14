import re
import json
import sys
import logging
import argparse
import os


def load_config(config_path: str = "config.json") -> tuple[str, str]:
    """Load regex pattern and log file path from config.json with safe defaults."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"'{config_path}' not found.")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    pattern = config.get("email_pattern", r"^[\w\.-]+@[\w\.-]+\.\w+$")
    log_file = config.get("log_file", "app.log")

    if not isinstance(pattern, str) or not pattern.strip():
        raise ValueError("Invalid 'email_pattern' in config.json.")
    if not isinstance(log_file, str) or not log_file.strip():
        raise ValueError("Invalid 'log_file' in config.json.")

    return pattern, log_file


def setup_logging(log_file: str) -> None:
    """Configure logging to both file and stdout."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Professional Email Cleaning and Validation CLI Tool"
    )
    parser.add_argument("--input", required=True, help="Path to the input text file")
    parser.add_argument("--output", required=True, help="Path to the output cleaned file")
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate process without saving results"
    )

    args = parser.parse_args()

    # 1) Load configuration
    try:
        pattern, log_file = load_config("config.json")
    except json.JSONDecodeError:
        print("Critical Error: 'config.json' is not a valid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

    # 2) Setup logging
    setup_logging(log_file)

    logging.info("Service started")
    logging.info(f"Parameters: Input={args.input}, Output={args.output}, Dry-Run={args.dry_run}")

    # 3) Prepare counters and regex
    try:
        regex = re.compile(pattern)
    except re.error as e:
        logging.critical(f"Invalid regex pattern in config.json: {e}")
        sys.exit(1)

    total_lines = 0
    empty_lines = 0
    invalid_count = 0
    valid_matches = 0
    unique_emails = set()

    # 4) Process input
    try:
        if not os.path.exists(args.input):
            logging.critical(f"Input file not found: {args.input}")
            sys.exit(1)

        with open(args.input, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                total_lines += 1

                email = line.strip().lower()
                if not email:
                    empty_lines += 1
                    continue

                # fullmatch ensures entire string matches the pattern
                if regex.fullmatch(email):
                    valid_matches += 1
                    unique_emails.add(email)
                else:
                    invalid_count += 1
                    logging.warning(f"Invalid email skipped at line {line_num}: {email}")

        # Duplicates = valid matches - unique emails
        duplicates_removed = max(0, valid_matches - len(unique_emails))

        # 5) Summary report (log + console)
        logging.info("SUMMARY")
        logging.info(f"Total lines processed : {total_lines}")
        logging.info(f"Empty lines           : {empty_lines}")
        logging.info(f"Valid emails (matches): {valid_matches}")
        logging.info(f"Valid unique emails   : {len(unique_emails)}")
        logging.info(f"Invalid emails        : {invalid_count}")
        logging.info(f"Duplicates removed    : {duplicates_removed}")

        # 6) Write output (unless dry-run)
        if args.dry_run:
            logging.info("Dry-run mode enabled: no output file was written.")
        else:
            with open(args.output, "w", encoding="utf-8") as output:
                for email in sorted(unique_emails):
                    output.write(email + "\n")
            logging.info(f"SUCCESS: Output written to '{args.output}'")

    except PermissionError:
        logging.critical(
            f"Permission denied: Could not write to '{args.output}'. "
            "Is it open in another program or protected?"
        )
        sys.exit(1)
    except Exception as e:
        logging.exception(f"An unexpected error occurred during processing: {e}")
        sys.exit(1)
    finally:
        logging.info("Service execution finished")


if __name__ == "__main__":
    main()
