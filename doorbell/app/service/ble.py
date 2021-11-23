
# from bluepy.btle import Scanner, DefaultDelegate

# class ScanDelegate(DefaultDelegate):
#     def __init__(self):
#         # DefaultDelegate.__init__(self)
#         super().__init__()

#     def handleDiscovery(self, dev, isNewDev, isNewData):
#         if isNewDev:
#             print("Discovered device", dev.addr)
#         elif isNewData:
#             print("Received new data from", dev.addr)


# class ScanHandler():
#     def __init__(self):
#         self.scanner = Scanner().withDelegate(ScanDelegate())
#         devices = self.scanner.scan(10.0)

#     # def run(self):



from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter


class ScanHandler():
    def __init__(self):
        scanner = BeaconScanner(self.handle_discovery)
        scanner.start()


    def handle_discovery(self, bt_addr, rssi, packet, additional_info):
        print(f"{bt_addr}, {rssi}, {packet}, {additional_info}")