#!/usr/anaconda3/envs/grasp_svr/bin/python python3
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'


from os import path

from kivy.lang import Builder
from kivymd.uix.label import MDLabel

from frontend.framework.content import ContentBase



LOAD_FILE = 'doorbell.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
print(FILE_PATH)
Builder.load_file(FILE_PATH)


class DoorBell(ContentBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('Importing DoorBell')





    
    
