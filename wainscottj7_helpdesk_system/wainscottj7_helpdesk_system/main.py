#!/usr/bin/env python3
#Name: Jacob Wainscott
#Date: 2/12/2025
#Assignment 1 Module 4 IT Help Desk Management Systems
# CIT 383-002

from helpdesk import HelpDeskSystem

def main():
    helpdesk = HelpDeskSystem()  # Create an instance of HelpDeskSystem

    while True:
        print("\nWelcome to the IT Help Desk System")
        print("1. Create a new ticket")
        print("2. View all tickets")
        print("3. Update ticket status")
        print("4. Exit")

        choice = input("Choose an option: ")

        # Option 1: Create a new ticket
        if choice == "1":
            #This will ask user to type a name but, they cannot leave it empty
            requester_name = input("Enter your name: ")
            while not requester_name.strip():  # Check if the input is empty or only spaces
                print("Name cannot be empty. Please enter your name.")
                requester_name = input("Enter your name: ")

            #Same here where user is asked to type the issue they cannot leave this blank
            issue = input("Describe your issue: ")
            while not issue.strip():  # Check if the issue description is empty or only spaces
                print("Issue description cannot be empty. Please describe your issue.")
                issue = input("Describe your issue: ")

            # Create the ticket
            helpdesk.create_ticket(requester_name, issue)

        # Option 2: View all tickets
        elif choice == "2":
            helpdesk.view_tickets()

        # Option 3: Update a ticket's status
        elif choice == "3":
            # Validates the ticket ID input must be a number and an existing ticket
            ticket_id = input("Enter Ticket ID: ")
            while not ticket_id.isdigit() or not any(ticket.ticket_id == int(ticket_id) for ticket in helpdesk.tickets):
                print("Invalid ticket ID. Please enter a valid ticket ID.")
                ticket_id = input("Enter Ticket ID: ")

            # Validates status input must be one of 'Open', 'In Progress', or 'Resolved'
            new_status = input("Enter new status (Open, In Progress, Resolved): ")
            #This is to allow the user to type the word in any case but, they will have to type the word or ask them again
            while new_status.lower() not in ["open", "in progress", "resolved"]:
                print("Invalid status. Please enter one of the following: 'Open', 'In Progress', 'Resolved'.")
                new_status = input("Enter new status (Open, In Progress, Resolved): ")

            # Update the ticket status
            helpdesk.update_ticket_status(ticket_id, new_status)

        # Option 4: Exit the program
        elif choice == "4":
            print("Exiting, Thank you for using HelpDesk!")
            break

        # Invalid option handling
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



