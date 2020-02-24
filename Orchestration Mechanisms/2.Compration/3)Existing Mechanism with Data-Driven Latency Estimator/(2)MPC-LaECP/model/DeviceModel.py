class Device(object):
    def __init__(self, deviceName):
        self.deviceName = deviceName

    def setCPUTotal(self, CPUTotal):
        self.CPUTotal = CPUTotal

    def getCPUTotal(self):
        return self.CPUTotal

    def setMemTotal(self, MemTotal):
        self.MemTotal = MemTotal

    def getMemTotal(self):
        return self.MemTotal


    def setCPURemain(self, CPURemain):
        self.CPURemain = CPURemain

    def setPubTopic(self, pubTopic):
        self.pubTopic = pubTopic

    def setPubVolum(self, pubVolum):
        self.pubVolum = pubVolum

    def setSubTopic(self, subTopic):
        self.subTopic = subTopic

    def setSubVolum(self, subVolum):
        self.subVolum = subVolum

    def setVolums(self, volums):
        self.volums = volums

    def setCompute(self, compute):
        self.compute = compute

    def getCompute(self):
        return self.compute

    def getCPURemain(self):
        return self.CPURemain

    def setMemRemain(self, MemRemain):
        self.MemRemain = MemRemain

    def setFrequency(self, frequency):
        self.frequency = frequency

    def getMemRemain(self):
        return self.MemRemain

    def getDeviceName(self):
        return self.deviceName


    def getResourceTotal(self):
        return self.resourceTotal

    def getResourceRemain(self):
        return self.resourceRemain

    def getPubTopic(self):
        return self.pubTopic

    def getPubVolum(self):
        return self.pubVolum

    def getSubTopic(self):
        return self.subTopic

    def getSubVolum(self):
        return self.subVolum

    def getVolums(self):
        return self.volums

    def getFrequency(self):
        return self.frequency

