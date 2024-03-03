# Subreg.py

# Subtensor Wallet Registration Script

This Python script automates the process of registering a wallet with the Subtensor network. It's designed to handle multiple attempts, manage delays between retries, and respond to various prompts automatically.

## Features

- **Automated Registration**: Automates the `btcli subnet register` command process.
- **Retry Logic**: Implements retry logic for registration, handling up to 10,000 attempts with customizable delays.
- **Password Management**: Securely reads the wallet password from a file.
- **Error Handling**: Captures and responds to common errors, including insufficient balance.

## Prerequisites

- Python 3.x installed on your system.
- `pexpect` library installed. Install via pip if necessary using `pip install pexpect`.
- Access to a terminal or command line interface.

## Setup Instructions

1. Ensure Python 3 and `pexpect` are installed on your system.
2. Place the script in a desired directory.
3. Create a password file containing your wallet's password in plain text and note its path.

## Usage

1. Open your terminal and navigate to the script's directory.
2. Run the script using the following command, replacing `path/to/password_file` with the actual path to your password file:

   ```bash
   python3 subreg.py path/to/password_file

    The script will start the registration process, handling prompts and retries as configured.

Configuration

    Modify max_attempts, retry_delay, and other variables in the script to customize the retry logic and delays.
    Ensure the command variable in the script correctly points to your btcli command with appropriate flags and parameters.

Troubleshooting

    If you encounter permission errors, ensure the script has executable permissions.
    For issues related to pexpect not found, verify that pexpect is installed (pip show pexpect).
    Ensure the password file is correctly formatted and the path in the script matches its location.

Contributing

Feel free to fork the repository and submit pull requests with enhancements or fixes.
