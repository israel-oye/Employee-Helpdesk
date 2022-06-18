from time import strftime
import pymysql
from contextlib import closing
from ticket_object import Ticket
from datetime import datetime as dt


connection = None

def connect_database():
    global connection

    SERVER = "127.0.0.1"
    DB_NAME = "vc helpdesk"
    USERNAME = "root"
    PWD = ""

    if not connection:
        connection = pymysql.connect(
            host=SERVER,
            database=DB_NAME,
            user=USERNAME,
            password=PWD,
            autocommit=True
        )

def close_connection():
    if connection:
        connection.close()

def reset_auto_inc():
    query_1 = "SET @count :=0;"
    query_2 = "UPDATE tickets SET ticketid = @count := (@count+1) ;"
    query_3 = "ALTER TABLE tickets AUTO_INCREMENT = 1;"

    connect_database()
    with closing(connection.cursor()) as cursor:
        cursor.execute(query_1)
        cursor.execute(query_2)
        cursor.execute(query_3)

def create_ticket(ticket):
    reset_auto_inc()

    query = "INSERT INTO tickets (statusid, solutionid, employeeid, issue, customername, customeremail, submitteddate)\
             VALUES(%s, %s, %s, %s, %s, %s, %s);"

    with closing(connection.cursor()) as cursor:
        cursor.execute(query, (ticket.status_id, ticket.solution_id, ticket.employee_id, ticket.issue, ticket.customer_name, ticket.customer_email, ticket.submission_date))

def make_ticket(row):
    date = row[7]
    return Ticket(
        Ticket_ID=row[0],
        Status_ID=row[1],
        Solution_ID=row[2],
        Employee_ID=row[3],
        Issue=row[4],
        Customer_Name=row[5],
        Customer_Email=row[6],
        Submitted_Date=date.strftime("%y/%m/%d")
    )

def get_open_tickets():
    reset_auto_inc()

    query = ("SELECT tickets.ticketid, status.status, solutions.solution, employees.name AS employee, "+
             "tickets.issue, tickets.customername, tickets.customeremail, tickets.submitteddate "+
             "FROM employees INNER JOIN "+
             "tickets ON employees.employeeid = tickets.employeeid INNER JOIN "+
             "solutions ON tickets.solutionid = solutions.solutionid INNER JOIN "+
             "status ON tickets.statusid = status.statusid "+
             "WHERE tickets.statusid=1 OR tickets.statusid=2 "+
             "ORDER BY tickets.ticketid;"
            )

    

    with closing(connection.cursor()) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        Tickets = []
        for ticket in rows:
            Tickets.append(make_ticket(row=ticket))
        return Tickets
        
def get_open_ticket(ticket_id):
    query = "SELECT * FROM tickets WHERE ticketid = %s;"

    with closing(connection.cursor()) as cursor:
        cursor.execute(query, (ticket_id,))
        row = cursor.fetchone()
        ticket = make_ticket(row)
    return ticket

def get_ticket_issue(ticket_id):
    reset_auto_inc()

    query = "SELECT issue FROM tickets WHERE ticketid = %s"

    with closing(connection.cursor()) as cursor:
        cursor.execute(query, (ticket_id))
        issue = str(cursor.fetchone()[0])
        
    return issue

def update_ticket(statusid, ticket_id):
    query = "UPDATE tickets SET statusid = %s WHERE ticketid = %s"

    with closing(connection.cursor()) as cursor:
        cursor.execute(query, (statusid, ticket_id))

def login(username, password):
    query = "SELECT COUNT(*) FROM employees WHERE username = %s AND password = %s;"

    with closing(connection.cursor()) as cursor:
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result[0] > 0:
            return True
        else:
            return False

