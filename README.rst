Spyrk
=====

Python module for Spark devices.

Use it as follow:

..  code:: python

    from spyrk import SparkCloud

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

    # Get variable value
    spark.captain_hamster.myvariable

Currently supporting:
---------------------

* Initialisation by username/password (generating a new access token every time).
* Initialisation by access token (get it from the Build Web IDE).
* Automatic discovery of devices.
* Automatic discovery of functions and variables in a device.
* Calling a function.
* Accessing a variable value.

Not yet supported:
------------------

* Subscribing and publishing events
* Any PUT method of the API (like uploading a firmware or application.cpp). That would be cool though.

Installation
------------

..  code:: bash

    $ pip install spyrk

Licensing and contributions
---------------------------

Spyrk is licensed under LGPLv3 and welcome contributions following the `C4.1 - Collective Code Construction Contract <http://rfc.zeromq.org/spec:22>`_ process.
