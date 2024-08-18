import mysql.connector, os, sys
os.system('cls')

def db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='goodgames'
        )
        print("Connection to database successful")
        return connection
    except mysql.connector.Error:
        print("Error")
        return None
    
def clear_terminal():
    os.system('cls')

def show_menu():
    print("[1] Log In. ")
    print("[2] Create a new account. ")
    print("[3] Exit. ")

    option = int(input("Select an option. "))
    return option

def login(connection):
    clear_terminal()

    while True:

        try:
            cursor = connection.cursor()
            
            print("////////// LOG IN ///////////")

            #Introduce your email and password
            email = input("Email: ")
            password = input("Password: ")

            #Checks if your info is on the database
            check_sql = "SELECT email, password FROM users WHERE email = %s AND password = %s"
            cursor.execute(check_sql, (email, password))
            check_results = cursor.fetchall()

            #Logs you in 
            if check_results:
                name_sql = "SELECT name FROM users WHERE email = %s AND password = %s"
                cursor.execute(name_sql, (email, password))
                name = cursor.fetchall()
                print("Welcome, ", name)
            else:
                print("This account doesn't exist. Please try again.")
                login()

        except mysql.connector.Error as err:
            print("Error, err")
        finally: 
            cursor.close()
            break

def register(connection):
    clear_terminal()

    while True:

        try:
            cursor = connection.cursor()

            #Introduce your data
            print("///////// SIGN UP ///////////")
            name = input("Name: ")
            date_of_birth = input("Date of Birth(YYYY-MM-DD): ")
            email = input("Email: ")
            password = input("Password: ")

            #Checks if the email already exists in the database
            check_if_email_exists_sql = "SELECT email FROM users WHERE email = %s"
            cursor.execute(check_if_email_exists_sql, (email,))
            checking_result = cursor.fetchall()
            
            #If there is not an account with that email, it creates a new account
            if not checking_result:
                register_sql = "INSERT INTO users (name, date_of_birth, email, password) VALUES (%s, %s, %s, %s)"
                cursor.execute(register_sql, (name, date_of_birth, email, password))
                connection.commit()
                print("You've created a new account successfully")

            else:
                print("There was an error with your registration. Please try again.")


        except mysql.connector.Error as err:
            print("Error, err")
        finally: 
            cursor.close()
            break

def main():
    connection = db_connection()
    if not connection:
        return
    option = show_menu()
    
    if option == 1:
        login(connection)
    elif option == 2:
        register(connection)
    elif option == 3:
        sys.exit()
    else:
        print("Select a valid option. ")
        show_menu()

    connection.close()

if __name__ == "__main__":
    main()