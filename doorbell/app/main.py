
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'

import sys
from os import environ, path

import yaml




def main(mode=0):
    """
    Main function. 
    
    """
    
    from models import MQTTConfig, APIConfig, Door, DoorsConfig, MqttStringConfig
    from frontend.app import DoorMonitorApp
    from definitions import ROOT_DIR



    if  environ.get('BUILD_TYPE', False):
        broker = environ.get('MQTT_SERVER', 'mqtt://localhost:1883')
        username = environ.get('MQTT_USERNAME', None)
        password = environ.get('MQTT_PASSWORD', None)
        client_id = environ.get('MQTT_CLIENT_ID', None)


    else:
        secret_cfg_path = path.join(ROOT_DIR, "secrets.yaml")
        with open(secret_cfg_path, 'r') as stream:
            secret_cfg = yaml.load(stream, Loader=yaml.FullLoader)
        print(secret_cfg)

        broker = secret_cfg['mqtt']['broker']
        username = secret_cfg['mqtt']['username']
        password = secret_cfg['mqtt']['password']
        client_id = secret_cfg['mqtt']['client_id']
        port = secret_cfg['mqtt']['port']

        api_url=secret_cfg['api']['url']

    cfg = None
    cfg_path = path.join(ROOT_DIR, "config.yaml")
    with open(cfg_path, 'r') as stream:
        cfg = yaml.load(stream, Loader=yaml.FullLoader)
    print(cfg)


    bell_config = MqttStringConfig(**cfg['bell'])
    mqtt_config = MQTTConfig(broker=broker, port=port, username=username, password=password, client_id=client_id)

    door_list = []
    for door, d_cfg in  cfg['doors'].items():
        print(f"new_door: {door}")
        new_door = Door(door_id=door, name=d_cfg['name'], command_topic=d_cfg['command_topic'], state_topic=d_cfg['state_topic'])
        # new_door.set_relay()
        door_list.append(new_door)
        
    doors_config = DoorsConfig(doors=door_list)

    print(cfg['garage'])

    garage_config=MqttStringConfig(**cfg['garage'])

    api_config=APIConfig(url=api_url)  

    mode_config = MqttStringConfig(**cfg['mode'])


    app = DoorMonitorApp(mqtt_config, doors_config, bell_config, garage_config, api_config, mode_config)
    app.run()



if __name__ == "__main__":

    mode = 0

    if 'local' in sys.argv:
        mode = 1

    # add_dir_to_pythonpath()
    main(mode=mode)