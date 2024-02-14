#!/usr/bin/python3

from asyncio import new_event_loop

import sdbus
from sdbus import (
    DbusInterfaceCommonAsync,
    dbus_method_async,
    request_default_bus_name_async,
)

class ExampleObjectObject(
      DbusInterfaceCommonAsync, 
      interface_name='com.interface.example'):
      @dbus_method_async(input_signature='si', result_signature='b', method_name='dbusMethodExample')
      async def dbusMethodExample(arg0, arg1, arg2):
          print("Received arguments:", arg0, arg1, arg2)
          return True

      
    
if __name__ == '__main__':
    loop = new_event_loop()

    exampleobject = ExampleObjectObject()
    
    async def startup() -> None:
        print("Running...")

        await request_default_bus_name_async('com.interface.example')
        exampleobject.export_to_dbus('/example/object')
    
    loop.run_until_complete(startup())
    loop.run_forever()
