'''
Testing the Spark Cloud API by using a real connected Spark Core.
To use this test you must create a config.py file in this tests folder.
You can use config.py.tpl as a template. The target core should run the default
Tinker app.

Beware, if you have several cores resgistered on your account and some are not
connected, the initialisation of the SparkCloud class will take a long time,
and this will make the tests very slow. This is because when we ask for the list
of devices and not all devices are connected, the Spark Cloud server wait
several seconds before timing out on them.

These tests could greatly benefit from using a fake core emulated in a staged
instance of the Spark Cloud server...
'''
import time

import pytest
from mock import *
from hammock import Hammock

from spyrk import SparkCloud

def mockHTTPResponse(json_result):
    mock = MagicMock()
    mock.ok = True
    mock.status_code = 200
    mock.json = MagicMock(return_value=json_result)
    return mock

@pytest.fixture
def hammock():
    hammock = MagicMock()

    # POST /oauth/token
    token_response = mockHTTPResponse(
        {
            "access_token": "254406f79c1999af65a7df4388971354f85cfee9",
            "token_type": "bearer",
            "expires_in": 7776000
        })
    hammock.oauth.token.POST = MagicMock(return_value=token_response)

    # GET v1/devices
    device_list = mockHTTPResponse(
        [
            {
                "id": "53ff6f0650723",
                "name": "plumber_laser",
                "last_app": None,
                "last_heard": None,
                "connected": False
            },
            {
                "id": "53ff6e066667574845411267",
                "name": "T1000",
                "last_app": None,
                "last_ip_address": "172.0.0.1",
                "last_heard": "2015-06-02T20:56:28.532Z",
                "product_id": 0,
                "connected": True
            }
        ]
    )

    # GET /v1/devices/{DEVICE_ID}
    device0_info = MagicMock()
    device0_info.GET.return_value = mockHTTPResponse(
        {
            "id": "53ff6f0650723",
            "name": "plumber_laser",
            "connected": False,
            "variables": {},
            "functions": [],
            "cc3000_patch_version": None,
            "product_id": 0,
            "last_heard": None
        }
    )

    device1_info = MagicMock()
    device1_info.GET.return_value = mockHTTPResponse(
        {
            "id": "53ff6e066667574845411267",
            "name": "T1000",
            "connected": True,
            "variables": {
                "game_state": "string"
            },
            "functions": [
                "digitalread",
                "digitalwrite",
                "analogread",
                "analogwrite"
            ],
            "cc3000_patch_version": "1.29",
            "product_id": 0,
            "last_heard": "2015-06-02T20:57:30.484Z"
        }
    )
    def route_devices(*args):
        if len(args) == 0:
            return DEFAULT
        if args[0] == "53ff6f0650723":
            return device0_info
        elif args[0] == "53ff6e066667574845411267":
            return device1_info
    hammock.v1.devices.side_effect = route_devices
    hammock.v1.devices.GET.return_value = device_list

    # POST /v1/devices/T1000/digitalwrite
    hammock.v1.devices("53ff6e066667574845411267")("digitalwrite").POST.return_value = mockHTTPResponse(
        {
            "return_value": 1
        }
    )

    # GET /v1/devices/T1000/game_state
    hammock.v1.devices("53ff6e066667574845411267")("game_state").GET.return_value = mockHTTPResponse(
        {
            "cmd": "VarReturn",
            "name": "game_state",
            "result": "state",
            "coreInfo": {
                "last_app": "",
                "last_heard": "2015-06-02T23:46:25.828Z",
                "connected": True,
                "last_handshake_at": "2015-06-02T23:45:56.201Z",
                "deviceID": "53ff6e066667574845411267"
            }
        }
    )

    return hammock

def test_login_password(hammock):
    """When login with user/password, SparkCloud fetches a token"""
    spark = SparkCloud("myLogin", "myPassword", spark_api=hammock)
    hammock.oauth.token.POST.assert_called_once_with(
        auth=('spark', 'spark'),
        data={"username": "myLogin", "password": "myPassword", "grant_type": "password"}
    )
    assert spark.access_token == "254406f79c1999af65a7df4388971354f85cfee9"

def test_login_token(hammock):
    """When login with an access token, the oauth token request is not used"""
    spark = SparkCloud("myToken", spark_api=hammock)
    assert spark.access_token == "myToken"

def test_target_device_accessed_by_name(hammock):
    """Access the spark device using its name as an attribute of the SparkCloud object"""
    spark = SparkCloud("myToken", spark_api=hammock)
    assert spark.T1000.connected == True
    hammock.v1.devices.GET.assert_called_once_with(
        params={"access_token": "myToken"}
    )
    print(hammock.v1.devices("53ff6e066667574845411267").GET.call_count == 1)

def test_target_device_accessed_by_dictionnary(hammock):
    spark = SparkCloud("myToken", spark_api=hammock)
    assert spark.devices["T1000"].connected == True
    hammock.v1.devices.GET.assert_called_once_with(
        params={"access_token": "myToken"}
    )
    assert hammock.v1.devices("53ff6e066667574845411267").GET.call_count == 1


def test_target_devices_caching(hammock):
    spark = SparkCloud("myToken", spark_api=hammock)
    assert spark.devices["T1000"].connected == True
    assert hammock.v1.devices("53ff6e066667574845411267").GET.call_count == 1
    hammock.v1.devices("53ff6e066667574845411267").GET.reset_mock()
    assert spark.devices["T1000"].connected == True
    assert hammock.v1.devices("53ff6e066667574845411267").GET.call_count == 0
    time.sleep(10)
    assert spark.devices["T1000"].connected == True
    assert hammock.v1.devices("53ff6e066667574845411267").GET.call_count == 1

def test_function_list(hammock):
    spark = SparkCloud("myToken", spark_api=hammock)
    device = spark.T1000
    assert 'digitalwrite' in device.functions

def test_variable_list(hammock):
    spark = SparkCloud("myToken", spark_api=hammock)
    device = spark.T1000
    assert 'game_state' in device.variables
    assert 'string' in device.variables["game_state"]

def test_function_call(hammock):
    spark = SparkCloud("myToken", spark_api=hammock)
    assert 1 == spark.T1000.digitalwrite('D7', 'HIGH')
    hammock.v1.devices("53ff6e066667574845411267")("digitalwrite").POST.assert_called_once_with(
        params={"access_token": "myToken"},
        data={"params": "D7,HIGH"}
    )

def test_variable_fetch(hammock):
    spark = SparkCloud("myToken", spark_api=hammock)
    assert spark.T1000.game_state == "state"
    hammock.v1.devices("53ff6e066667574845411267")("game_state").GET.assert_called_once_with(
        params={"access_token": "myToken"}
    )