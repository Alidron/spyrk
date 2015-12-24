# This file is part of Spyrk.
#
# Spyrk is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Spyrk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Spyrk.  If not, see <http://www.gnu.org/licenses/>.

from collections import namedtuple

from hammock import Hammock  # pip install hammock
from cached_property import timed_cached_property # pip install cached-property

class SparkCloud(object):

    """Provides access to the Spark Cloud.
    
    >>> spark = SparkCloud(USERNAME, PASSWORD)
    # Or
    >>> spark = SparkCloud(ACCESS_TOKEN)
    
    # List devices
    >>> print spark.devices

    # Access device
    >>> spark.devices['captain_hamster']
    # Or, shortcut form
    >>> spark.captain_hamster

    # List functions and variables of a device
    >>> print spark.captain_hamster.functions
    >>> print spark.captain_hamster.variables

    # Tell if a device is connected
    >>> print spark.captain_hamster.connected

    # Call a function
    >>> spark.captain_hamster.digitalwrite('D7', 'HIGH')
    >>> print spark.captain_hamster.analogread('A0')
    # (or any of your own custom function)

    # Get variable value
    >>> spark.captain_hamster.myvariable
    """
    
    def __init__(self, username_or_access_token, password=None, spark_api = Hammock('https://api.particle.io')):
        """Initialise the connection to a Spark Cloud.
        
        If you give a user name and password an access token will be requested.
        
        The list of known devices attached to your account will be requested.
        
        If you have several devices and not all of them are connected it will
        take a long time to create the object. The Spark Cloud will take ~30
        seconds (per device?) to reply as it waits for an answer from the
        disconnected devices.
        """
        self.spark_api = spark_api
        
        if password is None:
            self.access_token = username_or_access_token
        else:
            self.access_token = self._login(username_or_access_token, password)
            
        self.spark_api = self.spark_api.v1.devices

    @staticmethod
    def _check_error(response):
        """Raises an exception if the Spark Cloud returned an error."""
        if (not response.ok) or (response.status_code != 200):
            raise Exception(
                response.json()['error'] + ': ' +
                response.json()['error_description']
            )
        
    def _login(self, username, password):
        """Proceed to login to the Spark Cloud and returns an access token."""
        data = {
            'username': username,
            'password': password,
            'grant_type': 'password'
        }
        r = self.spark_api.oauth.token.POST(auth=('spark', 'spark'), data=data)
        self._check_error(r)
        return r.json()['access_token']

    @timed_cached_property(ttl=10) # cache the device for 10 seconds.
    def devices(self):
        """Create a dictionary of devices known to the user account."""
        params = {'access_token': self.access_token}
        r = self.spark_api.GET(params=params)
        self._check_error(r)
        json_list = r.json()

        devices_dict = {}
        if json_list:
            # it is possible the keys in json responses varies from one device to another: compute the set of all keys
            allKeys = {'functions', 'variables', 'api', 'requires_deep_update', 'status'} # added by device_info
            for device_json in json_list:
                allKeys.update(device_json.keys())

            Device = _BaseDevice.make_device_class(self, allKeys)
                    
            for d in json_list:
                if d["connected"]:
                    info = self._get_device_info(d['id'])
                    d['functions'] = info.get('functions')
                    d['variables'] = info.get('variables')
                    d['api'] = self.spark_api(d['id'])
                    d['requires_deep_update'] = d.get('requires_deep_update', False)
                    d['status'] = info.get('status')
                # ensure the set of all keys is present in the dictionnary (Device constructor requires all keys present)
                [d.setdefault(key, None) for key in allKeys]

                print d
                devices_dict[d['name']] = Device(**d)
                
        return devices_dict
            
    def _get_device_info(self, device_id):
        """Queries the Spark Cloud for detailed information about a device."""
        params = {'access_token': self.access_token}
        r = self.spark_api(device_id).GET(params=params)
        self._check_error(r)
        return r.json()
            
    def __getattr__(self, name):
        """Returns a Device object as an attribute of the SparkCloud object."""
        if name in self.devices:
            return self.devices[name]
        else:
            raise AttributeError()
    
class _BaseDevice(object):

    """Parent class for the dynamic Device class.
    
    The Device class being made of whatever fields the Spark Cloud API gives us,
    it has to be contructed on the fly once we know those fields.
    
    The generated Device class is subclassing this _BaseDevice as well as a
    nametuple.
    
    The namedtuple host all static fields while _BaseDevice host methods
    extending how a Device object should behave.
    """

    @staticmethod
    def make_device_class(spark_cloud, entries):
        """Returns a dynamic Device class based on what a GET device list from
        the Spark Cloud returns.
        
        spark_cloud parameter should be the caller instance of SparkCloud.
        
        entries parameter should be the list of fields the Spark Cloud API is
        returning.
        """
        attrs = list(
            set(
                list(entries) + [
                    'requires_deep_update', 'functions', 'variables', 'api', 'status'
                ]
            )
        )
        
        return type(
            'Device',
            (_BaseDevice, namedtuple('Device', attrs)),
            {'__slots__': (), 'spark_cloud': spark_cloud}
        )
        
    def __getattr__(self, name):
        """Returns virtual attributes corresponding to function or variable
        names.
        """
        params = {'access_token': self.spark_cloud.access_token}
        if not self.connected:
            raise IOError("{}.{} is not available: the spark device is not connected.".format(self.name, name))

        if name in self.functions:
        
            def fcall(*args):
                data = {'params': ','.join(args)}
                r = self.api(name).POST(params=params, data=data)
                self.spark_cloud._check_error(r)
                return r.json()['return_value']
                
            return fcall
            
        elif name in self.variables:
            r = self.api(name).GET(params=params)
            self.spark_cloud._check_error(r)
            return r.json()['result']
            
        else:
            raise AttributeError()
