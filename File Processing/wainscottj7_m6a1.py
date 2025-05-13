#!/usr/bin/python3
import csv
#Name: Jacob Wainscott
#Date: 3/23/2025
#Assignment: Module 6 Assignment 1 File Processing

#This function will read the employee_logins.csv file and return a list of employee login records.
def read_user_data():
    filename = "employee_logins.csv"
    rows = []  # List for login records

    try:
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader) #This will skip the header

            # Read each row and store it
            for row in csvreader:
                rows.append(row)
    except FileNotFoundError:
        print("Error: The file 'employee_logins.csv' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return rows

#This function will create a
# new CSV file named [your_nku_user_id]_affected_users.csv with three
# columns: name (last name; first name), login_count, and
# login_count_excess (number of login attempts beyond 100). It will also
# print to the console a table of suspicious employees
def write_suspicious_logins_data():
    records = read_user_data()
    suspicious_logins = []  # List to store suspicious logins

    # Identify suspicious logins (login_count >= 100)
    for record in records:
        first_name = record[0]
        last_name = record[1]
        try:
            login_count = int(record[2])  # Convert login attempts to integer
            if login_count >= 100:
                login_count_excess = login_count - 100
                suspicious_logins.append([f"{last_name}; {first_name}", login_count, login_count_excess])
        except ValueError:
            print(f"Invalid login count entry: {record}")

    if suspicious_logins:
        # Write to a new CSV file
        nku_user_id = "wainscottj7"
        output_filename = f"{nku_user_id}_affected_users.csv"

        try:
            with open(output_filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["name", "login_count", "login_count_excess"])  # Write headers
                csvwriter.writerows(suspicious_logins)  # Write suspicious login records
        except Exception as e:
            print(f"Error writing to file {output_filename}: {e}")
            return

        # Print suspicious logins to console in a table-like format
        print("\nSuspicious Logins:")
        print(f"{'Name (Lastname; Firstname)':<30}{'Login Count':<15}{'Excess Logins'}")
        print("-" * 60)

        for entry in suspicious_logins:
            print(f"{entry[0]:<30}{entry[1]:<15}{entry[2]}")

        print(f"\nTotal suspicious employees: {len(suspicious_logins)}")
    else:
        print("No suspicious logins found.")


#This function will call the previous two functions and handle the overall logic.
def main_wainscottj7():
    records = read_user_data()
    if records:
        write_suspicious_logins_data()


if __name__ == "__main__":
    main_wainscottj7()





