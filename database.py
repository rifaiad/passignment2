from __future__ import print_function, unicode_literals
import mysql.connector
from mysql.connector import errorcode
import PyInquirer
from PyInquirer import style_from_dict, Token, prompt, Separator
from prompt_toolkit.validation import Validator, ValidationError
import pprint
import regex

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

cnx = mysql.connector.connect(user='root',
                                password='root',
                                host='localhost',
                                )
cursor = cnx.cursor()

try:
  autoshop = mysql.connector.connect(user='root',
                                password='root',
                                host='localhost',
                                database='autoshop'
                                )
  print("Database 'autoshop' loaded succesfully!")
except(mysql.connector.errors.ProgrammingError):
  cursor.execute("CREATE DATABASE autoshop")
  autoshop = mysql.connector.connect(user='root',
                                password='root',
                                host='localhost',
                                database='autoshop'
                                )
  print("Database 'autoshop' did not exist and was created.")

atb = autoshop.cursor()
atb.execute("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))")

try:
  atb.execute("CREATE TABLE shops (address TEXT, uid TEXT, type TEXT)")
  print("Table 'shops' created succesfully.")
except(mysql.connector.errors.ProgrammingError):
  print("Table 'shops' loaded succesfully.")

try:
  atb.execute("CREATE TABLE workshops (address TEXT, uid TEXT)")
  print("Table 'workshops' created succesfully.")
except(mysql.connector.errors.ProgrammingError):
  print("Table 'workshops' loaded succesfully.")

try:
  atb.execute("CREATE TABLE products (name TEXT, category TEXT, price INT, uid TEXT)")
  print("Table 'products' created succesfully.")
except(mysql.connector.errors.ProgrammingError):
  print("Table 'products' loaded succesfully.")

try:
  atb.execute("CREATE TABLE orders (date TEXT, price_total INT, uid TEXT, Customeruid TEXT, products TEXT)")
  print("Table 'orders' created succesfully.")
except(mysql.connector.errors.ProgrammingError):
  print("Table 'orders' loaded succesfully.")

try:
  atb.execute("CREATE TABLE customers (name TEXT, uid TEXT)")
  print("Table 'customers' created succesfully.")
except(mysql.connector.errors.ProgrammingError):
  print("Table 'customers' loaded succesfully.")

try:
  atb.execute("CREATE TABLE employees (name TEXT, uid TEXT, date_of_employment TEXT, position TEXT, salary INT, workplace_uid TEXT)")
  print("Table 'employees' created succesfully.")
except(mysql.connector.errors.ProgrammingError):
  print("Table 'employees' loaded succesfully.")

mainmenu = [
    {
        'type': 'list',
        'message': 'Main Menu',
        'name': 'mainmenu',
        'choices': [
            Separator('-- DATABASE OPTIONS --'),

            {
                'name': 'Print data'
            },
            {
                'name': 'Edit data'
            },
            Separator('-- QUICK QUERIES --'),
            {
                'name': 'Retrieve workplace employees'
            },
            {
                'name': 'Retrieve category product list'
            },
            {
                'name': 'List employees by position'
            },
            {
                'name': 'List all of a customer\'s orders'
            },
            {
                'name': 'Search employees by position'
            },
            {
                'name': 'Search products by name'
            },
        ],
        'validate': lambda answer: 'No option has been selected.' \
            if len(answer) == 0 else True
    }
]

printdata = [
    {
        'type': 'list',
        'message': 'Print data',
        'name': 'printdata',
        'choices': [

            {
                'name': 'Print employees'
            },
            {
                'name': 'Print customers'
            },
            {
                'name': 'Print orders'
            },
            {
                'name': 'Print shops'
            },
            {
                'name': 'Print workshops'
            },
            {
                'name': 'Print products'
            },
        ],
        'validate': lambda answer: 'No option has been selected.' \
            if len(answer) == 0 else True
    }
]

