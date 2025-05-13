#!/usr/bin/env python3

#Name: Jacob Wainscott
#Date: 3/2/2025
#Module 5 Assignment 2 Command Line Arguments

import argparse

def calculate_average(cpu_usage, memory_usage):
    return (cpu_usage + memory_usage) / 2


def check_threshold(cpu_usage, memory_usage, threshold, show_percentage):
    alert_message = ""

    # Urgent Alert if both exceed threshold
    if cpu_usage > threshold and memory_usage > threshold:
        if show_percentage:
            alert_message = f"Urgent Alert: Both CPU and memory usage exceed the threshold of {threshold * 100:.2f}%"
        else:
            alert_message = f"Urgent Alert: Both CPU and memory usage exceed the threshold of {threshold:.2f}"

    # Standard Alert if either exceeds threshold
    elif cpu_usage > threshold or memory_usage > threshold:
        if show_percentage:
            alert_message = f"Alert: CPU or memory usage exceeds the threshold of {threshold * 100:.2f}%"
        else:
            alert_message = f"Alert: CPU or memory usage exceeds the threshold of {threshold:.2f}"

    return alert_message


def main():
    # command-line argument parsing
    parser = argparse.ArgumentParser(description="Monitor CPU and memory usage.")

    # Positional arguments
    parser.add_argument('cpu_usage', type=float, help="CPU usage of the server (between 0 and 1).")
    parser.add_argument('memory_usage', type=float, help="Memory usage of the server (between 0 and 1).")

    # Optional arguments
    parser.add_argument('-p', '--percentage', action='store_true', help="Display output as percentage.")
    parser.add_argument('-t', '--threshold', type=float, help="Set a threshold for alerting (between 0 and 1).")

    args = parser.parse_args()

    # Validate CPU and memory usage inputs
    if not (0 <= args.cpu_usage <= 1):
        print("Error: CPU usage must be a value between 0 and 1.")
        return
    if not (0 <= args.memory_usage <= 1):
        print("Error: Memory usage must be a value between 0 and 1.")
        return
    if args.threshold and not (0 <= args.threshold <= 1):
        print("Error: Threshold must be a value between 0 and 1.")
        return

    # Calculate the average usage
    avg_usage = calculate_average(args.cpu_usage, args.memory_usage)

    # Format for percentage if specified
    if args.percentage:
        cpu_usage_display = f"{args.cpu_usage * 100:.2f}%"
        memory_usage_display = f"{args.memory_usage * 100:.2f}%"
        avg_usage_display = f"{avg_usage * 100:.2f}%"
    else:
        cpu_usage_display = f"{args.cpu_usage:.2f}"
        memory_usage_display = f"{args.memory_usage:.2f}"
        avg_usage_display = f"{avg_usage:.2f}"

    # Display the resource usage summary
    print("Resource Usage Summary")
    print("********************************")
    print(f"CPU usage: {cpu_usage_display}")
    print(f"Memory usage: {memory_usage_display}")
    print(f"Average resource usage: {avg_usage_display}")

    # Check and display any alerts based on the threshold
    if args.threshold:
        alert_message = check_threshold(args.cpu_usage, args.memory_usage, args.threshold, args.percentage)
        if alert_message:
            print(alert_message)


if __name__ == "__main__":
    main()


