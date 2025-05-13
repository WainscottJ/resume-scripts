#!/usr/bin/env python3

# Name: Jacob Wainscott
# CIT 383-002
# Assignment 1 Python Conditionals and Loops

def main():
    # Define the list of servers
    servers = [
        {'name': 'server1', 'cpu': 85, 'disk': 20, 'reachable': True},
        {'name': 'server2', 'cpu': 70, 'disk': 5, 'reachable': False},
        {'name': 'critical_server', 'cpu': 90, 'disk': 15, 'reachable': True},
        {'name': 'server4', 'cpu': 60, 'disk': 50, 'reachable': True}
    ]

    # Initialize counters for summary
    high_cpu_counter = 0
    low_disk_counter = 0
    unreachable_counter = 0

    # This for loop iterates over each server and performs the checks
    for server in servers:
        if server['cpu'] > 80:
            high_cpu_counter += 1
            if server['name'] != 'critical_server':
                print(f"High CPU usage on {server['name']}")

        if server['disk'] < 10:
            low_disk_counter += 1
            if server['name'] != 'critical_server':
                print(f"Low disk space on {server['name']}")

        if not server['reachable']:
            unreachable_counter += 1
            if server['name'] != 'critical_server':
                print(f"Server {server['name']} is unreachable")

        if server['name'] == 'critical_server':
            print("Critical server found. Stopping checks.")
            break

    # Print summary of the checks
    print("\nSummary:")
    print(f"Servers with high CPU: {high_cpu_counter}")
    print(f"Servers with low disk space: {low_disk_counter}")
    print(f"Unreachable servers: {unreachable_counter}")

if __name__ == "__main__":
    main()
