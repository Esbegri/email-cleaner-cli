import re
import json
import sys
import logging
import argparse

parser = argparse.ArgumentParser(description="Email cleaning and validation CLI tool")
parser.add_argument("--input", required=True, help="Input file containing email addresses")
parser.add_argument("--output", required=True, help="Output file for cleaned email addresses")
parser.add_argument("--dry-run", action="store_true", help="Simulate without writing output file")

args = parser.parse_args()

try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        pattern = config["email_pattern"]
        log_file = config["log_file"]
except Exception as e:
    print(f"Configuration error: {e}")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Program started")
logging.info(f"Input file: {args.input}")

regex = re.compile(pattern)
emails = set()

try:
    with open(args.input, "r", encoding="utf-8") as file:
        for line in file:
            email = line.strip().lower()
            if regex.match(email):
                emails.add(email)

    if args.dry_run:
        logging.info(f"Dry-run mode: {len(emails)} valid emails found. No output written.")
    else:
        with open(args.output, "w", encoding="utf-8") as output:
            for email in sorted(emails):
                output.write(email + "\n")
        logging.info(f"{len(emails)} emails written to {args.output}")

    logging.info("Process completed successfully")

except FileNotFoundError:
    logging.error(f"Input file not found: {args.input}")
except Exception as e:
    logging.exception(f"Unexpected error: {e}")
