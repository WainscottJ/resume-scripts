#Name: Jacob Wainscott
#CIT 383-002
#Assignment 1 Python Conditionals and Loops

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

# This for loop iterates over each server and performs the checks on CPU ,
# disk space, whether a server is reachable or not, and checking if a server is critical
for server in servers:
    # Checks if the server's CPU usage is above 80%
    if server['cpu'] > 80:
        high_cpu_counter += 1
        if server['name'] != 'critical_server':
            print(f"High CPU usage on {server['name']}")

    # Checks if the server's disk space is below 10%
    if server['disk'] < 10:
        low_disk_counter += 1
        if server['name'] != 'critical_server':
            print(f"Low disk space on {server['name']}")

    # Checks if the server is reachable
    if not server['reachable']:
        unreachable_counter += 1
        if server['name'] != 'critical_server':
            print(f"Server {server['name']} is unreachable")

    # Checks if the server is named 'critical_server'
    if server['name'] == 'critical_server':
        print("Critical server found. Stopping checks.")
        break

# Print summary of the checks
print("\nSummary:")
print(f"Servers with high CPU: {high_cpu_counter}")
print(f"Servers with low disk space: {low_disk_counter}")
print(f"Unreachable servers: {unreachable_counter}")

