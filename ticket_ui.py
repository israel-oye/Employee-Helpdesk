import tickets_db as db, time
from ticket_object import Ticket
from datetime import datetime as dt

def display_menu():
    
    print("Vecta Corp Help Desk Aplication \n\
        COMMAND VIEW\n\
            --------------------------------\n\
            view - View open tickets\n\
            issue - View issue\n\
            add - Add a ticket\n\
            update - Update a ticket\n\
            del - Delete a ticket\n\
            exit - Exit the application.\n\
            menu - View option menu\n\
            --------------------------------")

def view_tickets():
    print("")
    print("VECTA CORP HELP DESK EMPLOYEES")
    print("-"*120)
    line_format = "{:5s} {:20s} {:15s} {:20s} {:20s} {:25s} {:15s}"
    print(line_format.format("ID", "Name", "Email", "Date", "Employee", "Solution", "Status"))
    print("-"*120)

    listOfTickets = db.get_open_tickets()
    for ticket in listOfTickets:
        print(line_format.format(str(ticket.ticket_id), ticket.customer_name, ticket.customer_email, str(ticket.submission_date), str(ticket.employee_id), str(ticket.solution_id), ticket.status_id ))
    print("-"*120)

def view_issue(ticketid):
    
    issue = db.get_ticket_issue(ticket_id=ticketid)
    print(f"Issue of ticket {ticketid}: "+issue+"\n"+"")
    

def add_issue():
    status_id = 1
    solution_id = int(input("Solution ID: 1-vProspect 2-vConvert 3-vRetain: "))
    employee = input("Employee ID: ")
    issue_opened = input("What's was customer issue: ")
    cust_name = input("Customer name: ")
    cust_mail = input("Customer email: ")
    date_of_issue = dt.now().strftime("%d/%m/%y")

    ticket_object = Ticket(
        Status_ID=status_id,
        Solution_ID=solution_id,
        Employee_ID=employee,
        Issue=issue_opened,
        Customer_Name=cust_name,
        Customer_Email=cust_mail,
        Submitted_Date=date_of_issue
    )
    db.create_ticket(ticket=ticket_object)
    time.sleep(0.66)
    print("Issue created succesfuly.\n\n")
    

def update_ticket():
    ticket_id = int(input("Ticket ID: "))
    choice = input("Are you sure you want to update this ticket (Y/N): ").lower()
    if choice == 'y':
        status = int(input("Status ID: 1-Open 2-In Progress 3-Closed: "))
        db.update_ticket(statusid=status, ticket_id=ticket_id)
        print("Ticket updated succesfully!\n")
        time.sleep(0.65)
    else:
        print("Ticket NOT updated.\n")

def delete_ticket(ticketid):
    pass

def main():
    db.connect_database()
    while True:
        print ("VECTOR CORP HELPDESK APPLICATION\nLOGIN DETAILS\n\n")
        time.sleep(0.7)
        username = input("Username: ")
        password = input("Password: ")
        if db.login(username=username, password=password):
            print("...Log in successful")
            time.sleep(0.65)
            break
        else:
            print("INVALID CREDENTIAL\n\n")

    display_menu()

    flag = True

    while flag:
        
        command = input("Enter command: ").lower()

        if command == "view":
            time.sleep(1.967)
            view_tickets()
        elif command == "issue":
            t_id = int(input("Ticket ID of Issue: "))
            view_issue(t_id)
        elif command == "add":
            add_issue()
        elif command == "update":
            update_ticket()
        elif command == "del":
            delete_ticket()
        elif command == "exit":
            print("Closing...")
            time.sleep(1.598)
            flag = False
        else:
            print("You have not selected a valid menu. Please try again...\n\n")
            display_menu()


if __name__ == "__main__":
    main()