editdata = [
    {
        'type': 'list',
        'message': 'Edit data',
        'name': 'editdata',
        'choices': [

            {
                'name': 'Edit employees'
            },
            {
                'name': 'Edit customers'
            },
            {
                'name': 'Edit orders'
            },
            {
                'name': 'Edit shops'
            },
            {
                'name': 'Edit workshops'
            },
            {
                'name': 'Edit products'
            },
        ],
        'validate': lambda answer: 'No option has been selected.' \
            if len(answer) == 0 else True
    }
]

editdata2 = [
    {
        'type': 'list',
        'message': 'Edit data',
        'name': 'editdata2',
        'choices': [

            {
                'name': 'Add entry'
            },
            {
                'name': 'Remove entry'
            },
            {
                'name': 'Edit entry'
            },
        ],
        'validate': lambda answer: 'No option has been selected.' \
            if len(answer) == 0 else True
    }
]

editemployee = [
    {
        'type': 'input',
        'message': 'New position',
        'name': 'newpos',
    },
    {
        'type': 'input',
        'message': 'New salary',
        'name': 'newsal',
    },
    {
        'type': 'input',
        'message': 'New workplace UID',
        'name': 'newwork',
    }
]

editorder = [
    {
        'type': 'input',
        'message': 'New price total',
        'name': 'newprice',
    },
]

editproduct = [
    {
        'type': 'input',
        'message': 'New name',
        'name': 'newname',
    },
    {
        'type': 'input',
        'message': 'New category',
        'name': 'newcategory',
    },
    {
        'type': 'input',
        'message': 'New price',
        'name': 'newprice',
    },
]







