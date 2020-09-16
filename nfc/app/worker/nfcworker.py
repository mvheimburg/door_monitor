
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'

import nfc
import ndef
 


class NFCWorker():

    def __init__(self):
        self.NFC = nfc.ContactlessFrontend()
        self.NFC.open("tty:S0")


    def handle_tag(self, tag):
        print("Tag address: " + str(tag.identifier.hex()), flush=True)
        return True
        
    def run(self):
        
        print("Waiting for NFC tag ...", flush=True)
        self.NFC.connect(rdwr={'on-connect': self.handle_tag})
