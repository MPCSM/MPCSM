from model.DeviceModel import Device

class MicroService(object):

    def __init__(self, serviceName,isSource,isSink):
        self.name = serviceName
        self.isSource=isSource
        self.isSink=isSink

    def setDepth(self, depth):
        self.depth = depth
    def setCandidateDevice(self, candidateDevice):
        self.candidateDevice = candidateDevice
    def setCandidateLatency(self, candidateLatency):
        self.candidateDevice = candidateLatency

    def setCPUDemand(self,CPUDemand):
        self.CPUDemand=CPUDemand

    def getCPUDemand(self):
        return self.CPUDemand

    def setMemDemand(self,memDemand):
        self.memDemand=memDemand

    def getMemDemand(self):
        return self.memDemand

    def setInnode(self,innode):
        self.innode=innode

    def setDevice(self,device):
        self.device=device

    def setLatencyRe(self,latencyRe):
        self.latencyRe=latencyRe

    def setAcutalLat(self,actualLat):
        self.actualLat=actualLat

    def setOnehopLat(self,onehopLat):
        self.onehopLat = onehopLat

    def setPubTopic(self, pubTopic):
        self.pubTopic = pubTopic

    def setPubVolum(self, pubVolum):
        self.pubVolum = pubVolum

    def setSubTopic(self, subTopic):
        self.subTopic = subTopic

    def setSubVolum(self, subVolum):
        self.subVolum = subVolum

    def setComponent(self,component):
        self.component=component
    # rate
    def setRate(self,rate):
        self.rate=rate
    #totalCount
    def setTotalCount(self,totalCount):
        self.totalCount=totalCount;

    def setComputeDemand(self,computeDemand):
        self.computeDemand=computeDemand

    def getComputeDemand(self):
        return self.computeDemand

    def setDiffLatency(self, diffLatency):
        self.diffLatency = diffLatency

    def getTotalCount(self):
        return self.totalCount;

    def getDepth(self):
        return self.depth
    def getResourceDemand(self):
        return self.resourceDemand
    def getServiceName(self):
        return self.name
    def getInnode(self):
        return self.innode
    def getDevice(self):
        return self.device

    def getLatencyRe(self):
        return self.latencyRe

    def getAcutalLat(self):
        return self.actualLat

    def getOnehopLat(self):
        return self.onehopLat

    def getIsSink(self):
        return self.isSink

    def getIsSource(self):
        return self.isSource

    def getPubTopic(self):
        return self.pubTopic

    def getPubVolum(self):
        return self.pubVolum

    def getSubTopic(self):
        return self.subTopic

    def getSubVolum(self):
        return self.subVolum

    def getComponent(self):
        return self.component
    # rate
    def getRate(self):
        return self.rate


    def getDiffLatency(self):
        return self.diffLatency


if __name__ == '__main__':
    mic = MicroService("abc")
    mic.setInnode(["haha","wwww"])
    mic.setDevice("abc")
    mic.setResourceDemand([10,5])
    test=mic.getInnode()

    print(type(test))
    print(test[1].getServiceName())
    print(mic.getDevice().getDeviceName())
    print(mic.getResourceDemand())