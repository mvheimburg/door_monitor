
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'

import sys
from os import environ, path

import yaml

from pythonpath import add_dir_to_pythonpath





def main(mode=0):
    """
    Main function. 
    
    """
    

    from frontend.app import DoorMonitorApp
    from workers import MqttWorker
    from definitions import ROOT_DIR

    if mode==0:
        server = environ.get('MQTT_SERVER', 'mqtt://localhost:1883')
        uname = environ.get('MQTT_USERNAME', None)
        password = environ.get('MQTT_PASSWORD', None)
        client_id = environ.get('MQTT_CLIENT_ID', None)
    else:
        secret_cfg_path = path.join(ROOT_DIR, "secrets.yaml")
        with open(secret_cfg_path, 'r') as stream:
            secret_cfg = yaml.load(stream, Loader=yaml.FullLoader)
        print(secret_cfg)

        server = secret_cfg['mqtt']['server']
        uname = secret_cfg['mqtt']['username']
        password = secret_cfg['mqtt']['password']
        client_id = secret_cfg['mqtt']['client_id']

    cfg = None
    cfg_path = path.join(ROOT_DIR, "config.yaml")
    with open(cfg_path, 'r') as stream:
        cfg = yaml.load(stream, Loader=yaml.FullLoader)
    print(cfg)

    mqttworker = MqttWorker(client_id=client_id, config=cfg)
    mqttworker.connect_to_broker(server, uname, password)
    mqttworker.subscribe()
    mqttworker.run()

    # nfcworker = NFCWorker()
    # nfcworker.run()

    app = DoorMonitorApp(worker=mqttworker)
    app.run()



if __name__ == "__main__":

    mode = 0

    if 'local' in sys.argv:
        mode = 1

    add_dir_to_pythonpath()
    main(mode=mode)