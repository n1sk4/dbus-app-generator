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

https://github.com/n1sk4/dbus-app-generator/blob/c74db2a3e5cf82f7e4e0a349bcf92e3415f13a6f/example/functions.json#L1C1-L16C2

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
| Argument                | Description                                                       |
| ----------------------- | ----------------------------------------------------------------- |
| interface_name          | interface name from JSON file you want to generate functions for  |
| -f / --output_file      | Name of the generated file                                        |
| -j / --json_file Cell   | JSON file name/path                                               |


Examples:
```
./DBusAppGenerator.py
./DBusAppGenerator.py com.interface.example -f DBApp.py -j functions.json
./DBusAppGenerator.py com.interface.example --output_file DBApp.py --json_file functions.json
```

Output:
Generated DBApp.py file:

https://github.com/n1sk4/dbus-app-generator/blob/c74db2a3e5cf82f7e4e0a349bcf92e3415f13a6f/example/DBApp.py#L1C1-L34C23
