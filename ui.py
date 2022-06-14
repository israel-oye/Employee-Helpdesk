import db, time
from objects import Employee

def authorize():
    db.connect_database()

    email = input("Enter email: ").lower()
    password = input("Enter your password: ")
    admin_found = False

    all_admins = db.get_admins()

    for employee in all_admins:
        # print(employee.name, employee.password)
        if employee.email == email and employee.password == password:
            admin_found = True

    db.close_connection()

    if admin_found:
        return True
    else:
        print("YOU ARE NOT AUTHORIZED!")
        return False
    

def display_menu():
    
    print("Vecta Corp Help Desk Apllication (Admin)\n\
        COMMAND VIEW\n\
            --------------------------------\n\
            view - View all employees\n\
            add - Add an employee\n\
            del - Delete an employee\n\
            exit - Exit the application.\n\
            --------------------------------")

def view_employees():
    print("")
    print("VECTA CORP HELP DESK EMPLOYEES")
    print("-"*120)
    line_format = "{:5s} {:15s} {:15s} {:20s} {:40s} {:15s} {:15s}"
    print(line_format.format("ID", "Name", "Username", "Password", "Email", "Role", "Salary"))
    print("-"*120)
    
    listOfEmployees = db.get_employees()
    for employee in listOfEmployees:
        print(line_format.format(str(employee.employee_id), employee.name, employee.username, employee.password, employee.email, employee.role, str(employee.salary))) 
    print("-"*120)

def add_employee():
    employee_name = input("Enter name: ")
    employee_uname = input("Enter username: ")
    employee_password = input("Enter password: ")
    employee_mail = input("Enter email address: ")
    employee_role_id = int(input("Enter role id. 1:Support, 2:Administration, 3:Developer, 4:Admin: "))
    employee_salary = int(input("Enter salary:$ "))

    employee_obj = Employee(name=employee_name, username=employee_uname, password=employee_password, email=employee_mail, role_id=employee_role_id, salary=employee_salary)
    db.create_employee(employee=employee_obj)
    print("Employee created succesfuly.\n\n")

def delete_employee():
    emp_id = int(input("Enter employee id of record to be deleted: "))
    employee = db.get_employee(emp_id)
    final_decision = input(f"Are you sure you want to delete {employee.name}'s record, Y or N: ")
    
    if final_decision == 'Y':
        db.delete_employee(emp_id)
        print("Record deleted sucessfully.\n\n")
    else:
        print('\n\n')
        display_menu()

def main():
    db.connect_database()
    display_menu()
    flag = True

    while flag:
        
        command = input("Enter command: ").lower()

        if command == "view":
            time.sleep(1.967)
            view_employees()
        elif command == "add":
            add_employee()
        elif command == "del":
            delete_employee()
        elif command == "exit":
            flag = False
        else:
            print("You have not selected a valid menu. Please try again...\n\n")
            display_menu()

    db.close_connection()
    print("The program has been terminated.")

if __name__ == "__main__":
    # if authorize():
    #     pass
    main()
