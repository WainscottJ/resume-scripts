README_group_3.md
Project Title: System Administration Automation Script
Course: CIT 383
Semester: Spring 2025
Instructor: Dr. Seth Adjei
Group Number: 3
File: sys_admin_group_3.py

Project Description
This Python-based system administration tool automates essential tasks for Linux system administrators on CentOS 9. The script supports modular subcommands for user account management, file organization, and system monitoring. It also includes robust logging and error handling.

Project Features
1. user Subcommand
--create: Create a single user with a role (admin or user)

--create-batch: Batch create users from a CSV file

--delete: Delete a specified user

--update: Update password or other user details

Logs errors (e.g., invalid roles, duplicates) and skips problematic entries

2. organize Subcommand
--dir: Organize files in a directory by file extension

--log-monitor: Analyze a log file and summarize error, warning, and critical messages

3. monitor Subcommand
--system: Monitor CPU and memory every 1 minute for 10 minutes

--disk: Check disk usage on a directory and alert if a specified threshold is exceeded

Sample Usage

# Create a single admin user
./sys_admin_group_3.py user --create --username johndoe --role admin

# Create users from a CSV file
./sys_admin_group_3.py user --create-batch --csv users.csv

# Delete a user
./sys_admin_group_3.py user --delete --username janedoe

# Update a user's password
./sys_admin_group_3.py user --update --username johndoe --password newpass123

# Organize files in a directory by type
./sys_admin_group_3.py organize --dir /home/student/docs

# Monitor and summarize log messages
./sys_admin_group_3.py organize --log-monitor /var/log/syslog

# Monitor CPU and memory usage
./sys_admin_group_3.py monitor --system

# Check disk usage and alert
./sys_admin_group_3.py monitor --disk --dir /home/student --threshold 85
Setup Instructions
Install Python 3 (if not already installed)

sudo dnf install python3 -y
Install required Python libraries


chmod +x sys_admin_group_3.py
Run the script with appropriate subcommand and arguments

./sys_admin_group_3.py user --create --username testuser --role user
Directory Structure of ZIP Submission

final_project_group_3.zip
├── sys_admin_group_3.py
├── pseudocode_group_3.txt
├── README_group_3.md
├── error_log_group_3.log              # sample error log
├── system_health_group_3.log          # sample monitoring log
Error Handling
All errors encountered during execution are logged with timestamps in:

error_log_group_3.log
👨‍Group 3 Members
Owen Townsend
Marshal Duncan
Jacob Wainscott
Riley Myers