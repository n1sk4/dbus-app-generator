# D-Bus App Generator
Python app using sdbus library.

This scripts purpose is to dynamically create classes, methods and calls based on a provided json file. 

## JSON file structure
```
├── dbusFunctions
│   ├── id: EXAMPLE
│   │    ├── parameters
│   │    │   ├── id: example_string, type: string
│   │    │   ├── id: example_int, type: int
│   │    │   └── id: ..., type: ...
│   │    └── metadata
│   │        ├── dbusServiceName: com.interface.example
│   │        ├── dbusObjectName: /example/object
│   │        ├── dbusInterfaceName: com.interface.example
│   │        └── dbusFunctionName: dbusMethodExample
│   │
│   └── id: ...
```

```
"dbusFunctions": [
    {
      "id": "EXAMPLE",
      "parameters": [
        { "id": "example_string", "type": "string" },
        { "id": "example_int", "type": "int" }
      ],
      "metadata": {
        "dbusServiceName": "com.interface.example",
        "dbusObjectName": "/example/object",
        "dbusInterfaceName": "com.interface.example",
        "dbusFunctionName": "dbusMethodExample"
      }
    }
]
```

## Dependencies
Python 3.11 installed

Using PIP:
```
 sudo pip install --only-binary ':all:' sdbus
OR
 sudo pip install --only-binary ':all:' sdbus --break-system-packages
```

## Running the generator
Convert to unix file type:
```
 sudo dos2unix DBusAppGenerator.py
 sudo dos2unix DBusAppGeneratorClass.py
```
Make executable: 
```
 sudo chmod +x DBusAppGenerator.py
 sudo chmod +x DBusAppGeneratorClass.py
```
Run:
Running the command to start DBusAppGenerator, it will generate every interface, object and function from provided JSON file.
You can add arguments to setup the name, select JSON file and select the interface which will be generated:
| Argument  | Description |
| ------------- | ------------- |
| interface_name  | interface name from JSON file you want to generate functions for  |
| -f / --output_file  | Name of the generated file  |
| -j / --json_file Cell  | JSON file name/path  |
Examples:
```
./DBusAppGenerator.py
./DBusAppGenerator.py com.interface.example -f DBApp.py -j functions.json
./DBusAppGenerator.py com.interface.example --output_file DBApp.py --json_file functions.json
```

Output:
Generated DBApp.py file:
```
#!/usr/bin/python3
 
from asyncio import new_event_loop
 
import sdbus
from sdbus import (
    DbusInterfaceCommonAsync,
    dbus_method_async,
    request_default_bus_name_async,
)
 
class ComInterfaceExampleObject(
      DbusInterfaceCommonAsync,
      interface_name='com.interface.example'):
 
      @dbus_method_async(input_signature='si', result_signature='b', method_name='dbusMethodExample')
      async def dbusMethodExample(arg0, arg1, arg2):
          print("Received arguments:", arg0, arg1, arg2)
          return True
 
      #Add functions here...
 
if __name__ == '__main__':
    loop = new_event_loop()
 
    comInterfaceExample = ComInterfaceExampleObject()
     
    async def startup() -> None:
        print("Running...")
 
        await request_default_bus_name_async('com.interface.example')
        ct600dbapp.export_to_dbus('/example/object')
     
    loop.run_until_complete(startup())
    loop.run_forever()
```
