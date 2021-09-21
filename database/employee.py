from sqlite3 import Connection, IntegrityError
from contextlib import contextmanager

class Employee(object):
  """An Employee class providing a persistant database backed state"""
  table_name = "employee" 

  def __init__(self, id: int, first_name: str, last_name: str, pay: float, db_conn: Connection):
    self.id = id
    self.conn = db_conn

    self.ensure_db_table_exists()
    self.initialise_db_record(first_name, last_name, pay)

  @staticmethod
  def get_existing_employee(id: int, db_conn: Connection) -> object:
    """Returns a employee from the database, specified by employee's unique ID"""
    record_map = Employee.get_as_dict(id, db_conn)
    return Employee(record_map["id"], record_map["first_name"], record_map["last_name"], record_map["pay"], db_conn)

  @staticmethod
  def get_as_dict(id: int, db_conn: Connection) -> dict:
    """Returns an employee with given ID, in dictionary representation"""
    with db_conn:

      cur = db_conn.cursor()
      sql = f"""SELECT * FROM employee 
                WHERE id=:id
                """
      cur.execute(sql, {"id": id})
      record = cur.fetchone()
      # map column names to values
      col_names = [description[0] for description in cur.description]
      record_map = {col_names[i]: record[i] for i in range(len(record))}

      return record_map

  def ensure_db_table_exists(self) -> None:
    """Ensures 'employee' table exists. Runs during class initalisation"""
    with self.conn:
      cur = self.conn.cursor()
      sql = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INT NOT NULL PRIMARY KEY,
                first_name TEXT,
                last_name TEXT, 
                pay REAL
                )"""
      cur.execute(sql)

  def initialise_db_record(self, first_name: str, last_name: str, pay: int) -> None:
    """Initialises Employee record in database. Runs during class initialisation"""
    with self.conn:
      cur = self.conn.cursor() 
      sql = f"""INSERT INTO employee 
                VALUES (:id, :first_name, :last_name, :pay
                )"""
      try:
        cur.execute(sql, {"id": self.id, "first_name": first_name, "last_name": last_name, "pay": pay}) 
      except IntegrityError as e:
        record_map = Employee.get_as_dict(self.id, self.conn)
        # identical record
        if record_map["first_name"] == first_name and record_map["last_name"] == last_name and record_map["pay"] == pay:
          return
        raise e 

  @property
  def first_name(self):
    """Return the employee's first name"""
    cur = self.conn.cursor() 
    sql = f"""SELECT first_name FROM employee 
              WHERE id=:id
              """
    cur.execute(sql, {"id": self.id})
    name = cur.fetchone()[0]
    return name

  @first_name.setter
  def first_name(self, value: str):
    """Set employee's first name"""
    with self.conn:
      cur = self.conn.cursor() 
      sql = f"""UPDATE employee SET first_name = :first_name
                WHERE id=:id
                """
      cur.execute(sql, {"first_name": value, "id": self.id}) 

  @property
  def last_name(self):
    """Return the employee's last name"""
    cur = self.conn.cursor() 
    sql = f"""SELECT last_name FROM employee 
              WHERE id=:id
              """
    cur.execute(sql, {"id": self.id})
    name = cur.fetchone()[0]
    return name

  @last_name.setter
  def last_name(self, value: str):
    """Set employee's last name"""
    with self.conn:
      cur = self.conn.cursor() 
      sql = f"""UPDATE employee SET last_name = :last_name
                WHERE id=:id
                """
      cur.execute(sql, {"last_name": value, "id": self.id}) 

  @property
  def pay(self):
    """Get employee's pay"""
    cur = self.conn.cursor() 
    sql = f"""SELECT pay FROM employee 
              WHERE id=:id
              """
    cur.execute(sql, {"id": self.id})
    name = cur.fetchone()[0]
    return name
  
  @pay.setter
  def pay(self, value: float):
    """Set employee's pay"""
    with self.conn:
      cur = self.conn.cursor() 
      sql = f"""UPDATE employee SET pay = :pay
                WHERE id=:id
                """
      cur.execute(sql, {"pay": value, "id": self.id}) 
      
  @property
  def email(self):
    """Return employee's email address"""
    return f'{self.first_name}.{self.last_name}@email.com'

  @property 
  def fullname(self):
    """Return employee's full name"""
    return f'{self.first_name} {self.last_name}'

  def delete(self):
    """Delete employee from database"""
    with self.conn:
      cur = self.conn.cursor() 
      sql = f"""DELETE FROM employee
                WHERE id=:id
                """
      cur.execute(sql, {"id": self.id}) 

  def __repr__(self):
    return f'Employee("{self.first_name}", "{self.last_name}", {self.pay})'

  def __eq__(self, o: object) -> bool:
    if not isinstance(o, Employee):
      return False
    if o.id == self.id and o.first_name == self.first_name and o.last_name == self.last_name and o.pay == self.pay:
      return True
    return False


@contextmanager
def temporary_employee(id, first_name, last_name, pay, db_conn):
  """
  Returns an employee instance where the database representatioon lives only 
  for the lifetime of the objects initialisation
  """
  e = Employee(id, first_name, last_name, pay, db_conn)
  try:
    yield e
  finally:
    e.delete()