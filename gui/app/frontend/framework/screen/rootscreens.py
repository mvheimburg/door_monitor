#!/usr/anaconda3/envs/grasp_svr/bin/python python3
# -*- coding: utf-8 -*-
__author__ = 'sintefocean'


from os import path
from kivy.lang import Builder

from frontend.framework.screen.screenbehaviour import ScreenBehaviour




LOAD_FILE = 'rootscreens.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
Builder.load_file(FILE_PATH)



class RootScreen(ScreenBehaviour):
    pass

