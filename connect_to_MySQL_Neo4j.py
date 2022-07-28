# Import of needed libraries
import pymysql
from neo4j import GraphDatabase

conn = None

# define function for sql query - 1st choice in the menu
def choice_one():
    conn = pymysql.connect(host="localhost", user="root", password="root", db="employees", cursorclass=pymysql.cursors.DictCursor)
    if (not conn):
        connect()
    
    # SQL query 
    query = "select name, did from employee order by name"
    
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        input_q = input("press q to quit")
        while input_q != "q":
            z = cursor.fetchmany(size=2)
            for el in z:
                print(el.get("name"), " | ", el.get("did"))
            input_q = input("press q to quit   ")

# define function for sql query - 2nd choice in the menu
def choice_two(eid):
    conn = pymysql.connect(host="localhost", user="root", password="root", db="employees", cursorclass=pymysql.cursors.DictCursor)
    if (not conn):
        connect()
        
    # SQL query
    query = '''select employee.eid, 
               format(max(salary.salary),2) AS Maximum,
               format(avg(salary.salary),2) AS Average, 
               format(min(salary.salary),2) AS Minimum 
               from employee 
               inner join salary 
                on employee.eid = salary.eid 
               where employee.eid = %s'''
    
    with conn: 
        cursor = conn.cursor()
        cursor.execute(query, (eid))
        x = cursor.fetchall()
        return x

# define function for sql query - 3rd choice in the menu
def choice_three(month):
    conn = pymysql.connect(host="localhost", user="root", password="root", db="employees", cursorclass=pymysql.cursors.DictCursor)
    if (not conn):
        connect()
        
    query = "select eid, name, dob from employee where month(dob) = %s"
    
    with conn:
        #try:
        cursor = conn.cursor()
        cursor.execute(query, (month))
        x = cursor.fetchall()
        #print(x)
        return x

# define function for sql query - 4th choice in the menu
def choice_four(eid, name, dob, did):
    conn = pymysql.connect(host="localhost", user="root", password="root", db="employees", cursorclass=pymysql.cursors.DictCursor)
    
    if (not conn):
        connect()
    
    # query for SQL
    query = "INSERT INTO employee VALUES (%s, %s, %s, %s)"
    
    with conn:
        
        try:    
            cursor = conn.cursor()
            cursor.execute(query,(eid, name, dob, did))
            print("Employee Added Successfully")
        except pymysql.err.IntegrityError:
            print(eid," ID Already Existing or, ", did, " DID is Invalid")
        except pymysql.err.OperationalError:
            print("Invalid Date of Birth")

driver = None

def connect():
    global driver
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"), max_connection_lifetime=1000)

# define function for sql/cypher query - 5th choice in the menu   
def get_department(tx,eid):
    
    # Cypher query
    query = "MATCH (d:Department)<-[:MANAGES]-(e:Employee) WHERE e.eid = $eid RETURN d.did"
    
    departments = []
    results = tx.run(query, eid=eid)
    for result in results:
        #print(result)
        departments.append(result["d.did"])
    #print("departments list  ", departments)
    return departments
    
    
def choice_five(eid):
    connect()
    #user_id = input("Enter ID: ")
    with driver.session() as session:
        values = session.read_transaction(get_department, eid)
        print("Departments Managed by: ", eid)
        print("Departments", " | ", "Budget") 

    for value in values:
        conn = pymysql.connect(host="localhost", user="root", password="root", db="employees", cursorclass=pymysql.cursors.DictCursor)
        if (not conn):
            connect()
        
        query = "SELECT did, budget from dept where did= %s"

        with conn:
            #try:
            cursor = conn.cursor()
            cursor.execute(query, (value))
            x = cursor.fetchall()
            for e in x:
                print(e.get("did"), " | ", e.get("budget"))
        
       
# define function for cypher query - 6th choice in the menu   
def add_rel(tx, eid, did):

        # cypher query
        query = "CREATE p = (e:Employee{eid:$eid})-[:MANAGES]->(d:Department{did:$did}) RETURN p"
        tx.run(query, eid=eid, did=did)

# define function for sql/cypher query - 6th choice in the menu         
def choice_six(eid,did):
    connect()
    with driver.session() as session:
        rel_nodes = session.write_transaction(add_rel,eid,did)
        print("Relation created between: ", eid, "AND", did)
        
    return
    
    
# define function for sql query - 7th choice in the menu 
def choice_seven():
    
    # connection
    conn = pymysql.connect(host="localhost", user="root", password="root", db="employees", cursorclass=pymysql.cursors.DictCursor)
    if (not conn):
        connect()
    
    # SQL query 
    query = "select dept.did as Did, dept.name as Name, dept.lid as Location, dept.budget as Budget from dept"
    
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        x = cursor.fetchall()
        
        return x
    # lack of one time reading from database...   