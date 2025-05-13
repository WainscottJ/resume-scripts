
from .ticket import Ticket  # Imports the Ticket class

class HelpDeskSystem:
    def __init__(self):
        self.tickets = []

    def create_ticket(self, requester_name, issue):
        ticket_id = len(self.tickets) + 1  # Generate a new ticket ID based on the list length
        new_ticket = Ticket(ticket_id, requester_name, issue, "Open")  # Create the new ticket
        self.tickets.append(new_ticket)  # Add the ticket to the list
        print(f"Ticket created successfully! Ticket ID: {ticket_id}")  # Success message

    def view_tickets(self):
        if not self.tickets:
            print("No tickets available.")  # Handle case with no tickets
        else:
            print("Tickets:")
            for ticket in self.tickets:
                print(ticket)  # Print each ticket using the __str__ method of Ticket

    def update_ticket_status(self, ticket_id, new_status):
        ticket_id = int(ticket_id)
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                ticket.update_status(new_status)  # Update the status
                print(f"Ticket updated successfully! {ticket}")  # Print updated ticket
                return
        print(f"Ticket {ticket_id} does not exist.")  # Handle invalid ticket ID