while(1):
  print("\n")
  answer1 = prompt(mainmenu, style=style)

  if(answer1["mainmenu"]=='Print data'):
    answer2 = prompt(printdata, style=style)
    if(answer2["printdata"]=='Print employees'):
      atb.execute('SELECT * FROM employees')
      for i in atb.fetchall():
        print(i)
        print("\n")
    elif(answer2["printdata"]=='Print customers'):
      atb.execute('SELECT * FROM customers')
      for i in atb.fetchall():
        print(i)
        print("\n")
    elif(answer2["printdata"]=='Print orders'):
      atb.execute('SELECT * FROM orders')
      for i in atb.fetchall():
        print(i)
        print("\n")
    elif(answer2["printdata"]=='Print shops'):
      atb.execute('SELECT * FROM shops')
      for i in atb.fetchall():
        print(i)
        print("\n")
    elif(answer2["printdata"]=='Print workshops'):
      atb.execute('SELECT * FROM workshops')
      for i in atb.fetchall():
        print(i)
        print("\n")
    elif(answer2["printdata"]=='Print products'):
      atb.execute('SELECT * FROM products')
      for i in atb.fetchall():
        print(i)
        print("\n")

        

  elif(answer1["mainmenu"]=='Edit data'):
    answer2 = prompt(editdata, style=style)
    if(answer2["editdata"]=='Edit employees'):
      answer3 = prompt(editdata2, style=style)
      print(answer3)
      if(answer3["editdata2"]=='Add entry'):
        name = input("Insert employee name: ")
        uid = input("Insert employee uid: ")
        doe = input("Insert date of employment (dd.mm.yy): ")
        pos = input("Insert employee position: ")
        sal = input("Insert employee salary per month: ")
        work = input("Insert the UID of the employee's workplace: ")
        val = (name, uid, doe, pos, sal, work)
        atb.execute("INSERT INTO employees (name, uid, date_of_employment, position, salary, workplace_uid) VALUES (%s, %s, %s, %s, %s, %s)", val)
        autoshop.commit()
      elif(answer3["editdata2"]=='Remove entry'):
        uid = input("Insert the uid of the employee to delete: ")
        atb.execute("DELETE FROM employees WHERE uid = '%s'" % uid)
        autoshop.commit()
        print(atb.rowcount, "employee(s) has(have) been removed.")
      elif(answer3["editdata2"]=='Edit entry'):
        uid = input("Insert the uid of the employee to edit: ")
        answer4 = prompt(editemployee, style=style)
        val = (answer4["newpos"], uid)
        atb.execute("UPDATE employees SET position = '%s' WHERE uid = '%s'" % val)
        autoshop.commit()
        val = (answer4["newsal"], uid)
        atb.execute("UPDATE employees SET salary = '%s' WHERE uid = '%s'" % val)
        autoshop.commit()
        val = (answer4["newwork"], uid)
        atb.execute("UPDATE employees SET workplace_uid = '%s' WHERE uid = '%s'" % val)
        autoshop.commit()
    elif(answer2["editdata"]=='Edit customers'):
      answer3 = prompt(editdata2, style=style)
      print(answer3)
      if(answer3["editdata2"]=='Add entry'):
        name = input("Insert customer name: ")
        uid = input("Insert customer uid: ")
        val = (name, uid)
        atb.execute("INSERT INTO customers (name, uid) VALUES (%s, %s)", val)
        autoshop.commit()
      elif(answer3["editdata2"]=='Remove entry'):
        uid = input("Insert the uid of the customer to delete: ")
        atb.execute("DELETE FROM customers WHERE uid = '%s'" % uid)
        autoshop.commit()
        print(atb.rowcount, "customer(s) has(have) been removed.")
      elif(answer3["editdata2"]=='Edit entry'):
        print("Editing customers is not yet supported.")
    elif(answer2["editdata"]=='Edit orders'):
      answer3 = prompt(editdata2, style=style)
      print(answer3)
      if(answer3["editdata2"]=='Add entry'):
        date = input("Insert order date: ")
        price = input("Insert the order total: ")
        uid = input("Insert order UID: ")
        cuid = input("Insert the customer's UID: ")
        products = input("Insert the order's products in the following format (product1UID, number);(product2UID, number): ")
        val = (date, price, uid, cuid, products)
        atb.execute("INSERT INTO orders (date, price_total, UID, CustomerUID, products) VALUES (%s, %s, %s, %s, %s)", val)
        autoshop.commit()
      elif(answer3["editdata2"]=='Remove entry'):
        uid = input("Insert the uid of the order to delete: ")
        atb.execute("DELETE FROM orders WHERE uid = '%s'" % uid)
        autoshop.commit()
        print(atb.rowcount, "order(s) has(have) been removed.")
      elif(answer3["editdata2"]=='Edit entry'):
        uid = input("Insert the uid of the order to edit: ")
        answer4 = prompt(editorder, style=style)
        val = (answer4["newprice"], uid)
        atb.execute("UPDATE orders SET price_total = '%s' WHERE uid = '%s'" % val)
        autoshop.commit()
    elif(answer2["editdata"]=='Edit shops'):
      answer3 = prompt(editdata2, style=style)
      print(answer3)
      if(answer3["editdata2"]=='Add entry'):
        address = input("Insert shop address: ")
        uid = input("Insert the shop's UID: ")
        stype = input("Insert shop's type: ")
        val = (address, uid, stype)
        atb.execute("INSERT INTO shops (address, UID, type) VALUES (%s, %s, %s)", val)
        autoshop.commit()
      elif(answer3["editdata2"]=='Remove entry'):
        uid = input("Insert the uid of the shop to delete: ")
        atb.execute("DELETE FROM shops WHERE uid = '%s'" % uid)
        autoshop.commit()
        print(atb.rowcount, "shop(s) has(have) been removed.")
      elif(answer3["editdata2"]=='Edit entry'):
        print("Editing shops not yet implemented.")
    elif(answer2["editdata"]=='Edit workshops'):
      answer3 = prompt(editdata2, style=style)
      print(answer3)
      if(answer3["editdata2"]=='Add entry'):
        address = input("Insert workshop address: ")
        uid = input("Insert the workshop's UID: ")
        val = (address, uid)
        atb.execute("INSERT INTO workshops (address, UID) VALUES (%s, %s)", val)
        autoshop.commit()
      elif(answer3["editdata2"]=='Remove entry'):
        uid = input("Insert the uid of the workshop to delete: ")
        atb.execute("DELETE FROM workshops WHERE uid = '%s'" % uid)
        autoshop.commit()
        print(atb.rowcount, "workshop(s) has(have) been removed.")
      elif(answer3["editdata2"]=='Edit entry'):
        print("Editing workshops not yet implemented.")
    elif(answer2["editdata"]=='Edit products'):
      answer3 = prompt(editdata2, style=style)
      print(answer3)
      if(answer3["editdata2"]=='Add entry'):
        name = input("Insert the product's name: ")
        category = input("Insert the product category: ")
        price = input("Insert the product's price: ")
        uid = input("Insert the product's UID: ")
        val = (name, category, price, uid)
        atb.execute("INSERT INTO products (name, category, price, uid) VALUES (%s, %s, %s, %s)", val)
        autoshop.commit()
      elif(answer3["editdata2"]=='Remove entry'):
        uid = input("Insert the uid of the product to delete: ")
        atb.execute("DELETE FROM products WHERE uid = '%s'" % uid)
        autoshop.commit()
        print(atb.rowcount, "product(s) has(have) been removed.")
      elif(answer3["editdata2"]=='Edit entry'):
        uid = input("Insert the uid of the order to edit: ")
        answer4 = prompt(editproduct, style=style)
        val = (answer4["newname"], uid)
        atb.execute("UPDATE products SET name = '%s' WHERE uid = '%s'" % val)
        autoshop.commit()
        val = (answer4["newname"], uid)
        atb.execute("UPDATE products SET name = '%s' WHERE uid = '%s'" % val)
        autoshop.commit()
        val = (answer4["newcategory"], uid)
        atb.execute("UPDATE products SET category = '%s' WHERE uid = '%s'" % val)
        autoshop.commit()
        val = (answer4["newprice"], uid)
        atb.execute("UPDATE products SET price = '%s' WHERE uid = '%s'" % val)
        autoshop.commit()
  elif(answer1["mainmenu"]=='Retrieve workplace employees'):
    eUID = input("Please insert the UID of the shop/workshop in question: ")
    atb.execute('SELECT employees.name, employees.uid FROM employees INNER JOIN shops ON employees.workplace_uid = "%s"' % eUID)
    for i in atb.fetchall():
      print(i)
  elif(answer1["mainmenu"]=='Retrieve category product list'):
    cat = input("Please insert the category you want to print the contents of: ")
    val = (cat, cat)
    atb.execute("CREATE OR REPLACE VIEW %s_Products AS SELECT * FROM products WHERE category = '%s'" % val)
    atb.execute("SELECT * FROM %s_Products" %cat)
    for i in atb.fetchall():
      print(i)
  elif(answer1["mainmenu"]=='List all of a customer\'s orders'):
    cui = input("Insert the UID of the customer in question: ")
    atb.execute("SELECT * FROM orders WHERE orders.customeruid = '%s'" %cui)
    for i in atb.fetchall():
      print(i)
  elif(answer1["mainmenu"]=='Search employees by position'):
    search = input("Insert the position in question: ")
    search = "%" + search + "%"
    atb.execute("SELECT * FROM `employees` WHERE position LIKE '%s'" %search)
    for i in atb.fetchall():
      print(i)

  elif(answer1["mainmenu"]=='Search products by name'):
    search = input("Insert a manufacturer, type or name with which to search for products: ")
    search = "%" + search + "%"
    atb.execute("SELECT * FROM `products` WHERE name LIKE '%s'" %search)
    for i in atb.fetchall():
      print(i)

      







