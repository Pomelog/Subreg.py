import pexpect
import time
import re


def read_password_from_file(file_path):
    with open(file_path, 'r') as file:
        password = file.readline().strip()
    print(f"Password read successfully from {file_path}")
    return password

def register_wallet(password_file):
    password = read_password_from_file(password_file)
    command = "btcli subnet register --netuid  --wallet.name  --wallet.hotkey "

    attempt = 1
    max_attempts = 10000 # Consider the practicality of this high number.
    retry_delay = 15
    recycle_delay = 45  # Time to wait after "Recycling TAO for Registration..."
    retry_delay_on_insufficient_balance = 5  # Added for handling insufficient balance.

    while attempt <= max_attempts:
        print(f"\nAttempt {attempt} of {max_attempts}: Starting registration process...")
        child = pexpect.spawn(command, encoding='utf-8', timeout=10)

        try:
            # Use regex to be more flexible with the expected strings (accounting for ANSI codes).
            child.expect("Enter subtensor network .*: ", timeout=10)
            child.sendline("local")
            print("Network selected: local")

            """

            # Check for an "Insufficient balance" message immediately after sending "local"
            index = child.expect([
                "rYour balance is:.*",  # Expected continuation if balance is sufficient
                "Insufficient balance .*"  # The message indicating insufficient funds
            ], timeout=10)

            # If "Insufficient balance" is detected, restart the registration process
            if index == 1:
                print("Insufficient balance detected. Restarting the process...")
                attempt += 1
                time.sleep(retry_delay)
                continue

            # Modify this pattern to ignore ANSI escape sequences
            #full_prompt_pattern = r"Do you want to continue\?.*\x1b\[[0-9;]*m\(n\):"

            """

            # Use this pattern in the expect call
            balance_prompt = re.compile(r"Your balance is:.*")
            child.expect(balance_prompt, timeout=10)
            child.sendline("y")
            print("Confirmed to continue with registration.")

            """
            # Await balance check confirmation.
            child.expect("Your balance is .*", timeout=10)
            print("Balance checked.")

            child.expect("The cost to register by recycle is .*", timeout=10)
            print("Cost to register by recycle retrieved.")

            # The prompt "Do you want to continue? [y/n] (n):" may include ANSI escape codes, so we use a regex pattern
            # that accepts any characters (including ANSI codes) between the question and the user input prompt.
            continue_pattern = r"Do you want to continue\?.*\(n\):"
            child.expect(continue_pattern, timeout=10)
            child.sendline("y")
            print("Confirmed to continue with registration.")

            """

            # Increase timeout here if the next step takes a while to process
            child.expect("Enter password to unlock key:", timeout=30)
            child.sendline(password)
            print("Password entered successfully.")

            # Check for confirmation to recycle and register.
            child.expect("Recycle ", timeout=30)
            child.sendline("y")
            print("Confirmed to recycle and register.")

              # Look for the "error" keyword in the output
            child.expect("error", timeout=45)
            print("An error occurred during registration.")
            attempt += 1
            time.sleep(retry_delay)  # Wait before retrying
            continue  # Restart the process

            # Here, add handling for "Insufficient balance" message.
            # Note: This section is commented out. To handle "Insufficient balance", you would
            # include logic similar to the timeout handling but check child.before for the specific message.

            # Await completion of the process.
            child.expect(pexpect.EOF, timeout=120)
            print("Registration process likely completed.")  # Adjusted message for clarity.
            print("Output:", child.before)
            break  # Exit the loop on successful registration.

        except pexpect.exceptions.TIMEOUT as e:
            print(f"Timeout occurred: {str(e)}. Checking for specific known issues...")
            if "Insufficient balance" in child.before:
                print("Detected insufficient balance. Waiting to retry...")
                time.sleep(retry_delay_on_insufficient_balance)
            else:
                print("Unknown timeout issue. Waiting to retry...")
                time.sleep(retry_delay)
        except pexpect.exceptions.EOF as e:
            print(f"Unexpected end of file: {str(e)}. Last output before EOF: {child.before}")
            # Handle specific known EOF scenarios here.
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        finally:
            if child.isalive():
                child.close()

        attempt += 1

    if attempt > max_attempts:
        print("Maximum attempt limit reached. Registration not successful.")

# Replace the placeholder path with the actual path to your password file.
register_wallet('path/to/wallet')
