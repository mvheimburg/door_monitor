"""Containers module."""

from dependency_injector import containers, providers
from os import path

import yaml

from frontend.app import DoorMonitorApp
from definitions import ROOT_DIR


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    # cfg = None
    # cfg_path = path.join(ROOT_DIR, "config.yaml")
    # with open(cfg_path, 'r') as stream:
    #     cfg = yaml.load(stream, Loader=yaml.FullLoader)
    # print(cfg)

    # print(type(config.bell))
    # print(config.bell)


    frontend = providers.Singleton(DoorMonitorApp, config)

