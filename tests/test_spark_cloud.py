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

from spyrk import SparkCloud

@pytest.fixture
def config():
    from . import config
    
    msg = 'Setup your tests/config.py before runnning the tests'
    assert config.login_password != ('username', 'password'), msg
    assert config.login_token != ('access_token'), msg
    assert config.target_device != 'device_name', msg
    
    return config

_cache_spark = None
@pytest.fixture
def spark(config):
    global _cache_spark
    
    if not _cache_spark:
        _cache_spark = SparkCloud(*config.login_token)
        
    return _cache_spark

# Somehow, does not work for me anymore. Have to investigate.
@pytest.mark.xfail
def test_login_password(config):
    spark = SparkCloud(*config.login_password)
    assert spark
    
def test_login_token(config):
    # spark = SparkCloud(*config.login_token)
    # assert spark
    pass
    
def test_target_device(config, spark):
    assert config.target_device in spark.devices
    device = getattr(spark, config.target_device)
    assert device.connected
    
def test_function_list(config, spark):
    device = getattr(spark, config.target_device)
    assert 'digitalwrite' in device.functions
    
def test_variable_list(config, spark):
    pass  # Not implemented in the testing core yet
    
def test_function_call(config, spark):
    device = getattr(spark, config.target_device)
    assert 1 == device.digitalwrite('D7', 'HIGH')
    time.sleep(0.5)
    assert 1 == device.digitalwrite('D7', 'LOW')
    
def test_variable_fetch(config, spark):
    pass  # Not implemented in the testing core yet
