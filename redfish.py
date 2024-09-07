class Redfish:
    
    @staticmethod
    def getSystem(id):
        return {
            "@odata.context": "/redfish/v1/$metadata#Systems/Members/$entity",
            "@odata.id": f"/redfish/v1/Systems/{id}/",
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
            "Id": id,
            "UUID": "123-321",
            "Manufacturer": "Redfish",
            "Model": id,
            "MemorySummary": {
                "TotalSystemMemoryGiB": "128"
            },
            "ProcessorSummary": {
                "Count": "2",
                "Model": "Intel(R) Generic"
            }
        }