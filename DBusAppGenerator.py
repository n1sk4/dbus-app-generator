#!/usr/bin/python3
from DBusAppGeneratorClass import DBusFunctionsGenerator

generator = DBusFunctionsGenerator('functions.json')
file_path = "DBApp.py"

try:
  with open(file_path, 'w') as file:
    file.write(generator.get_source_code())
except Exception as e:
  print(f"Error occoured trying to create a file: {e}")

print("File created successfully:", file_path)