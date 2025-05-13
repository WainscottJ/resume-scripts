#!/usr/bin/env python3
# Name: Jacob Wainscott
# CIT 383-002 Assignment 1 Python Functions
# Date: 2/9/2025

import random

# Define the systems list
systems = [
    ('System1', {
        'users': [('alice', 'admin'), ('bob', 'user')],
        'vulnerabilities': {'critical': 2, 'low': 5}
    }),
    ('System2', {
        'users': [('charlie', 'guest'), ('dave', 'admin')],
        'vulnerabilities': {'high': 3, 'medium': 2}
    })
]

# Function to audit permissions
def audit_permissions(system):
    system_name, details = system
    users = details['users']
    for user in users:
        if user[1] == 'admin':
            return {system_name: "Admin access found."}
    return {system_name: "No Admin Access"}

# Function to check vulnerabilities
def check_vulnerabilities(system):
    system_name, details = system
    vulnerabilities = details['vulnerabilities']
    if vulnerabilities.get('critical', 0) > 3:
        return {system_name: "Critical vulnerabilities detected. Immediate action required."}
    elif sum(vulnerabilities.values()) > 10:
        return {system_name: "Security Risk detected."}
    else:
        return {system_name: "Secure"}

# Function to generate random vulnerability data
def generate_random_vulnerability_data(systems):
    for system, details in systems:
        generated_users = [('user' + str(i), random.choice(['admin', 'guest', 'user'])) for i in range(1, random.randint(2, 5))]
        details['users'] = generated_users
        generated_vulnerabilities = {
            'critical': random.randint(1, 5),
            'low': random.randint(1, 5),
            'medium': random.randint(1, 5),
            'high': random.randint(1, 5),
        }
        details['vulnerabilities'] = generated_vulnerabilities

# Function to get security summary
def get_security_summary(systems, permission_status, vulnerability_status):
    permission_counter = {"with admin access": 0, "without admin access": 0}
    vulnerability_counter = {"secure": 0, "at risk": 0, "critical": 0}
    for system in systems:
        permission_result = audit_permissions(system)
        vulnerability_result = check_vulnerabilities(system)

        if "Admin access found." in permission_result.values():
            permission_counter["with admin access"] += 1
        else:
            permission_counter["without admin access"] += 1

        if "Critical vulnerabilities detected." in vulnerability_result.values():
            vulnerability_counter["critical"] += 1
        elif "Security Risk detected." in vulnerability_result.values():
            vulnerability_counter["at risk"] += 1
        else:
            vulnerability_counter["secure"] += 1

    permission_status.update(permission_counter)
    vulnerability_status.update(vulnerability_counter)

    print("\nSummary:\n"
          f"{permission_counter['with admin access']} system(s) with admin access, "
          f"{permission_counter['without admin access']} system(s) without admin access.\n"
          f"{vulnerability_counter['secure']} system(s) secure, "
          f"{vulnerability_counter['at risk']} system(s) at risk, "
          f"{vulnerability_counter['critical']} system(s) at critical risk.")

# Main function
def main():
    print("Initial System Data")
    generate_random_vulnerability_data(systems)
    print(systems)
    print("\nGenerating Random data for systems...")
    for system in systems:
        permission_result = audit_permissions(system)
        vulnerability_result = check_vulnerabilities(system)
        for key, value in permission_result.items():
            print(f"{key}: {value}")
        for key, value in vulnerability_result.items():
            print(f"{key}: {value}")

    permission_status = {}
    vulnerability_status = {}
    get_security_summary(systems, permission_status, vulnerability_status)

if __name__ == "__main__":
    main()
