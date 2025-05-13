#!/usr/bin/env python3
# import necessary modules
import argparse
import os
import subprocess
import csv
import logging
import time

# Set up centralized logging
logging.basicConfig(
    filename='error_log_group_3.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_disk_space(directory, threshold): # check disk space usage for a given directory, compares threshold. Logs warning if exceeds threshold.
    try:
        print(f"[INFO] Checking disk space for directory {directory}")
        command = f"df -h {directory}" # execute command to get disk usage info
        output = subprocess.check_output(command, shell=True).decode('utf-8').splitlines()
        disk_usage = output[1].split()[4][:-1]  # Extract % usage as integer
        disk_usage = int(disk_usage)
        if disk_usage > threshold:
            logging.warning(f"Disk usage at {disk_usage}% - consider freeing up space.")
            print(f"[ALERT] Disk usage at {disk_usage}% - consider freeing up space.")
        else:
            print(f"[INFO] Disk usage is under control: {disk_usage}%")
    except Exception as e:
        logging.error(f"Error checking disk space: {e}")
        print(f"[ERROR] Error checking disk space: {e}")

def monitor_system_health(): # monitors cpu and memory usage every minute for 10 minites, logs metrics to system_health.log, alerts if CPU usage exceeds 80%
    print("[INFO] System health check every 1 minute for 10 minutes")
    health_logger = logging.getLogger('health_logger') # logger for system health metrics
    health_handler = logging.FileHandler('system_health.log')
    health_formatter = logging.Formatter('%(asctime)s - %(message)s')
    health_handler.setFormatter(health_formatter)
    health_logger.addHandler(health_handler)
    health_logger.setLevel(logging.INFO)

    for _ in range(10): # monitor for 10 iterations with 60 second intervals
        try:
            cpu_usage = subprocess.check_output( # get cpu usage percatage using shell commands
                r"top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - $1}'",
                shell=True).decode('utf-8').strip()
            memory_usage = subprocess.check_output( # get memory usage percentage using shell commands 
                r"free | grep Mem | awk '{print $3/$2 * 100.0}'",
                shell=True).decode('utf-8').strip()

            cpu_usage_float = float(cpu_usage)
            if cpu_usage_float > 80:
                print(f"[ALERT] High CPU usage detected: {int(cpu_usage_float)}%")
            # log metrics to system health log file
            health_logger.info(f"CPU usage: {cpu_usage}%")
            health_logger.info(f"Memory usage: {memory_usage}%")
            time.sleep(60) # wait 60 seconds between checks
        except subprocess.CalledProcessError as e:
            logging.error(f"Error monitoring system health: {e}")
            print(f"[ERROR] Error monitoring system health: {e}")

    print("[INFO] Logged CPU and memory usage to system_health.log.")

def create_user(username, role): # creates a new system user with specified role. Admins added to sudo group for elevated privilages
    try:
        if ' ' in username:
            logging.error("Invalid username format. Usernames should not contain spaces.")
            print("[ERROR] Invalid username format. Usernames should not contain spaces.")
            return
        print(f"[INFO] Creating user '{username}' with role '{role}'")
        os.system(f"useradd -m {username}") # create user with home directory
        if role == "admin":
            os.system(f"usermod -aG sudo {username}") # add admin users to sudo group
            print(f"[INFO] User '{username}' created successfully with home directory /home/{username}")
            print(f"[INFO] Role '{role}' assigned with full access permissions.")
        else:
            print(f"[INFO] User '{username}' created successfully with home directory /home/{username}")
            print(f"[INFO] Role '{role}' assigned with standard access permissions.")
        logging.info(f"User '{username}' created successfully with role '{role}'")
    except Exception as e:
        logging.error(f"Error creating user '{username}': {e}")
        print(f"[ERROR] Error creating user '{username}': {e}")

def delete_user(username): # deletes a user account and their home directory
    try:
        if ' ' in username:
            logging.error("Invalid username format. Usernames should not contain spaces.")
            print("[ERROR] Invalid username format. Usernames should not contain spaces.")
            return
        print(f"[INFO] Deleting user '{username}'")
        subprocess.run(f"userdel -r {username}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # delete user and their home directory
        print(f"[INFO] User '{username}' deleted successfully.")
        logging.info(f"User '{username}' deleted successfully.")
    except Exception as e:
        logging.error(f"Error deleting user '{username}': {e}")
        print(f"[ERROR] Error deleting user '{username}': {e}")

def update_user(username, password=None): # updates user information, primarily for setting/chaning passwords
    try:
        if ' ' in username:
            logging.error("Invalid username format. Usernames should not contain spaces.")
            print("[ERROR] Invalid username format. Usernames should not contain spaces.")
            return
        print(f"[INFO] Updating information for user '{username}'")
        if password: # change user password using chpasswd
            os.system(f"echo '{username}:{password}' | chpasswd")
            print(f"[INFO] Password updated successfully for '{username}'.")
            logging.info(f"Password updated successfully for '{username}'.")
        else:
            print(f"[INFO] No updates made for '{username}'.")
            logging.info(f"No updates made for '{username}'.")
    except Exception as e:
        logging.error(f"Error updating user '{username}': {e}")
        print(f"[ERROR] Error updating user '{username}': {e}")

def create_users_batch(csv_file): # creates multiple users from a CSV file containing username, role, and pass. Skips existing users and validates roles
    try:
        print(f"[INFO] Creating users from CSV file: {csv_file}")
        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                username, role, password = row
                if role not in ['admin', 'user']: # validate role
                    logging.error(f"Invalid role specified for user '{username}' in CSV file.")
                    print(f"[ERROR] Invalid role specified for user '{username}' in CSV file.")
                    print(f"[INFO] Skipping user '{username}'.")
                    continue
                if subprocess.call(f"getent passwd {username}", shell=True) == 0: # check if user already exists
                    logging.error(f"User '{username}' already exists. Skipping.")
                    print(f"[ERROR] User '{username}' already exists. Skipping.")
                    continue
                create_user(username, role) # create user and set password if provided
                if password:
                    update_user(username, password)
        print("[INFO] Batch user creation completed.")
        logging.info("Batch user creation completed.")
    except Exception as e:
        logging.error(f"Error processing CSV file: {e}")
        print(f"[ERROR] Error processing CSV file: {e}")

def organize_directory(directory): # organizes files in a directory by moving .txt files to text_files subdirectory and .log files to log_files subdirectory
    try: # create subdirectories if they don't exist
        text_dir = os.path.join(directory, "text_files")
        log_dir = os.path.join(directory, "log_files")
        os.makedirs(text_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)

        print(f"[INFO] Organizing files in {directory} by type")
        for file in os.listdir(directory): # move .txt files to text_files directory
            if file.endswith('.txt'):
                os.rename(os.path.join(directory, file), os.path.join(text_dir, file))
                print(f"[INFO] Moved .txt files to {text_dir}")
            elif file.endswith('.log'): # move .log files to log_files directory
                os.rename(os.path.join(directory, file), os.path.join(log_dir, file))
                print(f"[INFO] Moved .log files to {log_dir}")

        print("[INFO] Directory organization complete.")
        logging.info("Directory organization complete.")
    except Exception as e:
        logging.error(f"Error organizing directory: {e}")
        print(f"[ERROR] Error organizing directory: {e}")

def log_monitor(log_file): # analyzes log file counting ERROR, CRITICAL, and WARNING messages
    try:
        print(f"[INFO] Monitoring {log_file} for critical messages")
        with open(log_file, 'r') as f:
            content = f.readlines()
        # count occurrences of different log levels
        errors = sum(1 for line in content if "ERROR" in line)
        criticals = sum(1 for line in content if "CRITICAL" in line)
        warnings = sum(1 for line in content if "WARNING" in line)

        print(f"[INFO] Errors: {errors}; Criticals: {criticals}; Warnings: {warnings}")
    except Exception as e:
        logging.error(f"Error monitoring log file: {e}")
        print(f"[ERROR] Error monitoring log file: {e}")

def main(): # sets up command line argument parsing and dispatches to appropriate functions based on user input
    # sets up argument parser with subcommands
    parser = argparse.ArgumentParser(description="System Administration Script")
    subparsers = parser.add_subparsers(dest='command')
    # user management subcommands
    user_parser = subparsers.add_parser('user')
    user_parser.add_argument('--create', action='store_true')
    user_parser.add_argument('--create-batch', action='store_true')
    user_parser.add_argument('--delete', action='store_true')
    user_parser.add_argument('--update', action='store_true')
    user_parser.add_argument('--username', type=str)
    user_parser.add_argument('--role', type=str, choices=['admin', 'user'])
    user_parser.add_argument('--password', type=str)
    user_parser.add_argument('--csv', type=str)
    # directory and organization subcommands
    organize_parser = subparsers.add_parser('organize')
    organize_parser.add_argument('--dir', type=str)
    organize_parser.add_argument('--log-monitor', type=str)
    # system monitoring subcommands
    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--system', action='store_true')
    monitor_parser.add_argument('--disk', action='store_true')
    monitor_parser.add_argument('--dir', type=str)
    monitor_parser.add_argument('--threshold', type=int)

    args = parser.parse_args()

    if args.command == 'user': # dispatch to appropriate function based on command
        if args.create:
            create_user(args.username, args.role)
        elif args.create_batch:
            create_users_batch(args.csv)
        elif args.delete:
            delete_user(args.username)
        elif args.update:
            update_user(args.username, args.password)

    elif args.command == 'organize':
        if args.dir:
            organize_directory(args.dir)
        if args.log_monitor:
            log_monitor(args.log_monitor)

    elif args.command == 'monitor':
        if args.system:
            monitor_system_health()
        elif args.disk:
            if args.threshold:
                directory = args.dir if args.dir else os.getcwd()
                check_disk_space(directory, args.threshold)
            else:
                print("[ERROR] Disk threshold not specified.")

if __name__ == "__main__":
    main()