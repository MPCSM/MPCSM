
import pandas as pd
from sklearn.externals import joblib
import xgboost as xgb
from model.DeviceModel import Device
from model.Application import App
from sklearn import preprocessing
import operator
import numpy as np

itermax=1

s = 1

datasums=[10,20,30,40,50,60,70,80]
for thisTotalCount in datasums:

    placements = pd.read_csv(str(thisTotalCount)+"-placementInfo.csv").values
    thisType="mix"
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
        ["fault-source", True, False, 0, faultDetectionCPU[0], faultDetectionMem[0], 1, 7464602, 0, 0, 0.05, 1, thisTotalCount],#0
        ["wafer-source", True, False, 0, waferInspectionCPU[0], waferInspectionCPU[0], 2, 552769, 0, 0, 0.05, 1, thisTotalCount],#1
    #["rul-source", True, False, 0, rulPredictionCPU[0], rulPredictionMem[0], 1, 3509033, 0, 0, 0.0005, 5, 29],
        ["fault-losso", False, False, 1, faultDetectionCPU[1], faultDetectionMem[1], 3, 515318 * 3, 1, 7464602, 51, 1,thisTotalCount],  # 1
        ["wafer-auto", False, False, 1, waferInspectionCPU[1], waferInspectionCPU[1], 1, 7132, 1, 237880, 19.2, 1,thisTotalCount],  # 7
        ["wafer-statis", False, False, 1, waferInspectionCPU[2], waferInspectionCPU[2], 1, 36632, 1, 314889, 141, 1,thisTotalCount],  # 8
    #["rul-preprocess", False, False, 1, rulPredictionCPU[1], rulPredictionMem[1], 1, 63565202, 1, 3509033, 0.02, 5, 29],
        ["fault-knn", False, False, 2, faultDetectionCPU[2], faultDetectionMem[2], 1, 12752, 1, 515318, 19.1, 1, thisTotalCount],  # 2
        ["fault-svm", False, False, 2, faultDetectionCPU[3], faultDetectionMem[3], 1, 12752, 1, 515318, 1, 1,thisTotalCount],  # 3
        ["fault-xgboost", False, False, 2, faultDetectionCPU[4], faultDetectionMem[4], 1, 12752, 1, 515318, 0.5, 1,thisTotalCount],  # 4
        ["wafer-cnn", False, False, 2, waferInspectionCPU[3], waferInspectionCPU[3], 1, 263, 1, 7132, 34, 1, thisTotalCount],  # 9
        ["wafer-svm", False, False, 2, waferInspectionCPU[4], waferInspectionCPU[4], 1, 611, 1, 36632, 7, 1, thisTotalCount],  # 10
        ["fault-ensemble", False, True, 3, faultDetectionCPU[5], faultDetectionMem[5], 0, 0, 3, 12752 * 3, 49, 1,thisTotalCount],  # 5
        ["wafer-ensemble", False, True, 3, waferInspectionCPU[5], waferInspectionCPU[5], 0, 0, 2, 874, 52, 1, thisTotalCount],  # 11
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
    def oneLatency(X):
        dataPD = pd.DataFrame(columns=dataAtt, data=[X])
        attribute = dataPD.drop(
            columns=['microPubTopic', 'pubDevicefre', 'upComponent', 'upPubVolum', 'upSubVolum', 'upPubTopic',
                     'microSubtopic', 'microRate', 'pubDevicesubtopics', 'upRate'])
        print(attribute)
        lbl = preprocessing.LabelEncoder()
        attribute['upLatency'] = lbl.fit_transform(attribute['upLatency'].astype(str))  # 将提示的包含错误数据类型这一列进行转换
        xrf = joblib.load('xgboostModel/'+str(thisTotalCount)+'-'+thisType+'-onexgboost.pkl')
        dpredict = xgb.DMatrix(attribute)
       ######
        prediction = xrf.predict(dpredict, ntree_limit=xrf.best_ntree_limit)
        ###print(prediction)
        return prediction;
    def twoLatency(X):
        dataPD = pd.DataFrame(columns=dataAttTwo, data=[X])
        attribute = dataPD[['upLatency1', 'upLatency2', 'totalCount', 'pubDevicesubcvolum1', 'pubDevicepubtopics1',
                               'pubDevicepubvolum1',
                               'upCount1', 'pubDevicecpubvolum2', 'pubDevicesubtopics1', 'pubDevicecpuPercent1',
                               'subDevicePubTopic', 'subDevicePubVolum',
                               'pubDevicesubcvolum2', 'subDeviceSubVolum', 'pubDevicevolums1', 'pubDevicefre1',
                               'subDeviceFrequency', 'pubDevicesubtopics2',
                               'pubDevicecpuPercent2', 'subDeviceSubTopic', 'pubDevicepubtopics2',
                               'subDeviceCpuPercent', 'upCount2', 'subDeviceVolums']]

        lbl = preprocessing.LabelEncoder()
        
        attribute['upLatency1'] = lbl.fit_transform(attribute['upLatency1'].astype(str))
        attribute['upLatency2'] = lbl.fit_transform(attribute['upLatency2'].astype(str))
        xrf = joblib.load('xgboostModel/'+str(thisTotalCount)+'-'+thisType+'-twoxgboost.pkl')
        dpredict = xgb.DMatrix(attribute)
        prediction = xrf.predict(dpredict, ntree_limit=xrf.best_ntree_limit)
        return prediction;
    def threeLatency(X):
        dataPD = pd.DataFrame(columns=dataAttThree, data=[X])
        attribute = dataPD[
            ['upLatency1', 'upLatency2', 'totalCount', 'upLatency3', 'subDevicePubVolum', 'pubDevicepubvolum1',
             'pubDevicesubcvolum1',
             'subDeviceSubVolum', 'pubDevicepubvolum2', 'pubDevicesubcvolum3', 'pubDevicesubcvolum2', 'upCount1',
             'pubDevicesubtopics3',
             'pubDevicesubtopics1', 'pubDevicecpuPercent2', 'pubDevicecpuPercent1', 'pubDevicepubvolum3',
             'pubDevicesubtopics2',
             'pubDevicecpuPercent3', 'subDeviceSubTopic', 'pubDevicepubtopics2', 'pubDevicepubtopics1',
             'subDeviceCpuPercent',
             'subDevicePubTopic', 'upCount2', 'subDeviceVolums', 'pubDevicevolums3', 'pubDevicepubtopics3',
             'pubDevicevolums1', 'pubDevicevolums2',
             'pubDevicefre2', 'subDeviceFrequency', 'pubDeviceFrequency', 'pubDevicefre1']]
        print(attribute)
        lbl = preprocessing.LabelEncoder()
        attribute['upLatency1'] = lbl.fit_transform(attribute['upLatency1'].astype(str))
        attribute['upLatency2'] = lbl.fit_transform(attribute['upLatency2'].astype(str))
        attribute['upLatency3'] = lbl.fit_transform(attribute['upLatency3'].astype(str)) 
        xrf = joblib.load('xgboostModel/'+str(thisTotalCount)+'-'+thisType+'-threexgboost.pkl')
        dpredict = xgb.DMatrix(attribute)
        prediction = xrf.predict(dpredict, ntree_limit=xrf.best_ntree_limit)
        return prediction;

    thisServices=oneGraphApp.getMicroServices()

    for micro in thisServices:
        microComponent=micro.getComponent()
        microSubVolum=micro.getSubVolum()
        microSubtopic=micro.getSubTopic()
        microPubVolum=micro.getPubVolum()
        microPubTopic=micro.getPubTopic()
        microRate=micro.getRate()
        microTotalCount = micro.getTotalCount()
        flag=0
        if micro.getIsSource():
            continue;
        totalL=float("inf")
        innodes = micro.getInnode()
        innodeSize=len(innodes)
        innodeIsCloud=0
        upLatancys=[]
        upComponents=[]
        upSubVolums=[]
        upSubtopics=[]
        upPubVolums=[]
        upPubTopics=[]
        microRates=[]
        for innode in innodes:
            upLatancy = innode.getAcutalLat()
            #print("microName",micro.getServiceName(),innode.getServiceName(),upLatancy)
            upLatancys.append(upLatancy)
            microRate=innode.getRate()
            upComponent = innode.getComponent()
            upSubVolum= innode.getSubVolum()
            upSubtopic = innode.getSubTopic()
            upPubVolum = innode.getPubVolum()
            upPubTopic = innode.getPubTopic()
            upComponents.append(upComponent)
            upSubVolums.append(upSubVolum)
            upSubtopics.append(upSubtopic)
            upPubVolums.append(upPubVolum)
            upPubTopics.append(upPubTopic)
            microRates.append(microRate)
            theDevice = innode.getDevice()
            if(theDevice.getDeviceName()=="cloud"):
                innodeIsCloud=1
        if (micro.getServiceName() == "fault-xgboost"):
            subDevice = devices[2]
            # cpu,pubtopics,pubvolum,subtopics,subvolum,volums
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
                pubDevicepubtopics.append(theDevice.getPubTopic())
                pubDevicepubvolum.append(theDevice.getPubVolum())
                pubDevicesubtopics.append(theDevice.getSubTopic())
                pubDevicesubvolum.append(theDevice.getSubVolum())
                pubDevicevolums.append(theDevice.getVolums())
                pubDevicefre.append(theDevice.getFrequency())
                pubDevicecpuPercent.append((theDevice.getCPUTotal() - theDevice.getCPURemain()) / theDevice.getCPUTotal())
            subDevicePubTopic = subDevice.getPubTopic()
            subDevicePubVolum = subDevice.getPubVolum()
            subDeviceSubTopic = subDevice.getSubTopic()
            subDeviceSubVolum = subDevice.getSubVolum()
            subDeviceVolums = subDevice.getVolums()
            subDeviceFrequency = subDevice.getFrequency()
            subDeviceCpuPercent = (subDevice.getCPUTotal() - subDevice.getCPURemain() ) / subDevice.getCPUTotal()

            tempTotal = oneLatency(
                [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                 microRate,
                 pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                 pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                 pubDevicecpuPercent[0],
                 subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                 subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent,upLatancys[0],microTotalCount,upComponents[0],upSubVolums[0],upSubtopics[0],upPubVolums[0],upPubTopics[0],
                 microRates[0]]
                );
            micro.setDevice(devices[2])
            micro.setAcutalLat(tempTotal)
            continue;
        if (micro.getServiceName() == "wafer-svm"):
            subDevice = devices[0]
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
                pubDevicepubtopics.append(theDevice.getPubTopic())
                pubDevicepubvolum.append(theDevice.getPubVolum())
                pubDevicesubtopics.append(theDevice.getSubTopic())
                pubDevicesubvolum.append(theDevice.getSubVolum())
                pubDevicevolums.append(theDevice.getVolums())
                pubDevicefre.append(theDevice.getFrequency())
                pubDevicecpuPercent.append((theDevice.getCPUTotal() - theDevice.getCPURemain()) / theDevice.getCPUTotal())
            subDevicePubTopic = subDevice.getPubTopic()
            subDevicePubVolum = subDevice.getPubVolum()
            subDeviceSubTopic = subDevice.getSubTopic()
            subDeviceSubVolum = subDevice.getSubVolum()
            subDeviceVolums = subDevice.getVolums()
            subDeviceFrequency = subDevice.getFrequency()
            subDeviceCpuPercent = (subDevice.getCPUTotal() - subDevice.getCPURemain()) / subDevice.getCPUTotal()

            tempTotal = oneLatency(
                [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                 microRate,
                 pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                 pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                 pubDevicecpuPercent[0],
                 subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                 subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent,upLatancys[0],microTotalCount,upComponents[0],upSubVolums[0],upSubtopics[0],upPubVolums[0],upPubTopics[0],
                 microRates[0]]
            );

            micro.setDevice(devices[0])
            micro.setAcutalLat(tempTotal)
            continue;
        if (innodeIsCloud == 0):
            i=0
            totalL=float("inf")
            for device in devices[0:3]:
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
                    if(theDevice.getDeviceName()==device.getDeviceName()):
                        pubDevicepubtopics.append(theDevice.getPubTopic()+microPubTopic)
                        pubDevicepubvolum.append(theDevice.getPubVolum()+microPubVolum)
                        pubDevicesubtopics.append(theDevice.getSubTopic()+microSubtopic)
                        pubDevicesubvolum.append(theDevice.getSubVolum()+microSubVolum)
                        pubDevicevolums.append(theDevice.getVolums()+microPubVolum+microSubVolum)
                        pubDevicefre.append(theDevice.getFrequency())
                        pubDevicecpuPercent.append((theDevice.getCPUTotal() - (theDevice.getCPURemain() - micro.getCPUDemand())) / theDevice.getCPUTotal())
                    else:
                        pubDevicepubtopics.append(theDevice.getPubTopic())
                        pubDevicepubvolum.append(theDevice.getPubVolum())
                        pubDevicesubtopics.append(theDevice.getSubTopic())
                        pubDevicesubvolum.append(theDevice.getSubVolum())
                        pubDevicevolums.append(theDevice.getVolums())
                        pubDevicefre.append(theDevice.getFrequency())
                        pubDevicecpuPercent.append((theDevice.getCPUTotal() - theDevice.getCPURemain()) / theDevice.getCPUTotal())
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
                subDevicePubTopic = subDevice.getPubTopic() + microPubTopic
                subDevicePubVolum = subDevice.getPubVolum() + microPubVolum
                subDeviceSubTopic = subDevice.getSubTopic() + microSubtopic
                subDeviceSubVolum = subDevice.getSubVolum() + microSubVolum
                subDeviceVolums = subDevice.getVolums() + microSubVolum + microPubVolum
                subDeviceFrequency = subDevice.getFrequency()
                subDeviceCpuPercent = ( subDevice.getCPUTotal()-(subDevice.getCPURemain()-micro.getCPUDemand()))/ subDevice.getCPUTotal()
                if (micro.getCPUDemand()<=device.getCPURemain()):
                    if(innodeSize==1):
                        tempTotal = oneLatency(
                           [ microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                            microRate,
                            pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                            pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                            pubDevicecpuPercent[0],
                            subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                            subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent, upLatancys[0], microTotalCount,
                            upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                            microRates[0]]);
                    elif(innodeSize==2):
                        tempTotal = twoLatency([microTotalCount,microComponent,microSubVolum,microSubtopic,microPubVolum,microPubTopic,microRate,
                        pubDevicepubtopics[0],pubDevicepubtopics[1],
                        pubDevicepubvolum[0],pubDevicepubvolum[1],
                        pubDevicesubtopics[0],pubDevicesubtopics[1],
                        pubDevicesubvolum[0],pubDevicesubvolum[1],
                        pubDevicevolums[0],pubDevicevolums[1],
                        pubDevicefre[0],pubDevicefre[1],
                        pubDevicecpuPercent[0],pubDevicecpuPercent[1],

                        subDevicePubTopic,subDevicePubVolum,subDeviceSubTopic,subDeviceSubVolum,subDeviceVolums,subDeviceFrequency,subDeviceCpuPercent
                        , upLatancys[0], upLatancys[1],microTotalCount,upComponents[0],upSubVolums[0],upSubtopics[0],upPubVolums[0],upPubTopics[0], microRates[0]
    ,                    microTotalCount, upComponents[1],upSubVolums[1],upSubtopics[1],upPubVolums[1],upPubTopics[1],
                                                microRates[1],
                                                ]);

                    elif (innodeSize == 3):
                        tempTotal = threeLatency([microTotalCount,microComponent,microSubVolum,microSubtopic,microPubVolum,microPubTopic,microRate,
                        pubDevicepubtopics[0],pubDevicepubtopics[1],pubDevicepubtopics[2],
                        pubDevicepubvolum[0],pubDevicepubvolum[1],pubDevicepubvolum[2],
                        pubDevicesubtopics[0],pubDevicesubtopics[1],pubDevicesubtopics[2],
                        pubDevicesubvolum[0],pubDevicesubvolum[1],pubDevicesubvolum[2],
                        pubDevicevolums[0],pubDevicevolums[1],pubDevicevolums[2],
                        pubDevicefre[0],pubDevicefre[1],pubDevicefre[2],
                        pubDevicecpuPercent[0],pubDevicecpuPercent[1],pubDevicecpuPercent[2],
                        subDevicePubTopic,subDevicePubVolum,subDeviceSubTopic,subDeviceSubVolum,subDeviceVolums,subDeviceFrequency,subDeviceCpuPercent
                        ,upLatancys[0],upLatancys[1],upLatancys[2],
                                                  microTotalCount,upComponents[0],upSubVolums[0],upSubtopics[0],upPubVolums[0],upPubTopics[0],  microRates[0],
                                                  microTotalCount, upComponents[1],upSubVolums[1],upSubtopics[1],upPubVolums[1],upPubTopics[1],  microRates[1],
                                                  microTotalCount,upComponents[2],upSubVolums[2],upSubtopics[2],upPubVolums[2],upPubTopics[2],  microRates[2],
                                                  ]);

                    if(tempTotal<totalL):
                        deviceID=i
                        flag=1
                        totalL=tempTotal
                        micro.setDevice(device)
                        micro.setAcutalLat(totalL)
                i=i+1
        if(flag==0 or innodeIsCloud==1):
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
                if (theDevice.getDeviceName() == "cloud"):
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
            subDevice = devices[3]
            subDevicePubTopic = subDevice.getPubTopic() + microPubTopic
            subDevicePubVolum = subDevice.getPubVolum() + microPubVolum
            subDeviceSubTopic = subDevice.getSubTopic() + microSubtopic
            subDeviceSubVolum = subDevice.getSubVolum() + microSubVolum
            subDeviceVolums = subDevice.getVolums() + microSubVolum + microPubVolum
            subDeviceFrequency = subDevice.getFrequency()
            subDeviceCpuPercent = (subDevice.getCPUTotal() - (
                        subDevice.getCPURemain() - micro.getCPUDemand())) / subDevice.getCPUTotal()
            subDeviceMemPercent = (subDevice.getMemTotal() - (
                        subDevice.getMemRemain() - micro.getMemDemand())) / subDevice.getMemTotal()
            deviceID = 3
            if (innodeSize == 1):
                tempTotal = oneLatency([microTotalCount,microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                                             microRate,
                                             pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                                             pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                                             pubDevicecpuPercent[0],
                                             subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                                             subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent
                                            ,upLatancys[0], microTotalCount, upComponents[0],upSubVolums[0],upSubtopics[0],upPubVolums[0],upPubTopics[0],
                                        microRates[0]]
                                            );
                # tempTotal = innodes[0].getAcutalLat() + temponehop
            elif (innodeSize == 2):
                tempTotal = twoLatency([microTotalCount,microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                                             microRate,
                                             pubDevicepubtopics[0], pubDevicepubtopics[1],
                                             pubDevicepubvolum[0], pubDevicepubvolum[1],
                                             pubDevicesubtopics[0], pubDevicesubtopics[1],
                                             pubDevicesubvolum[0], pubDevicesubvolum[1],
                                             pubDevicevolums[0], pubDevicevolums[1],
                                             pubDevicefre[0], pubDevicefre[1],
                                             pubDevicecpuPercent[0], pubDevicecpuPercent[1],

                                             subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                                             subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent,upLatancys[0],upLatancys[1],
                                        microTotalCount, upComponents[0],upSubVolums[0],upSubtopics[0],upPubVolums[0],upPubTopics[0],
                                         microRates[0],
                                        microTotalCount, upComponents[1],upSubVolums[1],upSubtopics[1],upPubVolums[1],upPubTopics[1],
                                        microRates[1],


                                        ]
                                             );
            elif (innodeSize == 3):
                tempTotal = threeLatency([microTotalCount,microComponent, microSubVolum, microSubtopic, microPubVolum,
                                               microPubTopic, microRate,
                                               pubDevicepubtopics[0], pubDevicepubtopics[1], pubDevicepubtopics[2],
                                               pubDevicepubvolum[0], pubDevicepubvolum[1], pubDevicepubvolum[2],
                                               pubDevicesubtopics[0], pubDevicesubtopics[1], pubDevicesubtopics[2],
                                               pubDevicesubvolum[0], pubDevicesubvolum[1], pubDevicesubvolum[2],
                                               pubDevicevolums[0], pubDevicevolums[1], pubDevicevolums[2],
                                               pubDevicefre[0], pubDevicefre[1], pubDevicefre[2],
                                               pubDevicecpuPercent[0], pubDevicecpuPercent[1], pubDevicecpuPercent[2],

                                               subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic,
                                               subDeviceSubVolum, subDeviceVolums, subDeviceFrequency,
                                               subDeviceCpuPercent,upLatancys[0],upLatancys[1],upLatancys[2],
                                          microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0],
                                          upPubTopics[0],
                                          microRates[0],
                                          microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1], upPubVolums[1],
                                          upPubTopics[1],
                                          microRates[1],
                                          microTotalCount, upComponents[2], upSubVolums[2], upSubtopics[2], upPubVolums[2],
                                          upPubTopics[0],
                                           microRates[2],


                                          ]);
            micro.setDevice(devices[3])
            micro.setAcutalLat(tempTotal)
        thisDevice=devices[deviceID]
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

    iter=0
    placementScheme = []
    waferensembleLatency = []
    faultensembleLatency = []
    waferTrueLatency=[]
    faultTrueLatency=[]
    totalTrueLatency=[]
    while(iter<itermax):
        microserviceName = []
        deviceNames = []
        tempLatency = []
        fianlLatency = []
        thisServices =oneGraphApp.getMicroServices()
        scheme=[]
        for micro in thisServices:
            if micro.getIsSource():
                continue;
            deviceName = micro.getDevice().getDeviceName()
            microserviceName.append(micro.getServiceName())
            deviceNames.append(deviceName)
            tempLatency.append(micro.getAcutalLat())
            scheme.append(deviceName)

        diffL={}
        for micro in thisServices:
            microComponent = micro.getComponent()
            microSubVolum = micro.getSubVolum()
            microSubtopic = micro.getSubTopic()
            microPubVolum = micro.getPubVolum()
            microPubTopic = micro.getPubTopic()
            microRate = micro.getRate()
            microTotalCount = micro.getTotalCount()
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
            pubDevicefre = []
            pubDevicecpuPercent = []
            pubDevicememPercent = []
            pubDevicepubtopics = []
            pubDevicepubvolum = []
            pubDevicesubtopics = []
            pubDevicesubvolum = []
            pubDevicevolums = []
            for innode in innodes:
                upLatancy = innode.getAcutalLat()
                upLatancys.append(upLatancy)
                microRate = innode.getRate()
                upComponent = innode.getComponent()
                upSubVolum = innode.getSubVolum()
                upSubtopic = innode.getSubTopic()
                upPubVolum = innode.getPubVolum()
                upPubTopic = innode.getPubTopic()
                upComponents.append(upComponent)
                upSubVolums.append(upSubVolum)
                upSubtopics.append(upSubtopic)
                upPubVolums.append(upPubVolum)
                upPubTopics.append(upPubTopic)
                microRates.append(microRate)
                theDevice = innode.getDevice()
                pubDevicepubtopics.append(theDevice.getPubTopic())
                pubDevicepubvolum.append(theDevice.getPubVolum())
                pubDevicesubtopics.append(theDevice.getSubTopic())
                pubDevicesubvolum.append(theDevice.getSubVolum())
                pubDevicevolums.append(theDevice.getVolums())
                pubDevicefre.append(theDevice.getFrequency())
                pubDevicecpuPercent.append((theDevice.getCPUTotal() - theDevice.getCPURemain()) / theDevice.getCPUTotal())
            subDevice = micro.getDevice()
            subDevicePubTopic = subDevice.getPubTopic()
            subDevicePubVolum = subDevice.getPubVolum()
            subDeviceSubTopic = subDevice.getSubTopic()
            subDeviceSubVolum = subDevice.getSubVolum()
            subDeviceVolums = subDevice.getVolums()
            subDeviceFrequency = subDevice.getFrequency()
            subDeviceCpuPercent = (subDevice.getCPUTotal() -
                        subDevice.getCPURemain() ) / subDevice.getCPUTotal()

            if (innodeSize == 1):
                tempTotal = oneLatency(
                    [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                     microRate,
                     pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                     pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                     pubDevicecpuPercent[0],
                     subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                     subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent, upLatancys[0], microTotalCount,
                     upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                     microRates[0]]);
            elif (innodeSize == 2):
                tempTotal = twoLatency(
                    [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic, microRate,
                     pubDevicepubtopics[0], pubDevicepubtopics[1],
                     pubDevicepubvolum[0], pubDevicepubvolum[1],
                     pubDevicesubtopics[0], pubDevicesubtopics[1],
                     pubDevicesubvolum[0], pubDevicesubvolum[1],
                     pubDevicevolums[0], pubDevicevolums[1],
                     pubDevicefre[0], pubDevicefre[1],
                     pubDevicecpuPercent[0], pubDevicecpuPercent[1],

                     subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum, subDeviceVolums,
                     subDeviceFrequency, subDeviceCpuPercent
                        , upLatancys[0], upLatancys[1], microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0],
                     upPubVolums[0], upPubTopics[0], microRates[0]
                        , microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1], upPubVolums[1], upPubTopics[1],
                     microRates[1],
                     ]);
            elif (innodeSize == 3):
                tempTotal = threeLatency(
                    [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic, microRate,
                     pubDevicepubtopics[0], pubDevicepubtopics[1], pubDevicepubtopics[2],
                     pubDevicepubvolum[0], pubDevicepubvolum[1], pubDevicepubvolum[2],
                     pubDevicesubtopics[0], pubDevicesubtopics[1], pubDevicesubtopics[2],
                     pubDevicesubvolum[0], pubDevicesubvolum[1], pubDevicesubvolum[2],
                     pubDevicevolums[0], pubDevicevolums[1], pubDevicevolums[2],
                     pubDevicefre[0], pubDevicefre[1], pubDevicefre[2],
                     pubDevicecpuPercent[0], pubDevicecpuPercent[1], pubDevicecpuPercent[2],

                     subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum, subDeviceVolums,
                     subDeviceFrequency, subDeviceCpuPercent
                        , upLatancys[0], upLatancys[1], upLatancys[2],
                     microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                     microRates[0],
                     microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1], upPubVolums[1], upPubTopics[1],
                     microRates[1],
                     microTotalCount, upComponents[2], upSubVolums[2], upSubtopics[2], upPubVolums[2], upPubTopics[2],
                     microRates[2],

                     ]);
            diff = abs(tempTotal - micro.getAcutalLat())
            #print("microName,initalLatency,finalLatency", micro.getAcutalLat(),tempTotal)
            micro.setAcutalLat(tempTotal)
            micro.setDiffLatency(diff)
            diffL[micro.getServiceName()] = diff
        waferDevice = []
        faultDevice = []
        for micro in thisServices:
            if micro.getIsSource():
                continue;
            fianlLatency.append(micro.getAcutalLat())
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
            if (micro.getServiceName() == "wafer-ensemble"):
                waferensembleLatency.append(micro.getAcutalLat())
            if (micro.getServiceName() == "fault-ensemble"):
                faultensembleLatency.append(micro.getAcutalLat())
        sourcelossofilename =  'result/infoForeachPlace/XGB-LaECP'+str(thisTotalCount)+'.csv'
        features0 = ["deviceName"]
        features1=["microserviceName"]
        features2 = ["tempLatency"]
        features3 = ["finallyLatency"]
        sourceautoPD0 = pd.DataFrame(columns=features0, data=deviceNames)
        sourceautoPD1 = pd.DataFrame(columns=features1, data=microserviceName)
        sourceautoPD2 = pd.DataFrame(columns=features2, data=tempLatency)
        sourceautoPD3 = pd.DataFrame(columns=features3, data=fianlLatency)
        sourceautoPD = pd.concat([sourceautoPD0,sourceautoPD1, sourceautoPD2, sourceautoPD3], axis=1)
        sourceautoPD.to_csv(sourcelossofilename)
        schemeDevice = faultDevice + waferDevice
        flag = 0
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
        # print(flag)
        if (flag == 0):
            faultTrueLatency.append(0)
            waferTrueLatency.append(0)
            totalTrueLatency.append(0)
        schestr = '-'
        schemeDevice = [str(x) for x in schemeDevice]
        sche = schestr.join(schemeDevice)
        placementScheme.append(sche)
        list1= sorted(diffL.items(),key=lambda x:x[1],reverse=True)
        adjustName=[]
        i=0
        for item in list1:
            adjustName.append(item[0])
            i=i+1
            if(i==s):
                break;
        for micro in thisServices:
            if(micro.getServiceName() in adjustName):
                #print(micro.getServiceName())
                subDevice = micro.getDevice()
                subDevicePubTopic = subDevice.getPubTopic()-micro.getPubTopic()
                subDevicePubVolum = subDevice.getPubVolum()-micro.getPubVolum()
                subDeviceSubTopic = subDevice.getSubTopic()-micro.getSubTopic()
                subDeviceSubVolum = subDevice.getSubVolum()-micro.getSubVolum()
                subDeviceVolums = subDevice.getVolums()-micro.getPubVolum()-micro.getSubVolum()
                subDevice.setPubTopic(subDevicePubTopic)
                subDevice.setPubVolum(subDevicePubVolum)
                subDevice.setSubTopic(subDeviceSubTopic)
                subDevice.setSubVolum(subDeviceSubVolum)
                subDevice.setVolums(subDeviceVolums)
                subDevice.setCPURemain(subDevice.getCPURemain() + micro.getCPUDemand())

        for micro in thisServices:
            if (micro.getServiceName() in adjustName):
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
                for innode in innodes:
                    upLatancy = innode.getAcutalLat()
                    #print("microName", micro.getServiceName(), innode.getServiceName(), upLatancy)
                    upLatancys.append(upLatancy)
                    microRate = innode.getRate()
                    upComponent = innode.getComponent()
                    upSubVolum = innode.getSubVolum()
                    upSubtopic = innode.getSubTopic()
                    upPubVolum = innode.getPubVolum()
                    upPubTopic = innode.getPubTopic()
                    upComponents.append(upComponent)
                    upSubVolums.append(upSubVolum)
                    upSubtopics.append(upSubtopic)
                    upPubVolums.append(upPubVolum)
                    upPubTopics.append(upPubTopic)
                    microRates.append(microRate)
                    theDevice = innode.getDevice()
                    if (theDevice.getDeviceName() == "cloud"):
                        innodeIsCloud = 1
                if (micro.getServiceName() == "fault-xgboost"):
                    subDevice = devices[2]
                    # cpu,pubtopics,pubvolum,subtopics,subvolum,volums
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
                        pubDevicepubtopics.append(theDevice.getPubTopic())
                        pubDevicepubvolum.append(theDevice.getPubVolum())
                        pubDevicesubtopics.append(theDevice.getSubTopic())
                        pubDevicesubvolum.append(theDevice.getSubVolum())
                        pubDevicevolums.append(theDevice.getVolums())
                        pubDevicefre.append(theDevice.getFrequency())
                        pubDevicecpuPercent.append(
                            (theDevice.getCPUTotal() - theDevice.getCPURemain()) / theDevice.getCPUTotal())
                    subDevicePubTopic = subDevice.getPubTopic()
                    subDevicePubVolum = subDevice.getPubVolum()
                    subDeviceSubTopic = subDevice.getSubTopic()
                    subDeviceSubVolum = subDevice.getSubVolum()
                    subDeviceVolums = subDevice.getVolums()
                    subDeviceFrequency = subDevice.getFrequency()
                    subDeviceCpuPercent = (subDevice.getCPUTotal() - subDevice.getCPURemain()) / subDevice.getCPUTotal()

                    tempTotal = oneLatency(
                        [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                         microRate,
                         pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                         pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                         pubDevicecpuPercent[0],
                         subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                         subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent, upLatancys[0], microTotalCount,
                         upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                         microRates[0]]
                    );
                    micro.setDevice(devices[2])
                    micro.setAcutalLat(tempTotal)
                    continue;
                if (micro.getServiceName() == "wafer-svm"):
                    subDevice = devices[0]
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
                        pubDevicepubtopics.append(theDevice.getPubTopic())
                        pubDevicepubvolum.append(theDevice.getPubVolum())
                        pubDevicesubtopics.append(theDevice.getSubTopic())
                        pubDevicesubvolum.append(theDevice.getSubVolum())
                        pubDevicevolums.append(theDevice.getVolums())
                        pubDevicefre.append(theDevice.getFrequency())
                        pubDevicecpuPercent.append(
                            (theDevice.getCPUTotal() - theDevice.getCPURemain()) / theDevice.getCPUTotal())
                    subDevicePubTopic = subDevice.getPubTopic()
                    subDevicePubVolum = subDevice.getPubVolum()
                    subDeviceSubTopic = subDevice.getSubTopic()
                    subDeviceSubVolum = subDevice.getSubVolum()
                    subDeviceVolums = subDevice.getVolums()
                    subDeviceFrequency = subDevice.getFrequency()
                    subDeviceCpuPercent = (subDevice.getCPUTotal() - subDevice.getCPURemain()) / subDevice.getCPUTotal()
                    tempTotal = oneLatency(
                        [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                         microRate,
                         pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                         pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                         pubDevicecpuPercent[0],
                         subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                         subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent, upLatancys[0], microTotalCount,
                         upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                         microRates[0]]
                    );
                    micro.setDevice(devices[0])
                    micro.setAcutalLat(tempTotal)
                    continue;
                if (innodeIsCloud == 0):

                    i = 0
                    totalL = float("inf")
                    for device in devices[0:3]:
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
                                       or micro.getServiceName() == "wafer-statis" or micro.getServiceName() == "wafer-ensemble"):
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
                        subDeviceMemPercent = (subDevice.getMemTotal() - (
                                    subDevice.getMemRemain() - micro.getMemDemand())) / subDevice.getMemTotal()

                        if (micro.getCPUDemand() <= device.getCPURemain()):
                            if (innodeSize == 1):
                                tempTotal = oneLatency(
                                    [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum,
                                     microPubTopic,
                                     microRate,
                                     pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                                     pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                                     pubDevicecpuPercent[0],
                                     subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                                     subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent, upLatancys[0], microTotalCount,
                                     upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                                     microRates[0]]);
                            elif (innodeSize == 2):
                                tempTotal = twoLatency(
                                    [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum,
                                     microPubTopic, microRate,
                                     pubDevicepubtopics[0], pubDevicepubtopics[1],
                                     pubDevicepubvolum[0], pubDevicepubvolum[1],
                                     pubDevicesubtopics[0], pubDevicesubtopics[1],
                                     pubDevicesubvolum[0], pubDevicesubvolum[1],
                                     pubDevicevolums[0], pubDevicevolums[1],
                                     pubDevicefre[0], pubDevicefre[1],
                                     pubDevicecpuPercent[0], pubDevicecpuPercent[1],

                                     subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                                     subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent
                                        , upLatancys[0], upLatancys[1], microTotalCount, upComponents[0], upSubVolums[0],
                                     upSubtopics[0], upPubVolums[0], upPubTopics[0], microRates[0]
                                        , microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1], upPubVolums[1],
                                     upPubTopics[1],
                                     microRates[1],
                                     ]);
                            elif (innodeSize == 3):
                                tempTotal = threeLatency(
                                    [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum,
                                     microPubTopic, microRate,
                                     pubDevicepubtopics[0], pubDevicepubtopics[1], pubDevicepubtopics[2],
                                     pubDevicepubvolum[0], pubDevicepubvolum[1], pubDevicepubvolum[2],
                                     pubDevicesubtopics[0], pubDevicesubtopics[1], pubDevicesubtopics[2],
                                     pubDevicesubvolum[0], pubDevicesubvolum[1], pubDevicesubvolum[2],
                                     pubDevicevolums[0], pubDevicevolums[1], pubDevicevolums[2],
                                     pubDevicefre[0], pubDevicefre[1], pubDevicefre[2],
                                     pubDevicecpuPercent[0], pubDevicecpuPercent[1], pubDevicecpuPercent[2],

                                     subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                                     subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent
                                        , upLatancys[0], upLatancys[1], upLatancys[2],
                                     microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0],
                                     upPubTopics[0], microRates[0],
                                     microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1], upPubVolums[1],
                                     upPubTopics[1], microRates[1],
                                     microTotalCount, upComponents[2], upSubVolums[2], upSubtopics[2], upPubVolums[2],
                                     upPubTopics[2], microRates[2],

                                     ]);
                            if (tempTotal < totalL):
                                deviceID = i
                                flag = 1
                                totalL = tempTotal
                                micro.setDevice(device)
                                micro.setAcutalLat(totalL)
                        i = i + 1
                if (flag == 0 or innodeIsCloud == 1):
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
                        if (theDevice.getDeviceName() == "cloud"):
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
                    subDevice = devices[3]
                    subDevicePubTopic = subDevice.getPubTopic() + microPubTopic
                    subDevicePubVolum = subDevice.getPubVolum() + microPubVolum
                    subDeviceSubTopic = subDevice.getSubTopic() + microSubtopic
                    subDeviceSubVolum = subDevice.getSubVolum() + microSubVolum
                    subDeviceVolums = subDevice.getVolums() + microSubVolum + microPubVolum
                    subDeviceFrequency = subDevice.getFrequency()
                    subDeviceCpuPercent = (subDevice.getCPUTotal() - (
                            subDevice.getCPURemain() - micro.getCPUDemand())) / subDevice.getCPUTotal()
                    deviceID = 3
                    tempTotal = 0
                    temponehop = 0
                    if (innodeSize == 1):
                        tempTotal = oneLatency(
                            [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                             microRate,
                             pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                             pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                             pubDevicecpuPercent[0],
                             subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                             subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent
                                , upLatancys[0], microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0],
                             upPubVolums[0], upPubTopics[0],
                             microRates[0]]
                            );
                    elif (innodeSize == 2):
                        tempTotal = twoLatency(
                            [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                             microRate,
                             pubDevicepubtopics[0], pubDevicepubtopics[1],
                             pubDevicepubvolum[0], pubDevicepubvolum[1],
                             pubDevicesubtopics[0], pubDevicesubtopics[1],
                             pubDevicesubvolum[0], pubDevicesubvolum[1],
                             pubDevicevolums[0], pubDevicevolums[1],
                             pubDevicefre[0], pubDevicefre[1],
                             pubDevicecpuPercent[0], pubDevicecpuPercent[1],

                             subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                             subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent, upLatancys[0], upLatancys[1],
                             microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                             microRates[0],
                             microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1], upPubVolums[1], upPubTopics[1],
                             microRates[1],

                             ]
                            );
                    elif (innodeSize == 3):
                        tempTotal = threeLatency([microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum,
                                                  microPubTopic, microRate,
                                                  pubDevicepubtopics[0], pubDevicepubtopics[1], pubDevicepubtopics[2],
                                                  pubDevicepubvolum[0], pubDevicepubvolum[1], pubDevicepubvolum[2],
                                                  pubDevicesubtopics[0], pubDevicesubtopics[1], pubDevicesubtopics[2],
                                                  pubDevicesubvolum[0], pubDevicesubvolum[1], pubDevicesubvolum[2],
                                                  pubDevicevolums[0], pubDevicevolums[1], pubDevicevolums[2],
                                                  pubDevicefre[0], pubDevicefre[1], pubDevicefre[2],
                                                  pubDevicecpuPercent[0], pubDevicecpuPercent[1], pubDevicecpuPercent[2],

                                                  subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic,
                                                  subDeviceSubVolum, subDeviceVolums, subDeviceFrequency,
                                                  subDeviceCpuPercent, upLatancys[0], upLatancys[1], upLatancys[2],
                                                  microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0],
                                                  upPubVolums[0],
                                                  upPubTopics[0],
                                                  microRates[0],
                                                  microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1],
                                                  upPubVolums[1],
                                                  upPubTopics[1],
                                                  microRates[1],
                                                  microTotalCount, upComponents[2], upSubVolums[2], upSubtopics[2],
                                                  upPubVolums[2],
                                                  upPubTopics[0],
                                                  microRates[2],

                                                  ]);
                    micro.setDevice(devices[3])
                    micro.setAcutalLat(tempTotal)

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
            if (1-(micro.getServiceName() in adjustName)):
                microComponent = micro.getComponent()
                microSubVolum = micro.getSubVolum()
                microSubtopic = micro.getSubTopic()
                microPubVolum = micro.getPubVolum()
                microPubTopic = micro.getPubTopic()
                microRate = micro.getRate()
                microTotalCount = micro.getTotalCount()
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
                pubDevicefre = []
                pubDevicecpuPercent = []
                pubDevicememPercent = []
                pubDevicepubtopics = []
                pubDevicepubvolum = []
                pubDevicesubtopics = []
                pubDevicesubvolum = []
                pubDevicevolums = []
                for innode in innodes:
                    upLatancy = innode.getAcutalLat()
                    upLatancys.append(upLatancy)
                    microRate = innode.getRate()
                    upComponent = innode.getComponent()
                    upSubVolum = innode.getSubVolum()
                    upSubtopic = innode.getSubTopic()
                    upPubVolum = innode.getPubVolum()
                    upPubTopic = innode.getPubTopic()
                    upComponents.append(upComponent)
                    upSubVolums.append(upSubVolum)
                    upSubtopics.append(upSubtopic)
                    upPubVolums.append(upPubVolum)
                    upPubTopics.append(upPubTopic)
                    microRates.append(microRate)
                    theDevice = innode.getDevice()
                    pubDevicepubtopics.append(theDevice.getPubTopic())
                    pubDevicepubvolum.append(theDevice.getPubVolum())
                    pubDevicesubtopics.append(theDevice.getSubTopic())
                    pubDevicesubvolum.append(theDevice.getSubVolum())
                    pubDevicevolums.append(theDevice.getVolums())
                    pubDevicefre.append(theDevice.getFrequency())
                    pubDevicecpuPercent.append((theDevice.getCPUTotal() - theDevice.getCPURemain()) / theDevice.getCPUTotal())
                subDevice = micro.getDevice()
                subDevicePubTopic = subDevice.getPubTopic()
                subDevicePubVolum = subDevice.getPubVolum()
                subDeviceSubTopic = subDevice.getSubTopic()
                subDeviceSubVolum = subDevice.getSubVolum()
                subDeviceVolums = subDevice.getVolums()
                subDeviceFrequency = subDevice.getFrequency()
                subDeviceCpuPercent = (subDevice.getCPUTotal() -
                                       subDevice.getCPURemain()) / subDevice.getCPUTotal()
                if (innodeSize == 1):
                    tempTotal = oneLatency(
                        [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic,
                         microRate,
                         pubDevicepubtopics[0], pubDevicepubvolum[0], pubDevicesubtopics[0],
                         pubDevicesubvolum[0], pubDevicevolums[0], pubDevicefre[0],
                         pubDevicecpuPercent[0],
                         subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum,
                         subDeviceVolums, subDeviceFrequency, subDeviceCpuPercent, upLatancys[0], microTotalCount,
                         upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                         microRates[0]]);
                elif (innodeSize == 2):
                    tempTotal = twoLatency(
                        [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic, microRate,
                         pubDevicepubtopics[0], pubDevicepubtopics[1],
                         pubDevicepubvolum[0], pubDevicepubvolum[1],
                         pubDevicesubtopics[0], pubDevicesubtopics[1],
                         pubDevicesubvolum[0], pubDevicesubvolum[1],
                         pubDevicevolums[0], pubDevicevolums[1],
                         pubDevicefre[0], pubDevicefre[1],
                         pubDevicecpuPercent[0], pubDevicecpuPercent[1],

                         subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum, subDeviceVolums,
                         subDeviceFrequency, subDeviceCpuPercent
                            , upLatancys[0], upLatancys[1], microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0],
                         upPubVolums[0], upPubTopics[0], microRates[0]
                            , microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1], upPubVolums[1], upPubTopics[1],
                         microRates[1],
                         ]);
                elif (innodeSize == 3):
                    tempTotal = threeLatency(
                        [microTotalCount, microComponent, microSubVolum, microSubtopic, microPubVolum, microPubTopic, microRate,
                         pubDevicepubtopics[0], pubDevicepubtopics[1], pubDevicepubtopics[2],
                         pubDevicepubvolum[0], pubDevicepubvolum[1], pubDevicepubvolum[2],
                         pubDevicesubtopics[0], pubDevicesubtopics[1], pubDevicesubtopics[2],
                         pubDevicesubvolum[0], pubDevicesubvolum[1], pubDevicesubvolum[2],
                         pubDevicevolums[0], pubDevicevolums[1], pubDevicevolums[2],
                         pubDevicefre[0], pubDevicefre[1], pubDevicefre[2],
                         pubDevicecpuPercent[0], pubDevicecpuPercent[1], pubDevicecpuPercent[2],

                         subDevicePubTopic, subDevicePubVolum, subDeviceSubTopic, subDeviceSubVolum, subDeviceVolums,
                         subDeviceFrequency, subDeviceCpuPercent
                            , upLatancys[0], upLatancys[1], upLatancys[2],
                         microTotalCount, upComponents[0], upSubVolums[0], upSubtopics[0], upPubVolums[0], upPubTopics[0],
                         microRates[0],
                         microTotalCount, upComponents[1], upSubVolums[1], upSubtopics[1], upPubVolums[1], upPubTopics[1],
                         microRates[1],
                         microTotalCount, upComponents[2], upSubVolums[2], upSubtopics[2], upPubVolums[2], upPubTopics[2],
                         microRates[2],

                         ]);
                micro.setAcutalLat(tempTotal)
        iter=iter+1
    sourcelossofilename = 'result/allplacement/' + str(thisTotalCount) + '-' + thisType + '-XGB-LaECP' + str(s) +"-allPlacement.csv"
    features1=["placement"]
    features2=["waferLatency"]
    features3=["faultLatency"]
    features4=["waferTrueLatency"]
    features5=["faultTrueLatency"]
    features6=["totalTrueLatency"]
    sourceautoPD1 = pd.DataFrame(columns=features1, data=placementScheme)
    sourceautoPD2 = pd.DataFrame(columns=features2, data=waferensembleLatency)
    sourceautoPD3 = pd.DataFrame(columns=features3, data=faultensembleLatency)
    sourceautoPD4 = pd.DataFrame(columns=features4, data=waferTrueLatency)
    sourceautoPD5 = pd.DataFrame(columns=features5, data=faultTrueLatency)
    sourceautoPD6 = pd.DataFrame(columns=features6, data=totalTrueLatency)
    sourceautoPD = pd.concat([sourceautoPD1, sourceautoPD2, sourceautoPD3,sourceautoPD4,sourceautoPD5,sourceautoPD6], axis=1)
    sourceautoPD.to_csv(sourcelossofilename)