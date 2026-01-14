```markdown
# Email Cleaner CLI Tool

A simple and practical **command-line Python tool** that extracts, validates, and deduplicates email addresses from a text file.

Designed for **automation**, **log tracking**, and **config-based customization**.

---

## Features

- ✅ Extracts valid email addresses
- ✅ Removes duplicate emails
- ✅ Case-insensitive processing
- ✅ CLI-based (command-line interface)
- ✅ Dry-run mode (simulation without writing output)
- ✅ Configurable regex pattern via JSON
- ✅ Logging system (file + console)

---

## Project Structure

```text
.
├── main.py
├── config.json
├── sample_input.txt
├── sample_output.txt
├── requirements.txt
└── README.md

## Requirements

• Python 3.10+

• No external libraries required (uses Python Standard Library)

## Configuration

{
  "email_pattern": "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$",
  "log_file": "app.log"
}

Usage
Standard Run:

Bash

python main.py --input sample_input.txt --output output.txt
Dry Run (Simulation):

Bash

python main.py --input sample_input.txt --output output.txt --dry-run

Example
Input (sample_input.txt):

Plaintext

test@gmail.com
hello@yahoo.com
test@gmail.com
invalid-email
HELLO@yahoo.com
Output (output.txt):

Plaintext

hello@yahoo.com
test@gmail.com

Logging
• All operations and errors are logged.

• Logs are written both to the console and the log file defined in config.json.

Use Cases
• Cleaning email lists before marketing campaigns.

• Preparing datasets for CRM import.

• Removing duplicates from large contact files.

• Automation in system scripts.

Author: Developed as a practice project for freelance-oriented Python CLI tools.