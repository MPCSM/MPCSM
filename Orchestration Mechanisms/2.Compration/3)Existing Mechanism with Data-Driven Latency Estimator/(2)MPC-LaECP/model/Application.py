from model.MicroServiceModel import MicroService
class App(object):
    def __init__(self, appName,latencyCons):
        self.appName = appName
        self.latencyCons=latencyCons

    def setMicroServices(self,microS):
        self.microServices=[]
        for microService in microS:
            service=MicroService(microService[0],microService[1],microService[2])
            service.setDepth(microService[3])
            service.setCPUDemand(microService[4])
            service.setMemDemand(microService[5])
            service.setPubTopic(microService[6])
            service.setPubVolum(microService[7])
            service.setSubTopic(microService[8])
            service.setSubVolum(microService[9])
            service.setComponent(microService[10])
            service.setRate(microService[11])
            service.setTotalCount(microService[12])
            self.microServices.append(service)

    def getAppName(self):
        return self.appName

    def getLatencyCons(self):
        return self.latencyCons

    def getMicroServices(self):
        return self.microServices