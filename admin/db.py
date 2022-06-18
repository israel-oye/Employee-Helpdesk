import pymysql
from contextlib import closing
from admin.objects import Employee

conn = None


def connect_database():
    global conn

    SERVER = "127.0.0.1"
    DB_NAME = "vc helpdesk"
    USERNAME = "root"
    PWD = ""

    if not conn:
        conn = pymysql.connect(
            host=SERVER,
            user=USERNAME,
            password=PWD,
            database=DB_NAME,
            autocommit=True,
        )
    

def close_connection():
    
    if conn:
        conn.close()

def reset_auto_inc():
    auto_inc_reset_query_1 = "SET @num := 0;"
    auto_inc_reset_query_2 = "UPDATE employees SET employeeid = @num := (@num+1);"
    auto_inc_reset_query_3 = "ALTER TABLE employees AUTO_INCREMENT = 1;"

    connect_database()
    with closing(conn.cursor()) as cursor:
        cursor.execute(auto_inc_reset_query_1)
        cursor.execute(auto_inc_reset_query_2)
        cursor.execute(auto_inc_reset_query_3)

def make_employee(row):
    return Employee(
        employee_id=row[0],
        name=row[1],
        username=row[2],
        password=row[3],
        email=row[4],
        role_id=row[5],
        salary=row[6],
        employee_role=row[5]

        )

def get_employees():
    
    reset_auto_inc()
    
    query = "SELECT employeeid, name, username, password, email, role, salary FROM employees INNER JOIN roles ON employees.roleid = roles.roleid;"
    
    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    employees = []
    for row in result:
        employees.append(make_employee(row))

    
    return employees


def get_employee(employee_id):
    reset_auto_inc()
    query = f"SELECT employeeid, name, username, password, email, role, salary FROM employees INNER JOIN roles ON employees.roleid = roles.roleid WHERE employeeid = {employee_id}"

    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

        requested_employee = make_employee(result)

    return requested_employee


def create_employee(employee):
    reset_auto_inc()
    query = "INSERT INTO employees (name, username, password, email, roleid, salary)\
             VALUES(%s, %s, %s, %s, %s, %s);"

    with closing(conn.cursor()) as cursor:
        cursor.execute(query, (employee.name, employee.username, employee.password, employee.email, employee.role_id, employee.salary))
        


def delete_employee(employee_id):
    
    query = f"DELETE FROM employees WHERE employeeid = {employee_id}"

    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
    reset_auto_inc()

def get_employee_roles():
    '''Gets employees with their roles'''

    query = "SELECT * FROM employee-roles;"

    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
        all_employee_roles = cursor.fetchall()

    return all_employee_roles

def get_admins():
    reset_auto_inc()
    query = f"SELECT * FROM employees WHERE roleid = 4;"

    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

        admins = []
        for row in result:
            admins.append(make_employee(row=row))
        
    return admins

def login(username, password, role_id):
    query = "SELECT COUNT(*) FROM employees WHERE username = %s AND password = %s AND roleid = %s;"

    with closing(conn.cursor()) as cursor:
        cursor.execute(query, (username, password, role_id))
        result = cursor.fetchone()

        if result[0] > 0:
            return True
        else:
            return False




