from typing import ContextManager
import unittest
from sqlite3 import connect

from .employee import temporary_employee


class TestEmployee(unittest.TestCase):

  conn = connect(':memory:')

  def test_create_employee(self):
    with temporary_employee(1001, "John", "Doe", 1000.0, self.conn) as e1:
      self.assertEqual(e1.first_name, "John")
      self.assertEqual(e1.last_name, "Doe") 
      self.assertEqual(e1.pay, 1000.0)

  def test_employee_email(self):
    with temporary_employee(1001, "John", "Doe", 1000.0, self.conn) as e1:
      self.assertEqual(e1.email, "John.Doe@email.com")

  def test_employee_fullname(self):
    with temporary_employee(1001, "John", "Doe", 1000.0, self.conn) as e1:
      self.assertEqual(e1.fullname, "John Doe")

  def test_update_employee_first_name(self):
    with temporary_employee(1001, "John", "Doe", 1000.0, self.conn) as e1:
      e1.first_name = "Jill"
      self.assertEqual(e1.first_name, "Jill")

  def test_update_employee_last_name(self):
    with temporary_employee(1001, "John", "Doe", 1000.0, self.conn) as e1:
      e1.last_name = "Voe"
      self.assertEqual(e1.last_name, "Voe")

  def test_update_employee_pay(self):
    with temporary_employee(1001, "John", "Doe", 1000.0, self.conn) as e1:
      e1.pay = 2000.1
      self.assertEqual(e1.pay, 2000.1)


if __name__ == "__main__":
  unittest.main() 
