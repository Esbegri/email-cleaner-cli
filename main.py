import re
import json
import sys
import logging
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Professional Email Cleaning and Validation CLI Tool")
    parser.add_argument("--input", required=True, help="Path to the input text file")
    parser.add_argument("--output", required=True, help="Path to the output cleaned file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate process without saving results")

    args = parser.parse_args()

    # 1. Configuration Loading with Error Handling
    try:
        if not os.path.exists("config.json"):
            print("Critical Error: 'config.json' not found. Please create it.")
            sys.exit(1)
            
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            pattern = config.get("email_pattern", r"^[\w\.-]+@[\w\.-]+\.\w+$")
            log_file = config.get("log_file", "app.log")
    except json.JSONDecodeError:
        print("Critical Error: 'config.json' is not a valid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"Initialization Error: {e}")
        sys.exit(1)

    # 2. Logging Setup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("Service started")
    logging.info(f"Parameters: Input={args.input}, Output={args.output}, Dry-Run={args.dry_run}")

    # 3. Processing
    regex = re.compile(pattern)
    unique_emails = set()

    try:
        if not os.path.exists(args.input):
            logging.error(f"File not found: {args.input}")
            return

        with open(args.input, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                email = line.strip().lower()
                if not email:
                    continue
                if regex.match(email):
                    unique_emails.add(email)
                else:
                    logging.warning(f"Invalid email format skipped at line {line_num}: {email}")

        if args.dry_run:
            logging.info(f"DRY-RUN SUMMARY: {len(unique_emails)} valid unique emails detected. No changes made to disk.")
        else:
            with open(args.output, "w", encoding="utf-8") as output:
                for email in sorted(unique_emails):
                    output.write(email + "\n")
            logging.info(f"SUCCESS: {len(unique_emails)} unique emails exported to '{args.output}'")

    except PermissionError:
        logging.error(f"Permission denied: Could not write to '{args.output}'. Is it open in another program?")
    except Exception as e:
        logging.exception(f"An unexpected error occurred during processing: {e}")
    finally:
        logging.info("Service execution finished")

if __name__ == "__main__":
    main()