#!/usr/bin/python3
import json

# Before running DBApp.py install:
# * DBus Python library: 'sudo apt install -y python3-dbus'
# * GI (GObject Introspection) Python library: 'sudo apt install python3-gi'

# Data types for D-Bus: https://dbus.freedesktop.org/doc/dbus-specification.html

class DBusFunctionsGenerator():
    def __init__(self, json_file=None, executor= "#!/usr/bin/python3"):
      # Run 'which python3' to check the correct path for the first line #!/{path_to_python3}/python3
      self.linux_executor = executor
      self.data_type_map = {
          "byte"        : "y",
          "boolean"     : "b",
          "int16"       : "n",
          "uint16"      : "q",
          "int32"       : "i",
          "int"         : "i",
          "uint32"      : "u",
          "uint"        : "u",
          "int64"       : "t",
          "double"      : "d",
          "unix_fd"     : "h",
          "string"      : "s",
          "object"      : "o",
          "object_path" : "o",
          "signature"   : "g"
      }
      self.data = None
      self.all_class_functions = ""
      self.object_interface_map = {}
      self.all_classes = ""
      self.class_object_map = {}
      self.all_class_objects = ""
      self.all_startup = ""
      self.load_json_file(json_file)
      self.map_dbus_objects_to_interfaces(self.data)
      self.create_classes()
      self.create_startup()
      self.create_class_objects()

    def map_data_types(self, data_types, data_type_map):
      return ','.join(data_type_map.get(data_type, "") for data_type in data_types.split(','))

    def load_json_file(self, json_file):
      if(json_file == None):
        print(f"No .json file provided")
        exit()
      try:
        with open(json_file, 'r') as f:
          self.data = json.load(f)
      except Exception as e:
        print(f"Error occurred trying to open .json file: {e}")
        exit()

    def map_dbus_objects_to_interfaces(self, data):
      for node in data["dbusFunctions"]:
        object_name = node["metadata"]["dbusObjectName"]
        if not object_name or object_name == "":
          continue

        if object_name not in self.object_interface_map:
          interface_name = node["metadata"]["dbusInterfaceName"]
          self.object_interface_map[object_name] = interface_name

    def load_and_create_functions(self, data, dbus_service_name, dbus_object_name):
      all_class_functions = ""
      for node in data["dbusFunctions"]:
        object_name     = node["metadata"]["dbusObjectName"]
        interface_name  = node["metadata"]["dbusInterfaceName"]
        function_name   = node["metadata"]["dbusFunctionName"]
        service_name    = node["metadata"]["dbusServiceName"]

        if not function_name or function_name == "":
          continue
        if service_name != dbus_service_name:
          #print(f"Service '{service_name}' not equal to '{dbapp_service_name}' for {function_name} skipped")
            continue
        if object_name != dbus_object_name:
          #print(f"Object '{object_name}' not equal to '{dbapp_object_name}' for {function_name} skipped")
          continue
        if interface_name != dbus_service_name:
          #print(f"Interface '{interface_name}' not equal to '{dbapp_service_name}' for {function_name} skipped")
          continue

        parameters = node["parameters"]
        param_types = ','.join(param["type"] for param in parameters)
        raw_in = self.map_data_types(param_types, self.data_type_map)
        in_signature = raw_in.replace(",", "")
        out_signature = 'b'
        argument_number = len(in_signature) + len(out_signature)
        result = True
        '''
        print(f"Function Name: '{function_name}'")
        print(f"Raw : '{raw_in}'")
        print(f"In Signature: '{in_signature}'")
        print(f"Out Signature: '{out_signature}'")
        print(f"Argument number: '{argument_number}'")
        '''

        new_function = self.create_function(in_signature, out_signature, function_name, argument_number, result)
        all_class_functions += new_function
        
      return all_class_functions

    def create_function(self, in_signature, out_signature, function_name, argument_number, result):
      arguments = ', '.join([f'arg{i}' for i in range(0, argument_number)])
      function_decorator = f"@dbus_method_async(input_signature='{in_signature}', result_signature='{out_signature}')"
      function_def = f"""
      async def {function_name}({arguments}):"""
      function_body = f"""
          print("Received arguments:", {arguments})
          return {result}\n
      """

      function_code = function_decorator + function_def + function_body
      return function_code

    def create_classes(self):
      for dbus_object, dbus_interface in self.object_interface_map.items():
        self.all_class_functions = self.load_and_create_functions(self.data, dbus_interface, dbus_object)
        if not self.all_class_functions or self.all_class_functions == "":
          continue

        words = dbus_object.split('/')
        class_name = ''.join(word.capitalize() for word in words if word)
        self.class_object_map[dbus_object] = class_name
        new_class=f"""
class {class_name}Object(
      DbusInterfaceCommonAsync, 
      interface_name='{dbus_interface}'):
      {self.all_class_functions}
    """
        self.all_classes += new_class

    def create_class_objects(self):
      for object_name, class_name in self.class_object_map.items():
        self.all_class_objects += f"""
    {class_name.lower()} = {class_name}Object()
    """

    def create_startup(self):
        
      for object_name, class_name in self.class_object_map.items():
        for object_name_oi, interface_name in self.object_interface_map.items():
          if object_name_oi == object_name:
            self.all_startup += f"""
        await request_default_bus_name_async('{interface_name}')
        {class_name.lower()}.export_to_dbus('{object_name}')
    """
      
    def get_source_code(self):
      return f"""{self.linux_executor}

from asyncio import new_event_loop

import sdbus
from sdbus import (
    DbusInterfaceCommonAsync,
    dbus_method_async,
    request_default_bus_name_async,
)
{self.all_classes}
if __name__ == '__main__':
    loop = new_event_loop()
{self.all_class_objects}
    async def startup() -> None:
        print("Startup...")
{self.all_startup}
    loop.run_until_complete(startup())
    loop.run_forever()
    print(f"D-Bus service running...")
"""