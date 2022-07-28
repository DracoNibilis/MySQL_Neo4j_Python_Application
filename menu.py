# import of needed libraries
import connect_to_MySQL_Neo4j
import datetime

# define main function
def main():
    
    # display choice
    while True:
        display_menu()
        choice = input("Choice: ")
        
        # exit menu / terminate program
        if (choice == "x"):
            break
            
        #  MENU - 1 - View Employees & Departments
        elif (choice == "1"):
            employees = connect_to_MySQL_Neo4j.choice_one()

          
        # MENU - 2 - View Salary Details    
        elif  (choice == "2"):
            def get_id():
                return input("Enter EID: ")
            eid = get_id()
                
            employee = connect_to_MySQL_Neo4j.choice_two(eid)
            print("salary Details for Employee: ", eid)
            print()
            
            for e in employee:
                print("Minimum","|", "Average","|", "Maximum")
                print(e["Minimum"],"|", e["Average"],"|", e["Maximum"])
                
        # MENU - 3 - View by Month
        elif (choice == "3"):
            month_name = input("Enter month: ")
            
            def get_month(month_name):
                #month_name = input("month name/ number: ")
                try:
                    month_name = int(month_name)
                    if month_name in range(1,13):
                        month = month_name
                        #return month
                        #print("correct month number", month)
                    #else:
                except UnboundLocalError:
                    print("unbound local error")
                    #month_name = input("Enter month: ")
                except SyntaxError:
                    print(" SYNTAX error becouse not number.....")  
                    #month_name = input("Enter month: ")


                    try:
                        month_name = str(month_name)
                        month_name.lower()
                        datetime_object = datetime.datetime.strptime(month_name, "%b")
                        month = datetime_object.month
                        
                        #return month
                        #print("changed month", month)
                    except Exception as e:
                        print("ERROR OCCUR")
                        #month_name = input("Enter month: ")
                #print("returned element is: ", month, type(month))
                #return month
                except Exception:
                    print("exception error .....")  
                    #month_name = input("Enter month: ")
                return month
            month = get_month(month_name)
            #month = str(month)

            by_date = connect_to_MySQL_Neo4j.choice_three(month)
            for d in by_date:
                print(d["eid"], "|", d["name"], "|", d["dob"])
                

            
        # MENU - 4 - Add New Employee    
        elif (choice == "4"):
            print("Add emplyees")
            eid = input("EID : ")
            name = input("Name : ")
            dob = input("DOB : ")
            did = input("Dept ID : ")
            connect_to_MySQL_Neo4j.choice_four(eid, name, dob, did)
        
        # MENU - 5 - View Departments Managed by Employee
        elif (choice == "5"):
            def get_id():
                return input("Enter EID: ")

            eid = get_id()
            dept = connect_to_MySQL_Neo4j.choice_five(eid)
        
        # MENU - 6 - Add Manager to Department        
        elif (choice == "6"):
            def get_id():
                return input("Enter EID: ")
            def get_dep():
                return input("Enter Department: ")
                
            eid = get_id()
            did = get_dep()
            connect_to_MySQL_Neo4j.choice_six(eid, did)
            
        # MENU - 7 - View Departments    
        elif (choice == "7"):
            dept = connect_to_MySQL_Neo4j.choice_seven()
            #print(dept)
            for d in dept:
                print(d["Did"], "|", d["Name"], "|", d["Location"], "|", d["Budget"])

# menu display
def display_menu():
    print()
    print("- - - - ")
    print("Empolyees")
    print("---------")
    print()
    print("MENU")
    print("====")
    print("1 - View Employees & Departments")
    print("2 - View Salary Details")
    print("3 - View by Month of Birth")
    print("4 - Add New Employee")
    print("5 - View Departments managed by Employee")
    print("6 - Add Manager to Department")
    print("7 - View Departments")
    print("x - Exit application")
    

    
    
    
if __name__ == "__main__":
    main()