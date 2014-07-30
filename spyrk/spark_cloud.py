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

class SparkCloud(object):
    def __init__(self, username_or_access_token, password=None):
        self.spark_api = Hammock('https://api.spark.io')
        
        if password is None:
            self.access_token = username_or_access_token
        else:
            self.access_token = self._login(username_or_access_token, password)
            
        self.spark_api = self.spark_api.v1.devices
        
        self._get_devices()
        
    @staticmethod
    def _check_error(response):
        if (not response.ok) or (response.status_code != 200):
            raise Exception(
                response.json()['error'] + ': ' +
                response.json()['error_description']
            )
        
    def _login(self, username, password):
        data = {
            'username': username,
            'password': password,
            'grant_type': 'password'
        }
        r = self.spark_api.oauth.token.POST(auth=('spark', 'spark'), data=data)
        self._check_error(r)
        return r.json()['access_token']
        
    def _get_devices(self):
        params = {'access_token': self.access_token}
        r = self.spark_api.GET(params=params)
        self._check_error(r)
        json_list = r.json()
        
        self.devices = {}
        if json_list:
            Device = namedtuple(
                'Device',
                list(set(json_list[0].keys() + ['requires_deep_update'])) +
                ['functions', 'variables', 'api']
            )
            _check_error = self._check_error
            
            def device_getattr(self, name):
                if name in self.functions:
                
                    def fcall(*args):
                        data = {'params': ','.join(args)}
                        r = self.api(name).POST(params=params, data=data)
                        _check_error(r)
                        return r.json()['return_value']
                    return fcall
                elif name in self.variables:
                    r = self.api(name).GET(params=params)
                    _check_error(r)
                    return r.json()['result']
                else:
                    raise AttributeError()
            Device.__getattr__ = device_getattr
                    
            for d in json_list:
                info = self._get_device_info(d['id'])
                d['functions'] = info['functions']
                d['variables'] = info['variables']
                d['api'] = self.spark_api(d['id'])
                d['requires_deep_update'] = d.get('requires_deep_update', False)

                self.devices[d['name']] = Device(**d)
            
    def _get_device_info(self, device_id):
        params = {'access_token': self.access_token}
        r = self.spark_api(device_id).GET(params=params)
        self._check_error(r)
        return r.json()
            
    def __getattr__(self, name):
        if name in self.devices:
            return self.devices[name]
        else:
            raise AttributeError()
