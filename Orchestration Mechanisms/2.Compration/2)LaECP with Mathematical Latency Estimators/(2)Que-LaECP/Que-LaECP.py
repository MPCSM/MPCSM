
import pandas as pd
from sklearn.externals import joblib
import xgboost as xgb
from model.DeviceModel import Device
from model.ApplicationQueue import App
import operator
from sklearn import preprocessing
import numpy as np

datasums=[10,20,30,40,50,60,70,80]
for thisTotalCount in datasums:
    totalDeviceNumber=3
    thisType="only"
    #source、losso、knn、svm、xgboost、ensemble
    faultcomputeDemand=[0.01,2,0.4,0.75,0.02,2.05]
    #source、auto、statis、cnn、svm、ensemble
    wafercomputeDemand=[0.01,0.61,4.15,1.03,0.07,2.4]
    #0123
    devicescompute=[100,274,381,700]

    devichName=["camera","faultsensor","edge0","edge1","edge2","cloud"]
    bandwidth=[[1000,94,94,93.2,93.7,4.45],
               [93.8, 1000, 331, 93.2, 85.9, 4.36],
               [94.1, 281, 1000, 93.6, 93.7, 3.33],
               [94.6, 94.7, 94.7, 1000, 93.4, 3.80],
               [93.7, 93.4, 93.8, 93.3, 1000, 3.79],
               [3.37, 3.36, 3.18, 3.36, 3.17, 1000]]

    apps=[]
    rulPredictionLatencyCons=2;
    faultDetectionLatencyCons=1;
    waferInspectionLatencyCons=0.6;

    faultDetectionCPU=[1,2,2,2,2,2]
    faultDetectionMem=[5,1,5,5,5,5]


    waferInspectionCPU=[1,3,3,3,1,2]
    waferInspectionMem=[5,5,5,5,5,5]


    rulPredictionCPU=[1,1,3]
    rulPredictionMem=[5,5,5]



    oneGraphApp=App("oneGraph",3)


    oneGraphApp.setMicroServices([
        ["fault-source", True, False, 0, faultDetectionCPU[0], faultDetectionMem[0], 1, 7464602, 0, 0, 0.05, 1, thisTotalCount,faultcomputeDemand[0]],#0
        ["wafer-source", True, False, 0, waferInspectionCPU[0], waferInspectionCPU[0], 2, 552769, 0, 0, 0.05, 1, thisTotalCount,wafercomputeDemand[0]],#1
    #["rul-source", True, False, 0, rulPredictionCPU[0], rulPredictionMem[0], 1, 3509033, 0, 0, 0.0005, 5, 29],
        ["fault-losso", False, False, 1, faultDetectionCPU[1], faultDetectionMem[1], 3, 515318, 1, 7464602, 51, 1,thisTotalCount,faultcomputeDemand[1]],  # 1
        ["wafer-auto", False, False, 1, waferInspectionCPU[1], waferInspectionCPU[1], 1, 7132, 1, 237880, 19.2, 1,thisTotalCount,wafercomputeDemand[1]],  # 7
        ["wafer-statis", False, False, 1, waferInspectionCPU[2], waferInspectionCPU[2], 1, 36632, 1, 314889, 141, 1,thisTotalCount,wafercomputeDemand[2]],  # 8
    #["rul-preprocess", False, False, 1, rulPredictionCPU[1], rulPredictionMem[1], 1, 63565202, 1, 3509033, 0.02, 5, 29],
        ["fault-knn", False, False, 2, faultDetectionCPU[2], faultDetectionMem[2], 1, 12752, 1, 515318, 19.1, 1, thisTotalCount,faultcomputeDemand[2]],  # 2
        ["fault-svm", False, False, 2, faultDetectionCPU[3], faultDetectionMem[3], 1, 12752, 1, 515318, 1, 1,thisTotalCount,faultcomputeDemand[3]],  # 3
        ["fault-xgboost", False, False, 2, faultDetectionCPU[4], faultDetectionMem[4], 1, 12752, 1, 515318, 0.5, 1,thisTotalCount,faultcomputeDemand[4]],  # 4
        ["wafer-cnn", False, False, 2, waferInspectionCPU[3], waferInspectionCPU[3], 1, 263, 1, 7132, 34, 1, thisTotalCount,wafercomputeDemand[3]],  # 9
        ["wafer-svm", False, False, 2, waferInspectionCPU[4], waferInspectionCPU[4], 1, 611, 1, 36632, 7, 1, thisTotalCount,wafercomputeDemand[4]],  # 10
        ["fault-ensemble", False, True, 3, faultDetectionCPU[5], faultDetectionMem[5], 0, 0, 3, 12752, 49, 1,thisTotalCount,faultcomputeDemand[5]],  # 5
        ["wafer-ensemble", False, True, 3, waferInspectionCPU[5], waferInspectionCPU[5], 0, 0, 2, 611, 52, 1, thisTotalCount,wafercomputeDemand[5]],  # 11
    #["rul-prediction", False, True, 2, rulPredictionCPU[2], rulPredictionMem[2], 1, 51086, 1, 63565202, 10, 5, 29],
    ])

    oneGraphAppServices=oneGraphApp.getMicroServices()
    oneGraphAppServices[0].setAcutalLat(0)
    oneGraphAppServices[1].setAcutalLat(0)

    oneGraphAppServices[10].setLatencyRe(faultDetectionLatencyCons)
    oneGraphAppServices[11].setLatencyRe(waferInspectionLatencyCons)

    oneGraphAppServices[2].setInnode([oneGraphAppServices[0]])
    oneGraphAppServices[5].setInnode([oneGraphAppServices[2]])
    oneGraphAppServices[6].setInnode([oneGraphAppServices[2]])
    oneGraphAppServices[7].setInnode([oneGraphAppServices[2]])
    oneGraphAppServices[10].setInnode([oneGraphAppServices[5],oneGraphAppServices[6],oneGraphAppServices[7]])

    oneGraphAppServices[3].setInnode([oneGraphAppServices[1]])
    oneGraphAppServices[4].setInnode([oneGraphAppServices[1]])
    oneGraphAppServices[8].setInnode([oneGraphAppServices[3]])
    oneGraphAppServices[9].setInnode([oneGraphAppServices[4]])
    oneGraphAppServices[11].setInnode([oneGraphAppServices[8],oneGraphAppServices[9]])


    devices=[]
    #nano、ljr、miniserver、cloud
    deviceFrequency=[1.43,2.2,3.6,2.5]
    devicesCPU=[4,12,8,24]
    devicesRemain=[3,12,6,24]
    devicesMem=[100,100,100,100]

    pubTopic=[1,0,1,0]
    pubVolum=[611,0,515318,0]
    subTopic=[1,0,1,0]
    subVolum=[36632,0,12752,0]
    volums=[37243,0,528070,0]

    edge0=Device("edge0")
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
    edge0.setCompute(devicescompute[0])
    devices.append(edge0)


    edge1=Device("edge1")
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
    edge1.setCompute(devicescompute[1])
    devices.append(edge1)

    edge2=Device("edge2")
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
    edge2.setCompute(devicescompute[2])
    devices.append(edge2)

    cloud=Device("cloud")
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
    cloud.setCompute(devicescompute[3])
    devices.append(cloud)

    rulsensor=Device("rulsensor")
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
    oneGraphAppServices[2].setDevice(rulsensor)

    faultsensor=Device("faultsensor")
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

    camera=Device("camera")
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

    dataAtt=["totalCount","microComponent","microSubVolum","microSubtopic","microPubVolum","microPubTopic","microRate",
        "pubDevicepubtopics","pubDevicepubvolum","pubDevicesubtopics","pubDevicesubcvolum","pubDevicevolums","pubDevicefre","pubDevicecpuPercent",
        "subDevicePubTopic","subDevicePubVolum","subDeviceSubTopic","subDeviceSubVolum","subDeviceVolums","subDeviceFrequency","subDeviceCpuPercent","upLatency",
        "upCount","upComponent","upSubVolum","upSubtopic","upPubVolum","upPubTopic","upRate"]
    dataAttTwo=["totalCount","microComponent","microSubVolum","microSubtopic","microPubVolum","microPubTopic","microRate",
                "pubDevicepubtopics1","pubDevicepubtopics2",
                            "pubDevicepubvolum1","pubDevicepubvolum2",
                            "pubDevicesubtopics1","pubDevicesubtopics2",
                            "pubDevicesubcvolum1","pubDevicesubcvolum2",
                            "pubDevicevolums1","pubDevicevolums2",
                            "pubDevicefre1","pubDevicefre2",
                            "pubDevicecpuPercent1","pubDevicecpuPercent2",
                "subDevicePubTopic","subDevicePubVolum","subDeviceSubTopic","subDeviceSubVolum","subDeviceVolums","subDeviceFrequency","subDeviceCpuPercent","upLatency1","upLatency2",
                "upCount1","upComponent1","upSubVolum1","upSubtopic1","upPubVolum1","upPubTopic1","upRate1",
                "upCount2","upComponent2","upSubVolum2","upSubtopic2","upPubVolum2","upPubTopic2","upRate2"]
    dataAttThree=["totalCount","microComponent","microSubVolum","microSubtopic","microPubVolum","microPubTopic","microRate",
        "pubDevicepubtopics1","pubDevicepubtopics2","pubDevicepubtopics3",
                    "pubDevicepubvolum1","pubDevicepubvolum2","pubDevicepubvolum3",
                    "pubDevicesubtopics1","pubDevicesubtopics2","pubDevicesubtopics3",
                    "pubDevicesubcvolum1","pubDevicesubcvolum2","pubDevicesubcvolum3",
                    "pubDevicevolums1","pubDevicevolums2","pubDevicevolums3",
                    "pubDevicefre1","pubDevicefre2","pubDevicefre3",
                    "pubDevicecpuPercent1","pubDevicecpuPercent2","pubDevicecpuPercent3",
        "subDevicePubTopic","subDevicePubVolum","subDeviceSubTopic","subDeviceSubVolum","subDeviceVolums","subDeviceFrequency","subDeviceCpuPercent","upLatency1","upLatency2","upLatency3",
        "upCount1","upComponent1","upSubVolum1","upSubtopic1","upPubVolum1","upPubTopic1","upRate1",
        "upCount2","upComponent2","upSubVolum2","upSubtopic2","upPubVolum2","upPubTopic2","upRate2",
        "upCount3","upComponent3","upSubVolum3","upSubtopic3","upPubVolum3","upPubTopic3","upRate3"]
    def oneLatency(uplatency,bandwidth,microSubvolum,totalcount,microComputDemand,deviceCoputeTotal):
        comm = microSubvolum / (bandwidth[0]*1024*1024/8)
        compute = totalcount * (microComputDemand / deviceCoputeTotal) * (
                    1 / (deviceCoputeTotal - totalcount * microComputDemand))
        total = comm + compute
        latency = uplatency[0] + total
        return latency;

    def twoLatency(uplatency,bandwidth,microSubvolum,totalcount,microComputDemand,deviceCoputeTotal):
        comm1 = microSubvolum / (bandwidth[0]*1024*1024/8)
        compute1 = totalcount * (microComputDemand / deviceCoputeTotal) * (
                1 / (deviceCoputeTotal - totalcount * microComputDemand))
        total1 = comm1 + compute1
        latency1 = uplatency[0] + total1

        comm2 = microSubvolum / (bandwidth[1]*1024*1024/8)
        compute2 = totalcount * (microComputDemand / deviceCoputeTotal) * (
                1 / (deviceCoputeTotal - totalcount * microComputDemand))
        total2 = comm2 + compute2
        latency2 = uplatency[1] + total2

        if (latency1 > latency2):
            return latency1
        else:
            return latency2;
    def threeLatency(uplatency,bandwidth,microSubvolum,totalcount,microComputDemand,deviceCoputeTotal):
        comm1 = microSubvolum / (bandwidth[0]*1024*1024/8)
        compute1 = totalcount * (microComputDemand / deviceCoputeTotal) * (
                1 / (deviceCoputeTotal - totalcount * microComputDemand))
        total1 = comm1 + compute1
        latency1 = uplatency[0] + total1

        comm2 = microSubvolum / (bandwidth[1]*1024*1024/8)
        compute2 = totalcount * (microComputDemand / deviceCoputeTotal) * (
                1 / (deviceCoputeTotal - totalcount * microComputDemand))
        total2 = comm2 + compute2
        latency2 = uplatency[1] + total2

        comm3 = microSubvolum / (bandwidth[2]*1024*1024/8)
        compute3 = totalcount * (microComputDemand / deviceCoputeTotal) * (
                1 / (deviceCoputeTotal - totalcount * microComputDemand))
        total3 = comm3 + compute3
        latency3 = uplatency[2] + total3

        max = (latency1 if latency1 > latency2 else latency2) if (
                                                                     latency1 if latency1 > latency2 else latency2) > latency3 else latency3
        return max;

    thisServices=oneGraphApp.getMicroServices()
    for micro in thisServices:
        microComputeDemand=micro.getComponent()
        microSubVolum=micro.getSubVolum()
        flag=0
        if micro.getIsSource():
            continue;
        totalL=float("inf")
        innodes = micro.getInnode()
        innodeSize=len(innodes)
        innodeIsCloud=0
        upLatancys=[]

        upDeviceIds=[]
        for innode in innodes:
            upLatancy = innode.getAcutalLat()
            upLatancys.append(upLatancy)
            theDevice = innode.getDevice()
            upDeviceId=devichName.index(theDevice.getDeviceName())
            upDeviceIds.append(upDeviceId)

            if(theDevice.getDeviceName()=="cloud"):
                innodeIsCloud=1
        if (micro.getServiceName() == "fault-xgboost"):
            subDevice = devices[2]
            subDeviceId=devichName.index(subDevice.getDeviceName())
            bd=[bandwidth[upDeviceIds[0]][subDeviceId]]
            subDevicecompute=subDevice.getCompute()
            tempTotal = oneLatency(
                upLatancys, bd, microSubVolum,thisTotalCount,microComputeDemand,subDevicecompute)

            micro.setDevice(devices[2])
            micro.setAcutalLat(tempTotal)
            continue;
        if (micro.getServiceName() == "wafer-svm"):
            subDevice = devices[0]
            subDeviceId = devichName.index(subDevice.getDeviceName())
            bd = [bandwidth[upDeviceIds[0]][subDeviceId]]
            subDevicecompute = subDevice.getCompute()
            tempTotal = oneLatency(
                upLatancys, bd, microSubVolum, thisTotalCount, microComputeDemand, subDevicecompute)
            micro.setDevice(devices[0])
            micro.setAcutalLat(tempTotal)
            continue;
        if (innodeIsCloud == 0):

            i=0
            totalL=float("inf")
            for device in devices[0:totalDeviceNumber]:
                if i == 0 and (micro.getServiceName() == "fault-losso"
                               or
                               micro.getServiceName() == "fault-ensemble"
                               or micro.getServiceName() == "wafer-statis" or micro.getServiceName() == "wafer-ensemble"):
                    i = i + 1;
                    continue;
                if i == 2 and micro.getServiceName() == "wafer-auto":
                    i = i + 1;
                    continue;
                subDevice = device
                if (micro.getCPUDemand()<=device.getCPURemain()):

                    if(innodeSize==1):
                        subDeviceId = devichName.index(subDevice.getDeviceName())
                        print("upDeviceIds[0],",upDeviceIds[0],subDeviceId)
                        bd = [bandwidth[upDeviceIds[0]][subDeviceId]]
                        subDevicecompute = subDevice.getCompute()
                        tempTotal = oneLatency(
                            upLatancys, bd, microSubVolum, thisTotalCount, microComputeDemand, subDevicecompute)

                    elif(innodeSize==2):
                        subDeviceId = devichName.index(subDevice.getDeviceName())
                        bd = [bandwidth[upDeviceIds[0]][subDeviceId],bandwidth[upDeviceIds[1]][subDeviceId]]
                        subDevicecompute = subDevice.getCompute()
                        tempTotal = twoLatency(
                            upLatancys, bd, microSubVolum, thisTotalCount, microComputeDemand, subDevicecompute)

                    elif (innodeSize == 3):
                        subDeviceId = devichName.index(subDevice.getDeviceName())
                        bd = [bandwidth[upDeviceIds[0]][subDeviceId], bandwidth[upDeviceIds[1]][subDeviceId],bandwidth[upDeviceIds[2]][subDeviceId]]
                        subDevicecompute = subDevice.getCompute()
                        tempTotal = threeLatency(
                            upLatancys, bd, microSubVolum, thisTotalCount, microComputeDemand, subDevicecompute)

                    if(tempTotal<totalL):
                        deviceID=i
                        flag=1
                        totalL=tempTotal
                        micro.setDevice(device)
                        micro.setAcutalLat(totalL)
                i=i+1
        if(flag==0 or innodeIsCloud==1):
            deviceID=3
            subDevice = devices[3]

            if (innodeSize == 1):
                subDeviceId = devichName.index(subDevice.getDeviceName())
                bd = [bandwidth[upDeviceIds[0]][subDeviceId]]
                subDevicecompute = subDevice.getCompute()
                tempTotal = oneLatency(
                    upLatancys, bd, microSubVolum, thisTotalCount, microComputeDemand, subDevicecompute)

            elif (innodeSize == 2):
                subDeviceId = devichName.index(subDevice.getDeviceName())
                bd = [bandwidth[upDeviceIds[0]][subDeviceId], bandwidth[upDeviceIds[1]][subDeviceId]]
                subDevicecompute = subDevice.getCompute()
                tempTotal = twoLatency(
                    upLatancys, bd, microSubVolum, thisTotalCount, microComputeDemand, subDevicecompute)

            elif (innodeSize == 3):
                subDeviceId = devichName.index(subDevice.getDeviceName())
                bd = [bandwidth[upDeviceIds[0]][subDeviceId], bandwidth[upDeviceIds[1]][subDeviceId],
                      bandwidth[upDeviceIds[2]][subDeviceId]]
                subDevicecompute = subDevice.getCompute()
                tempTotal = threeLatency(
                    upLatancys, bd, microSubVolum, thisTotalCount, microComputeDemand, subDevicecompute)

            micro.setDevice(devices[3])
            micro.setAcutalLat(tempTotal)

        thisDevice=devices[deviceID]
        thisDevice.setCPURemain(thisDevice.getCPURemain() - micro.getCPUDemand())

    dataAtt=["serviceName","deviceName","latency"]
    data=[]
    for micro in thisServices:
        if micro.getIsSource():
            continue;
        data.append([micro.getServiceName(),micro.getDevice().getDeviceName(),micro.getAcutalLat()])
    dataPD=pd.DataFrame(columns=dataAtt,data=data)
    print(dataPD)
    dataPD.to_csv('result/infoForeachPlace/Que-LaECP-'+str(thisTotalCount)+'.csv')

    waferDevice=[]
    faultDevice=[]
    for micro in thisServices:
        if micro.getIsSource():
            continue;
        if (micro.getServiceName().find("wafer") != -1):
            if (micro.getDevice().getDeviceName() == "cloud"):
                waferDevice.append(3)
            else:
                waferDevice.append(int(micro.getDevice().getDeviceName()[-1]))
        if (micro.getServiceName().find("fault") != -1):
            if(micro.getDevice().getDeviceName()=="cloud"):
                faultDevice.append(3)
            else:
                faultDevice.append(int(micro.getDevice().getDeviceName()[-1]))

    schemeDevice=faultDevice+waferDevice
    flag=0
    placements = pd.read_csv(str(thisTotalCount)+"-placementInfo.csv").values
    faultTrueLatency=[]
    waferTrueLatency=[]
    totalTrueLatency=[]
    placementScheme=[]
    for placement in placements:
        mapPlace=[]
        for i in placement[1:11]:
            i = int(i)
            mapPlace.append(i)
        #print(mapPlace,schemeDevice)
        if (operator.eq(mapPlace,schemeDevice)):
            #print(1)
            flag=1
            faultTrueLatency.append(placement[-1])
            waferTrueLatency.append(placement[-2])
            totalTrueLatency.append(placement[-1]+placement[-2])
    #print(flag)
    if(flag==0):
        faultTrueLatency.append(0)
        waferTrueLatency.append(0)
        totalTrueLatency.append(0)

    schestr = '-'
    schemeDevice = [str(x) for x in schemeDevice]
    sche = schestr.join(schemeDevice)
    placementScheme.append(sche)

    sourcelossofilename = 'result/allplacement/' + str(thisTotalCount) +"-Que-LaECP.csv"
    features1=["placement"]
    features4=["waferTrueLatency"]
    features5=["faultTrueLatency"]
    features6=["totalTrueLatency"]
    sourceautoPD1 = pd.DataFrame(columns=features1, data=placementScheme)
    sourceautoPD4 = pd.DataFrame(columns=features4, data=waferTrueLatency)
    sourceautoPD5 = pd.DataFrame(columns=features5, data=faultTrueLatency)
    sourceautoPD6 = pd.DataFrame(columns=features6, data=totalTrueLatency)
    sourceautoPD = pd.concat([sourceautoPD1, sourceautoPD4,sourceautoPD5,sourceautoPD6], axis=1)
    sourceautoPD.to_csv(sourcelossofilename)