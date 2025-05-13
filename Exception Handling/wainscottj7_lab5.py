#Name: Jacob Wainscott
#CIT 383-002 Module 5 Assignment 1 Exception Handling
#Date: 2/23/2025
import re
import time


# Custom Exceptions
class RepeatedPasswordError(Exception):
    pass


class WeakPasswordError(Exception):
    pass


class InvalidStructureError(Exception):
    pass


# List of common passwords
common_passwords = ["password", "123456", "123456789", "admin", "password1", "password123"]


# Function to validate password
def validate_password(password, previous_attempts):
    # Check for structural requirements
    if len(password) < 10:
        raise InvalidStructureError("Password must be at least 10 characters long.")
    if not re.search(r"[A-Z]", password):
        raise InvalidStructureError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise InvalidStructureError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise InvalidStructureError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*]", password):
        raise InvalidStructureError("Password must contain at least one special character (!@#$%^&*).")
    if " " in password:
        raise InvalidStructureError("Password must not contain spaces.")


    # Check for weak passwords
    if password.lower() in common_passwords or re.search(r"(password|admin)\d*", password.lower()):
        raise WeakPasswordError("Password is too weak or easily guessable.")


    # Check for repeated passwords
    if password in previous_attempts:
        raise RepeatedPasswordError("Repeated password attempt detected.")


def main():
    previous_attempts = []
    failed_attempts = 0


    while True:
        try:
            # Prompt user to enter password twice for confirmation
            password1 = input("Enter your password: ")
            password2 = input("Confirm your password: ")


            if password1 != password2:
                raise ValueError("Passwords do not match.")


            # Validate the password
            validate_password(password1, previous_attempts)


            # If validation passes, break the loop
            print("Password is valid.")
            break


        except (InvalidStructureError, WeakPasswordError, RepeatedPasswordError) as e:
            print(f"Error: {e}")
            failed_attempts += 1
            previous_attempts.append(password1)


            # Implement rate limiting after 3 failed attempts
            if failed_attempts >= 3:
                print("Too many failed attempts. Please wait for 5 seconds before trying again.")
                time.sleep(5)
                failed_attempts = 0


        except ValueError as e:
            print(f"Error: {e}")


        finally:
            print("Attempt completed.")


        # Stop after 5 failed attempts (including rate limiting)
        if len(previous_attempts) >= 5:
            print("Too many failed attempts. Exiting.")
            break


if __name__ == "__main__":
    main()



