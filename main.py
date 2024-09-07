from machine import Pin,SPI
import network
import time
from microWebSrv import MicroWebSrv

spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin

#W5x00 chip init
def init():
    nic.active(True)
    nic.ifconfig(('192.168.178.20','255.255.255.0','192.168.178.1','1.1.1.1'))
    while not nic.isconnected():
        time.sleep(1)
        # print(nic.regs())
    print(nic.ifconfig())
        
def main():
    init()

@MicroWebSrv.route('/redfish/v1')
def redfishRoot(httpClient, httpResponse):
    httpResponse.WriteResponseJSONOk({
       "@odata.context":"/redfish/v1/$metadata#ServiceRoot.ServiceRoot",
       "@odata.id":"/redfish/v1/",
       "@odata.type":"#ServiceRoot.1.0.0.ServiceRoot",
       "Chassis":{
          "@odata.id":"/redfish/v1/Chassis/"
       },
       "Id":"v1",
       "Name":"Redreset Root Service",
       "RedfishVersion":"1.0.0",
       "ServiceVersion":"1.0.0",
       "Systems":{
          "@odata.id":"/redfish/v1/Systems/"
       },
       "Time":"2024-09-07T14:17:09Z",
       "Type":"ServiceRoot.1.0.0",
       "UUID":"1cb57fd1-f7f6-5bb3-baca-2767e3006050",
    })

@MicroWebSrv.route('/redfish/v1/Systems')
def redfishSystems(httpClient, httpResponse):
    httpResponse.WriteResponseJSONOk({
        "@odata.context": "/redfish/v1/$metadata#Systems",
        "@odata.id": "/redfish/v1/Systems/",
        "@odata.type": "#ComputerSystemCollection.ComputerSystemCollection",
        "Description": "Computer Systems view",
        "MemberType": "ComputerSystem.1",
        "Members": [
            {
                "@odata.id": "/redfish/v1/Systems/1/"
            }
        ],
        "Members@odata.count": 1,
        "Name": "Computer Systems",
        "Total": 1,
        "Type": "Collection.1.0.0"
    })
    
@MicroWebSrv.route('/redfish/v1/Systems/1')
def redfishSystem(httpClient, httpResponse):
    httpResponse.WriteResponseJSONOk({
        "@odata.context": "/redfish/v1/$metadata#Systems/Members/$entity",
        "@odata.id": "/redfish/v1/Systems/1/",
        "@odata.type": "#ComputerSystem.1.0.1.ComputerSystem",
        "Actions": {
            "#ComputerSystem.Reset": {
                "ResetType@Redfish.AllowableValues": [
                    "On",
                    "ForceOff",
                    "ForceRestart",
                    "PushPowerButton"
                ],
                "target": "/redfish/v1/Systems/1/Actions/ComputerSystem.Reset/"
            }
        },
        "Id": "1",
        "UUID": "123-321",
        "Manufacturer": "Redfish",
        "Model": "1",
        "MemorySummary": {
            "TotalSystemMemoryGiB": "128"
        },
        "ProcessorSummary": {
            "Count": "2",
            "Model": "Intel(R) Generic"
        }
    })

main()
mws = MicroWebSrv()      # TCP port 80 and files in /flash/www
mws.Start(threaded=False) # Starts server in a new thread