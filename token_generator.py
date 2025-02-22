from uuid import UUID
import os
import yaml

# https://github.com/python/cpython/blob/3.5/Lib/uuid.py
def uuid4():
    """Generate a random UUID."""
    return UUID(bytes=os.urandom(16), version=4).hex

config = {'PLANT_TOKEN': uuid4(), 'SENSORS_TOKENS':{'MOISTURE_TOKEN': uuid4(), 'HUMIDITY_TOKEN': uuid4(), 'TEMPERATURE_TOKEN': uuid4()}}]

with open('config.yml', 'w') as yaml_file:
    yaml.dump(config, yaml_file, default_flow_style=False)

# generate a configuration of tokens without yaml
""" f = open("config.ini", "w")
f.write("PLANT_TOKEN=%s\n" % uuid4())
f.write("MOISTURE_TOKEN=%s\n" % uuid4())
f.write("HUMIDITY_TOKEN=%s\n" % uuid4())
f.write("TEMPERATURE_TOKEN=%s\n" % uuid4())
f.close() """