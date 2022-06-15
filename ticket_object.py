
class Ticket():
    

    def __init__(self, Ticket_ID=0, Status_ID=0, Solution_ID=0, Employee_ID=None, Issue=None, Customer_Name=None, Customer_Email=None, Submitted_Date=None) -> None:
        self.ticket_id = Ticket_ID
        self.status_id = Status_ID
        self.solution_id = Solution_ID
        self.employee_id = Employee_ID
        self.issue = Issue
        self.customer_name = Customer_Name
        self.customer_email = Customer_Email
        self.submission_date = Submitted_Date