# Spyrk

Python module for Spark devices.

Use it as follow:

```python
from Spyrk import SparkCloud

USERNAME = 'he.ho@example.com'
PASSWORD = 'pasSs'
ACCESS_TOKEN = '12adza445452d4za524524524d5z2a4'

spark = SparkCloud(USERNAME, PASSWORD)
# Or
spark = SparkCloud(ACCESS_TOKEN)

# List devices
print spark.devices

# Access device
spark.devices['captain_hamster']
# Or, shortcut form
spark.captain_hamster

# List functions and variables of a device
print spark.captain_hamster.functions
print spark.captain_hamster.variables

# Tell if a device is connected
print spark.captain_hamster.connected

# Call a function
spark.captain_hamster.digitalwrite('D7', 'HIGH')
print spark.captain_hamster.analogread('A0')
# (or any of your own custom function)
```

## Currently supporting:

* Initialisation by username/password (generating a new access token every time).
* Initialisation by access token (get it from the Build Web IDE).
* Automatic discovery of devices.
* Automatic discovery of functions and variables in a device.
* Calling a function.

## Not yet supported:
* Any PUT method of the API (like uploading a firmware or application.cpp). That would be cool though.
* Accessing a variable value.
* A command line interface (well, an official one is on its way...).

## Installation

`pip install spyrk`.
