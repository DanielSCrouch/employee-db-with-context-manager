from sqlite3 import connect

from database.employee import Employee
  
def main() -> None:
  db = 'test.db'
  db = ':memory:'
  with connect(db) as conn:
    e1 = Employee(1001, "John", "Doe", 1000.0, conn)
    e2 = Employee.get_existing_employee(1001, conn) 
    print(e1 == e2) 
    

if __name__ == "__main__":
  main()