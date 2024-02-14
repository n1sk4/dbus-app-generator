#!/usr/bin/python3
from DBusAppGeneratorClass import DBusFunctionsGenerator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("Interfaces", nargs="*", help="List of D-Bus interfaces")
parser.add_argument("-f", "--output_file", help="Output file; i.e. 'DBApp.py'")
parser.add_argument("-j", "--json_file", help="JSON file, i.e. 'functions.json")
args = parser.parse_args()

interfaces = args.Interfaces
print(f"{interfaces}")
output_file = args.output_file or "DBApp.py"
json_file = args.json_file or 'functions.json'

generator = DBusFunctionsGenerator(json_file, interfaces)

try:
  with open(output_file, 'w') as file:
    file.write(generator.get_source_code())
except Exception as e:
  print(f"Error occoured trying to create a file: {e}")
  exit()

print("File created successfully:", output_file)