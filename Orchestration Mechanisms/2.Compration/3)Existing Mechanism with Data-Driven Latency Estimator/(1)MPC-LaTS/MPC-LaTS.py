
import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import PolynomialFeatures

from model.DeviceModel import Device
from model.Application import App
import numpy as np
import operator

datasums=[10,20,30,40,50,60,70,80]
for thisTotalCount in datasums:
    placements = pd.read_csv(str(thisTotalCount) + "-placementInfo.csv").values

    s = 1
    # placements = pd.read_csv(str(thisTotalCount)+"-placementInfo.csv").values
    thisType = "only"
    devichName=["camera","faultsensor","edge0","edge1","edge2","cloud"]
    bandwidth=[[1000,94,94,93.2,93.7,4.45],
               [93.8, 1000, 331, 93.2, 85.9, 4.36],
               [94.1, 281, 1000, 93.6, 93.7, 3.33],
               [94.6, 94.7, 94.7, 1000, 93.4, 3.80],
               [93.7, 93.4, 93.8, 93.3, 1000, 3.79],
               [3.37, 3.36, 3.18, 3.36, 3.17, 1000]]
    apps = []
    rulPredictionLatencyCons = 2;
    faultDetectionLatencyCons = 1;
    waferInspectionLatencyCons = 0.6;

    faultDetectionCPU = [1, 2, 2, 2, 2, 2]
    faultDetectionMem = [5, 1, 5, 5, 5, 5]

    waferInspectionCPU = [1, 3, 3, 3, 1, 2]
    waferInspectionMem = [5, 5, 5, 5, 5, 5]

    rulPredictionCPU = [1, 1, 3]
    rulPredictionMem = [5, 5, 5]

    oneGraphApp = App("oneGraph", 3)

    oneGraphApp.setMicroServices([
        ["fault-source", True, False, 0, faultDetectionCPU[0], faultDetectionMem[0], 1, 7464602, 0, 0, 0.05, 1,thisTotalCount],# 0
        ["wafer-source", True, False, 0, waferInspectionCPU[0], waferInspectionCPU[0], 2, 552769, 0, 0, 0.05, 1,thisTotalCount],# 1
        #["rul-source", True, False, 0, rulPredictionCPU[0], rulPredictionMem[0], 1, 3509033, 0, 0, 0.0005, 5, 29],  # 2
        ["fault-losso", False, False, 1, faultDetectionCPU[1], faultDetectionMem[1], 3, 515318, 1, 7464602, 0.52, 1,thisTotalCount],#2
        ["wafer-static", False, False, 1, waferInspectionCPU[2], waferInspectionCPU[2], 1, 36632, 1, 314889, 0.01, 1,thisTotalCount],#3
        ["wafer-auto", False, False, 1, waferInspectionCPU[1], waferInspectionCPU[1], 1, 7132, 1, 237880, 0.008, 1,thisTotalCount],  #4
        #["rul-preprocess", False, False, 1, rulPredictionCPU[1], rulPredictionMem[1], 1, 63565202, 1, 3509033, 0.02, 5,thisTotalCount],#6
        #["rul-prediction", False, True, 2, rulPredictionCPU[2], rulPredictionMem[2], 1, 51086, 1, 63565202, 210, 5,thisTotalCount],#7
        ["wafer-cnn", False, False, 2, waferInspectionCPU[3], waferInspectionCPU[3], 1, 263, 1, 7132, 0.004, 1,thisTotalCount],  # 5
        ["fault-knn", False, False, 2, faultDetectionCPU[2], faultDetectionMem[2], 1, 12752, 1, 515318, 0.003, 1,thisTotalCount],  #6
        ["fault-xgboost", False, False, 2, faultDetectionCPU[4], faultDetectionMem[4], 1, 12752, 1, 515318, 0.0004, 1,thisTotalCount],  # 7
        ["fault-svm", False, False, 2, faultDetectionCPU[3], faultDetectionMem[3], 1, 12752, 1, 515318, 0.002, 1,thisTotalCount],  # 8
        ["wafer-svm", False, False, 2, waferInspectionCPU[4], waferInspectionCPU[4], 1, 611, 1, 36632, 0.0001, 1,thisTotalCount],  # 9
        ["fault-ensemble", False, True, 3, faultDetectionCPU[5], faultDetectionMem[5], 0, 0, 3, 12752, 49, 0.004,thisTotalCount],  # 10
        ["wafer-ensemble", False, True, 3, waferInspectionCPU[5], waferInspectionCPU[5], 0, 0, 2, 611, 0.002, 1,thisTotalCount],  # 11
    ])

    oneGraphAppServices = oneGraphApp.getMicroServices()
    oneGraphAppServices[0].setAcutalLat(0)
    oneGraphAppServices[1].setAcutalLat(0)

    oneGraphAppServices[2].setInnode([oneGraphAppServices[0]])
    oneGraphAppServices[3].setInnode([oneGraphAppServices[1]])
    oneGraphAppServices[4].setInnode([oneGraphAppServices[1]])

    oneGraphAppServices[5].setInnode([oneGraphAppServices[4]])
    oneGraphAppServices[6].setInnode([oneGraphAppServices[2]])
    oneGraphAppServices[7].setInnode([oneGraphAppServices[2]])
    oneGraphAppServices[8].setInnode([oneGraphAppServices[2]])
    oneGraphAppServices[9].setInnode([oneGraphAppServices[3]])
    oneGraphAppServices[11].setInnode([oneGraphAppServices[5],oneGraphAppServices[9]])
    oneGraphAppServices[10].setInnode([oneGraphAppServices[6],oneGraphAppServices[7],oneGraphAppServices[8]])

    thetime = []
    desGraphAppServices = []
    for micro in oneGraphAppServices:
        thetime.append(micro.getComponent())
    thetime = np.array(thetime)
    destime = np.argsort(-thetime)
    # print(destime)
    for index in destime:
        desGraphAppServices.append(oneGraphAppServices[index])
    print(desGraphAppServices)

    devices = []
    # nano、ljr、miniserver、cloud
    deviceFrequency = [1.43, 2.2, 3.6, 2.5]
    devicesCPU = [4, 12, 8, 24]
    devicesRemain = [3, 12, 6, 24]
    devicesMem = [100, 100, 100, 100]

    pubTopic = [1, 0, 1, 0]
    pubVolum = [611, 0, 515318, 0]
    subTopic = [1, 0, 1, 0]
    subVolum = [36632, 0, 12752, 0]
    volums = [37243, 0, 528070, 0]

    edge0 = Device("edge0")
    edge0.setCPUTotal(devicesCPU[0])
    edge0.setCPURemain(devicesRemain[0])
    edge0.setMemTotal(devicesMem[0])
    edge0.setMemRemain(devicesMem[0])
    edge0.setFrequency(deviceFrequency[0])

    edge0.setPubTopic(pubTopic[0])
    edge0.setPubVolum(pubVolum[0])
    edge0.setSubTopic(subTopic[0])
    edge0.setSubVolum(subVolum[0])
    edge0.setVolums(volums[0])
    devices.append(edge0)

    edge1 = Device("edge1")
    edge1.setCPUTotal(devicesCPU[1])
    edge1.setCPURemain(devicesRemain[1])
    edge1.setMemTotal(devicesMem[1])
    edge1.setMemRemain(devicesMem[1])
    edge1.setFrequency(deviceFrequency[1])
    edge1.setPubTopic(pubTopic[1])
    edge1.setPubVolum(pubVolum[1])
    edge1.setSubTopic(subTopic[1])
    edge1.setSubVolum(subVolum[1])
    edge1.setVolums(volums[1])
    devices.append(edge1)

    edge2 = Device("edge2")
    edge2.setCPUTotal(devicesCPU[2])
    edge2.setCPURemain(devicesRemain[2])
    edge2.setMemTotal(devicesMem[2])
    edge2.setMemRemain(devicesMem[2])
    edge2.setFrequency(deviceFrequency[2])
    edge2.setPubTopic(pubTopic[2])
    edge2.setPubVolum(pubVolum[2])
    edge2.setSubTopic(subTopic[2])
    edge2.setSubVolum(subVolum[2])
    edge2.setVolums(volums[2])
    devices.append(edge2)

    cloud = Device("cloud")
    cloud.setCPUTotal(devicesCPU[3])
    cloud.setCPURemain(devicesRemain[3])
    cloud.setMemTotal(devicesMem[3])
    cloud.setMemRemain(devicesMem[3])
    cloud.setFrequency(deviceFrequency[3])
    cloud.setPubTopic(pubTopic[3])
    cloud.setPubVolum(pubVolum[3])
    cloud.setSubTopic(subTopic[3])
    cloud.setSubVolum(subVolum[3])
    cloud.setVolums(volums[3])
    devices.append(cloud)

    rulsensor = Device("rulsensor")
    rulsensor.setCPUTotal(4)
    rulsensor.setCPURemain(4)
    rulsensor.setMemTotal(10)
    rulsensor.setMemRemain(10)
    rulsensor.setFrequency(0)
    rulsensor.setPubTopic(0)
    rulsensor.setPubVolum(0)
    rulsensor.setSubTopic(0)
    rulsensor.setSubVolum(0)
    rulsensor.setVolums(0)

    faultsensor = Device("faultsensor")
    faultsensor.setCPUTotal(4)
    faultsensor.setCPURemain(4)
    faultsensor.setMemTotal(10)
    faultsensor.setMemRemain(10)
    faultsensor.setFrequency(0.9)
    faultsensor.setPubTopic(1)
    faultsensor.setPubVolum(7464602)
    faultsensor.setSubTopic(0)
    faultsensor.setSubVolum(0)
    faultsensor.setVolums(7464602)
    oneGraphAppServices[0].setDevice(faultsensor)
    camera = Device("camera")
    camera.setCPUTotal(4)
    camera.setCPURemain(4)
    camera.setMemTotal(10)
    camera.setMemRemain(10)
    camera.setFrequency(0.9)
    camera.setPubTopic(2)
    camera.setPubVolum(552769)
    camera.setSubTopic(0)
    camera.setSubVolum(0)
    camera.setVolums(552769)
    oneGraphAppServices[1].setDevice(camera)
    # ------------------------------------------------------Part3 延迟模型---------------------------------------------------
    dataAtt = ["microComponent", "microSubVolum", "subDeviceCpuPercent"]

    def computeLatency(bandwidth, microSubvolum, serviceName, device, deviceCpuPercent):
        comm = microSubvolum / (bandwidth[0] * 1024 * 1024 / 8)
        xrf = joblib.load("Polynomial/finallyResult/"+str(serviceName) + '-' + str(device) +"-"+str(thisTotalCount)+ '.m')
        compute = xrf.predict(deviceCpuPercent)
        total = comm + compute
        return total;

    def oneLatency(bandwidth, microSubvolum, serviceName, device, deviceCpuPercent,microComponent):
        comm = microSubvolum / (bandwidth[0] * 1024 * 1024 / 8)
        if(device==5):
            compute=microComponent
        else:
            modelfile="finallyResult/" + str(serviceName) + '-' + str(device) + "-" + str(thisTotalCount) + '.m'
            xrf = joblib.load("Polynomial/"+modelfile)
            themap = pd.read_csv("Polynomial/finallyResult/map.csv")
            deg=themap[themap["models"] == modelfile]["deg"].values[0]
            quadratic_featurizer = PolynomialFeatures(degree=deg)
            X_test_quadratic = quadratic_featurizer.fit_transform([[deviceCpuPercent]])
            compute = xrf.predict(X_test_quadratic)
        total = comm + compute
        return total;


    def twoLatency(bandwidth, microSubvolum, serviceName, device, deviceCpuPercent,microComponent):

        comm1 = microSubvolum / (bandwidth[0] * 1024 * 1024 / 8)
        if (device == 5):
            compute = microComponent
        else:
            modelfile = "finallyResult/" + str(serviceName) + '-' + str(device) + "-" + str(thisTotalCount) + '.m'
            xrf = joblib.load("Polynomial/" + modelfile)
            themap = pd.read_csv("Polynomial/finallyResult/map.csv")
            deg = themap[themap["models"] == modelfile]["deg"].values[0]
            quadratic_featurizer = PolynomialFeatures(degree=deg)
            X_test_quadratic = quadratic_featurizer.fit_transform([[deviceCpuPercent]])
            compute = xrf.predict(X_test_quadratic)
        total1 = comm1 + compute

        comm2 = microSubvolum / (bandwidth[1] * 1024 * 1024 / 8)

        total2 = comm2 + compute

        if (total1 > total2):
            return total1
        else:
            return total2;


    def threeLatency(bandwidth, microSubvolum, serviceName, device, deviceCpuPercent,microComponent):

        comm1 = microSubvolum / (bandwidth[0] * 1024 * 1024 / 8)
        if (device == 5):
            compute = microComponent
        else:
            modelfile = "finallyResult/" + str(serviceName) + '-' + str(device) + "-" + str(thisTotalCount) + '.m'
            xrf = joblib.load("Polynomial/" + modelfile)
            themap = pd.read_csv("Polynomial/finallyResult/map.csv")
            deg = themap[themap["models"] == modelfile]["deg"].values[0]
            quadratic_featurizer = PolynomialFeatures(degree=deg)
            X_test_quadratic = quadratic_featurizer.fit_transform([[deviceCpuPercent]])
            compute = xrf.predict(X_test_quadratic)
        latency1 = comm1 + compute
        comm2 = microSubvolum / (bandwidth[1] * 1024 * 1024 / 8)

        latency2 = comm2 + compute

        comm3 = microSubvolum / (bandwidth[2] * 1024 * 1024 / 8)

        latency3 = comm3 + compute

        max = (latency1 if latency1 > latency2 else latency2) if (
                                                                     latency1 if latency1 > latency2 else latency2) > latency3 else latency3
        return max;



    for micro in oneGraphAppServices:
        microServiceName = micro.getServiceName()
        microComponent = micro.getComponent()
        microSubVolum = micro.getSubVolum()
        microSubtopic = micro.getSubTopic()
        microPubVolum = micro.getPubVolum()
        microPubTopic = micro.getPubTopic()
        microRate = micro.getRate()
        microTotalCount = micro.getTotalCount()
        flag = 0
        if micro.getIsSource():
            continue;
        totalL = float("inf")
        innodes = micro.getInnode()
        innodeSize = len(innodes)
        innodeIsCloud = 0
        upLatancys = []
        upComponents = []
        upSubVolums = []
        upSubtopics = []
        upPubVolums = []
        upPubTopics = []
        microRates = []
        upDeviceIds = []
        for innode in innodes:
            theDevice = innode.getDevice()
            upDeviceId = devichName.index(theDevice.getDeviceName())
            upDeviceIds.append(upDeviceId)
        if (micro.getServiceName() == "fault-xgboost"):
            subDevice = devices[2]
            subDeviceId = devichName.index(subDevice.getDeviceName())
            bd = [bandwidth[upDeviceIds[0]][subDeviceId]]
            subDeviceCpuPercent = (subDevice.getCPUTotal() - subDevice.getCPURemain()) / subDevice.getCPUTotal()
            # bandwidth, microSubvolum, serviceName, device, deviceCpuPercent
            tempTotal = oneLatency(
                bd, microSubVolum, microServiceName, 4, subDeviceCpuPercent,microComponent)
            micro.setDevice(devices[2])
            continue;
        if (micro.getServiceName() == "wafer-svm"):
            subDevice = devices[0]
            subDeviceId = devichName.index(subDevice.getDeviceName())
            bd = [bandwidth[upDeviceIds[0]][subDeviceId]]
            subDeviceCpuPercent = (subDevice.getCPUTotal() - subDevice.getCPURemain()) / subDevice.getCPUTotal()
            tempTotal = oneLatency(
                bd, microSubVolum, microServiceName, 2, subDeviceCpuPercent,microComponent)
            micro.setDevice(devices[0])
            continue;
        if (innodeIsCloud == 0):
            i = 0
            totalL = float("inf")
            for device in devices[0:4]:
                pubDevicefre = []
                pubDevicecpuPercent = []
                pubDevicememPercent = []
                pubDevicepubtopics = []
                pubDevicepubvolum = []
                pubDevicesubtopics = []
                pubDevicesubvolum = []
                pubDevicevolums = []
                for innode in innodes:
                    theDevice = innode.getDevice()
                    if (theDevice.getDeviceName() == device.getDeviceName()):
                        pubDevicepubtopics.append(theDevice.getPubTopic() + microPubTopic)
                        pubDevicepubvolum.append(theDevice.getPubVolum() + microPubVolum)
                        pubDevicesubtopics.append(theDevice.getSubTopic() + microSubtopic)
                        pubDevicesubvolum.append(theDevice.getSubVolum() + microSubVolum)
                        pubDevicevolums.append(theDevice.getVolums() + microPubVolum + microSubVolum)
                        pubDevicefre.append(theDevice.getFrequency())
                        pubDevicecpuPercent.append((theDevice.getCPUTotal() - (
                                theDevice.getCPURemain() - micro.getCPUDemand())) / theDevice.getCPUTotal())
                    else:
                        pubDevicepubtopics.append(theDevice.getPubTopic())
                        pubDevicepubvolum.append(theDevice.getPubVolum())
                        pubDevicesubtopics.append(theDevice.getSubTopic())
                        pubDevicesubvolum.append(theDevice.getSubVolum())
                        pubDevicevolums.append(theDevice.getVolums())
                        pubDevicefre.append(theDevice.getFrequency())
                        pubDevicecpuPercent.append(
                            (theDevice.getCPUTotal() - theDevice.getCPURemain()) / theDevice.getCPUTotal())
                if i == 0 and (micro.getServiceName() == "fault-losso"
                               or
                               micro.getServiceName() == "fault-ensemble"
                               or micro.getServiceName() == "wafer-static" or micro.getServiceName() == "wafer-ensemble"):
                    i = i + 1;
                    continue;
                if i == 2 and micro.getServiceName() == "wafer-auto":
                    i = i + 1;
                    continue;
                subDevice = device
                subDevicePubTopic = subDevice.getPubTopic() + microPubTopic
                subDevicePubVolum = subDevice.getPubVolum() + microPubVolum
                subDeviceSubTopic = subDevice.getSubTopic() + microSubtopic
                subDeviceSubVolum = subDevice.getSubVolum() + microSubVolum
                subDeviceVolums = subDevice.getVolums() + microSubVolum + microPubVolum
                subDeviceFrequency = subDevice.getFrequency()
                subDeviceCpuPercent = (subDevice.getCPUTotal() - (
                        subDevice.getCPURemain() - micro.getCPUDemand())) / subDevice.getCPUTotal()
                if (micro.getCPUDemand() <= device.getCPURemain()):

                    if (innodeSize == 1):
                        subDeviceId = devichName.index(subDevice.getDeviceName())
                        bd = [bandwidth[upDeviceIds[0]][subDeviceId]]
                        tempTotal = oneLatency(
                            bd, microSubVolum, microServiceName, subDeviceId, subDeviceCpuPercent,microComponent)

                    elif (innodeSize == 2):
                        subDeviceId = devichName.index(subDevice.getDeviceName())
                        bd = [bandwidth[upDeviceIds[0]][subDeviceId], bandwidth[upDeviceIds[1]][subDeviceId]]

                        tempTotal = twoLatency(
                            bd, microSubVolum, microServiceName, subDeviceId, subDeviceCpuPercent,microComponent)

                    elif (innodeSize == 3):
                        subDeviceId = devichName.index(subDevice.getDeviceName())
                        bd = [bandwidth[upDeviceIds[0]][subDeviceId], bandwidth[upDeviceIds[1]][subDeviceId],
                              bandwidth[upDeviceIds[2]][subDeviceId]]
                        tempTotal = threeLatency(
                            bd, microSubVolum, microServiceName, subDeviceId, subDeviceCpuPercent, microComponent)

                    if (tempTotal < totalL):
                        deviceID = i
                        flag = 1
                        totalL = tempTotal
                        micro.setDevice(device)
                        micro.setAcutalLat(totalL)
                i = i + 1

        thisDevice = devices[deviceID]
        subDevicePubTopic = thisDevice.getPubTopic() + microPubTopic
        subDevicePubVolum = thisDevice.getPubVolum() + microPubVolum
        subDeviceSubTopic = thisDevice.getSubTopic() + microSubtopic
        subDeviceSubVolum = thisDevice.getSubVolum() + microSubVolum
        subDeviceVolums = thisDevice.getVolums() + microSubVolum + microPubVolum
        subDeviceFrequency = thisDevice.getFrequency()
        thisDevice.setPubTopic(subDevicePubTopic)
        thisDevice.setPubVolum(subDevicePubVolum)
        thisDevice.setSubTopic(subDeviceSubTopic)
        thisDevice.setSubVolum(subDeviceSubVolum)
        thisDevice.setVolums(subDeviceVolums)
        thisDevice.setCPURemain(thisDevice.getCPURemain() - micro.getCPUDemand())

    flag == 0
    waferTrueLatency = []
    faultTrueLatency = []
    totalTrueLatency = []
    placementScheme = []

    microserviceName = []
    deviceNames = []
    scheme=[]
    waferDevice = []
    faultDevice = []
    for micro in oneGraphAppServices:
        if micro.getIsSource():
            continue;
        deviceName = micro.getDevice().getDeviceName()
        microserviceName.append(micro.getServiceName())
        deviceNames.append(deviceName)
        scheme.append(deviceName)
        if (micro.getServiceName().find("wafer") != -1):
            if (micro.getDevice().getDeviceName() == "cloud"):
                waferDevice.append(3)
            else:
                waferDevice.append(int(micro.getDevice().getDeviceName()[-1]))
        if (micro.getServiceName().find("fault") != -1):
            if (micro.getDevice().getDeviceName() == "cloud"):
                faultDevice.append(3)
            else:
                faultDevice.append(int(micro.getDevice().getDeviceName()[-1]))

    schemeDevice = faultDevice + waferDevice
    for placement in placements:
        mapPlace = []
        for i in placement[1:11]:
            i = int(i)
            mapPlace.append(i)
        # print(mapPlace,schemeDevice)
        if (operator.eq(mapPlace, schemeDevice)):
            # print(1)
            flag = 1
            faultTrueLatency.append(placement[-1])
            waferTrueLatency.append(placement[-2])
            totalTrueLatency.append(placement[-1] + placement[-2])
    if (flag == 0):
        faultTrueLatency.append(0)
        waferTrueLatency.append(0)
        totalTrueLatency.append(0)
    schestr = '-'
    schemeDevice = [str(x) for x in schemeDevice]
    sche = schestr.join(schemeDevice)
    placementScheme.append(sche)
    sourcelossofilename = 'result/allplacement/' + str(thisTotalCount) + '-' + thisType + '-MPC-LaTS' + str(
        s) + "-allPlacement.csv"
    features1 = ["placement"]
    features4 = ["waferTrueLatency"]
    features5 = ["faultTrueLatency"]
    features6 = ["totalTrueLatency"]
    sourceautoPD1 = pd.DataFrame(columns=features1, data=placementScheme)
    sourceautoPD4 = pd.DataFrame(columns=features4, data=waferTrueLatency)
    sourceautoPD5 = pd.DataFrame(columns=features5, data=faultTrueLatency)
    sourceautoPD6 = pd.DataFrame(columns=features6, data=totalTrueLatency)
    sourceautoPD = pd.concat([sourceautoPD1, sourceautoPD4, sourceautoPD5, sourceautoPD6],
                             axis=1)
    sourceautoPD.to_csv(sourcelossofilename)


    sourcelossofilename = 'result/infoForeachPlace/MPC-LaTS'+str(thisTotalCount)+'.csv'
    features0 = ["deviceName"]
    features1 = ["microserviceName"]
    sourceautoPD0 = pd.DataFrame(columns=features0, data=deviceNames)
    sourceautoPD1 = pd.DataFrame(columns=features1, data=microserviceName)

    sourceautoPD = pd.concat([sourceautoPD0, sourceautoPD1], axis=1)
    sourceautoPD.to_csv(sourcelossofilename)