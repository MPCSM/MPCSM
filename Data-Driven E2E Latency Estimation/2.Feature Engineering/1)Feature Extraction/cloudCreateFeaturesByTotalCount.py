import os
import pymongo
import pandas as pd
import numpy as np
#Naming convention!!
#Naming specification for decision: STR (totalcount)+"-db_name-edge.csv", STR (totalcount)+"-db_name-cloud.csv"
#In this file, the fault-edge and fault-cloud CSV are generated
totalCount=80
waferAddress=pd.read_csv("wafer-fault-decision/wafer-edge-address.csv").values

placementMixCloud=pd.read_csv("dbname-bytotalcount/"+str(totalCount)+"-db_name-cloud.csv").values
print(placementMixCloud)
for i in range(0,69):
    #FaultDecision is on the edge side because fault-ensemble is not on the cloud
    faultDecisionsEdge=[]
    faultDecisionaddress = pd.read_csv("wafer-fault-decision/fault-edge-address-mix" + str(i) + ".csv").values
    fault_db_name="wafer"+str(i)+"fault"
    #Add database filter code
    for j in range(len(placementMixCloud)):
        #print(placementMixCloud[j][1],i)
        if (placementMixCloud[j][1]==i):
            faultDecisionsEdge.append(placementMixCloud[j][2])
    if(len(faultDecisionsEdge)==0):
        continue;
    #print("faultDecisionsEdge",faultDecisionsEdge)
    datemill=1
    #The unique representation of the component   'losso','knn','svm','xgboost','ensemble' ，  does not change
    micocomponent=[51,19.1,1,0.5,49]
    #Raspberry  data, don't change
    pi=[1,7464602,0,0,7464602]
    picpurate=0.9
    xgboostA=[1,12752,1,515318, 528070]
    cpuTotal = {
        0: 4,
        1: 12,
        2: 8,
        3: 24
    }
    #No need to change 4 devices
    cpurate = {
        0: 1.43,
        1: 2.2,
        2: 3.6,
        3: 2.5
    }
     #The number of sent topics, the number of sent data, 
    # the number of received topics, the number of received data 0, 1, 2 and 3 respectively represent the four containers of 'losso',' KNN ',' SVM 'and 'ensemble'
    faultDateRate={
        0: [3,1545954,1,7464602],
        1: [1,12752,1,515318],
        2: [1,12752,1,515318],
        3:[0,0,3,38256]
    }
    waferDateRate = {
        0: [1, 7132, 1, 237880],
        1: [1, 36632, 1, 314889],
        2: [1, 263, 1, 7132],
        3: [0, 0, 2, 874]
    }
    waferMicocomponent = [19.2, 141, 34, 7, 52]
    waferPi = [2, 552769, 0, 0, 552769]
    svmA = [1, 611, 1, 36632, 37243]
    data=[]
    waferdata=[]
    twoForkdata=[]
    triForkData=[]
    label=[]
    waferlabel=[]
    triForkLabel=[]
    twoForkLabel=[]
    dataAtt=["totalCount","microComponent","microSubVolum","microSubtopic","microPubVolum","microPubTopic","microRate",
    "pubDevicepubtopics","pubDevicepubvolum","pubDevicesubtopics","pubDevicesubcvolum","pubDevicevolums","pubDevicefre","pubDevicecpuPercent",
    "subDevicePubTopic","subDevicePubVolum","subDeviceSubTopic","subDeviceSubVolum","subDeviceVolums","subDeviceFrequency","subDeviceCpuPercent","upLatency",
    "upCount","upComponent","upSubVolum","upSubtopic","upPubVolum","upPubTopic","upRate"]
    dataAttTri=["totalCount","microComponent","microSubVolum","microSubtopic","microPubVolum","microPubTopic","microRate",
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
    dataAttTwo = ["totalCount", "microComponent", "microSubVolum", "microSubtopic", "microPubVolum", "microPubTopic",
                  "microRate",
                  "pubDevicepubtopics1", "pubDevicepubtopics2",
                  "pubDevicepubvolum1", "pubDevicepubvolum2",
                  "pubDevicesubtopics1", "pubDevicesubtopics2",
                  "pubDevicesubcvolum1", "pubDevicesubcvolum2",
                  "pubDevicevolums1", "pubDevicevolums2",
                  "pubDevicefre1", "pubDevicefre2",
                  "pubDevicecpuPercent1", "pubDevicecpuPercent2",
                  "subDevicePubTopic", "subDevicePubVolum", "subDeviceSubTopic", "subDeviceSubVolum", "subDeviceVolums",
                  "subDeviceFrequency", "subDeviceCpuPercent", "upLatency1", "upLatency2",
                  "upCount1", "upComponent1", "upSubVolum1", "upSubtopic1", "upPubVolum1", "upPubTopic1", "upRate1",
                  "upCount2", "upComponent2", "upSubVolum2", "upSubtopic2", "upPubVolum2", "upPubTopic2", "upRate2"]
    labelAtt=["totalLatency"]
    for faultDecision in faultDecisionsEdge:
        cpuNow={
                0:1,
                1:0,
                2:2,
                3:0,
        }
        topicVolume = {
                0: [1,611,1,36632, 37243],
                1: [0, 0, 0, 0, 0],
                2: [1,12752,1,515318, 528070],
                3: [0, 0, 0, 0, 0]
        }
        #--------------------------Statistics of wafer's sending and receiving themes and other information--------------------------------------
        addressDecision=waferAddress[i][1:]
        waferip0=addressDecision[0]
        cpuNow[waferip0] = cpuNow[waferip0] + 3
        topicVolume[waferip0][0]=topicVolume[waferip0][0]+waferDateRate[0][0]
        topicVolume[waferip0][1] = topicVolume[waferip0][1] + waferDateRate[0][1]
        topicVolume[waferip0][2] = topicVolume[waferip0][2] + waferDateRate[0][2]
        topicVolume[waferip0][3] = topicVolume[waferip0][3] + waferDateRate[0][3]
        topicVolume[waferip0][4] = topicVolume[waferip0][4] + waferDateRate[0][1]+waferDateRate[0][3]

        waferip1=addressDecision[1]
        topicVolume[waferip1][0] = topicVolume[waferip1][0] + waferDateRate[1][0]
        topicVolume[waferip1][1] = topicVolume[waferip1][1] + waferDateRate[1][1]
        topicVolume[waferip1][2] = topicVolume[waferip1][2] + waferDateRate[1][2]
        topicVolume[waferip1][3] = topicVolume[waferip1][3] + waferDateRate[1][3]
        topicVolume[waferip1][4] = topicVolume[waferip1][4] + waferDateRate[1][1] +waferDateRate[1][3]
        cpuNow[waferip1] = cpuNow[waferip1] + 3

        waferip2=addressDecision[2]
        topicVolume[waferip2][0] = topicVolume[waferip2][0] + waferDateRate[2][0]
        topicVolume[waferip2][1] = topicVolume[waferip2][1] + waferDateRate[2][1]
        topicVolume[waferip2][2] = topicVolume[waferip2][2] + waferDateRate[2][2]
        topicVolume[waferip2][3] = topicVolume[waferip2][3] + waferDateRate[2][3]
        topicVolume[waferip2][4] = topicVolume[waferip2][4] + waferDateRate[2][1] +waferDateRate[2][3]
        cpuNow[waferip2] = cpuNow[waferip2] + 3

        waferip3=addressDecision[3]
        topicVolume[waferip3][0] = topicVolume[waferip3][0] + waferDateRate[3][0]
        topicVolume[waferip3][1] = topicVolume[waferip3][1] + waferDateRate[3][1]
        topicVolume[waferip3][2] = topicVolume[waferip3][2] + waferDateRate[3][2]
        topicVolume[waferip3][3] = topicVolume[waferip3][3] + waferDateRate[3][3]
        topicVolume[waferip3][4] = topicVolume[waferip3][4] + waferDateRate[3][1] +waferDateRate[3][3]
        cpuNow[waferip3] = cpuNow[waferip3] + 2

        # --------------------------1.Count fault's send and receive topics and delay information-------------------------------------
        addressDecision=faultDecisionaddress[faultDecision][1:]
        ##print(addressDecision)
        ip0=addressDecision[0]
        cpuNow[ip0] = cpuNow[ip0] + 2
        topicVolume[ip0][0]=topicVolume[ip0][0]+faultDateRate[0][0]
        topicVolume[ip0][1] = topicVolume[ip0][1] + faultDateRate[0][1]
        topicVolume[ip0][2] = topicVolume[ip0][2] + faultDateRate[0][2]
        topicVolume[ip0][3] = topicVolume[ip0][3] + faultDateRate[0][3]
        topicVolume[ip0][4] = topicVolume[ip0][4] + faultDateRate[0][1]+faultDateRate[0][3]

        ip1=addressDecision[1]

        topicVolume[ip1][0] = topicVolume[ip1][0] + faultDateRate[1][0]
        topicVolume[ip1][1] = topicVolume[ip1][1] + faultDateRate[1][1]
        topicVolume[ip1][2] = topicVolume[ip1][2] + faultDateRate[1][2]
        topicVolume[ip1][3] = topicVolume[ip1][3] + faultDateRate[1][3]
        topicVolume[ip1][4] = topicVolume[ip1][4] + faultDateRate[1][1] + faultDateRate[1][3]
        cpuNow[ip1] = cpuNow[ip1] + 2

        ip2=addressDecision[2]

        topicVolume[ip2][0] = topicVolume[ip2][0] + faultDateRate[2][0]
        topicVolume[ip2][1] = topicVolume[ip2][1] + faultDateRate[2][1]
        topicVolume[ip2][2] = topicVolume[ip2][2] + faultDateRate[2][2]
        topicVolume[ip2][3] = topicVolume[ip2][3] + faultDateRate[2][3]
        topicVolume[ip2][4] = topicVolume[ip2][4] + faultDateRate[2][1] + faultDateRate[2][3]
        cpuNow[ip2] = cpuNow[ip2] + 2

        ip3 = addressDecision[3]
        cpuNow[ip3] = cpuNow[ip3] + 2
        topicVolume[ip3][0] = topicVolume[ip3][0] + faultDateRate[3][0]
        topicVolume[ip3][1] = topicVolume[ip3][1] + faultDateRate[3][1]
        topicVolume[ip3][2] = topicVolume[ip3][2] + faultDateRate[3][2]
        topicVolume[ip3][3] = topicVolume[ip3][3] + faultDateRate[3][3]
        topicVolume[ip3][4] = topicVolume[ip3][4] + faultDateRate[3][1] + faultDateRate[3][3]
        # --------------------------2.Count the wafer delay-------------------------------------
        wafer_db_name = "wafer" + str(i) + "fault" + str(faultDecision)
        myclient = pymongo.MongoClient("mongodb://39.100.79.76:27019/")
        waferdb = myclient[wafer_db_name]
        mycol = waferdb["decision" + str(i)]

        mydoc = mycol.find()[1:totalCount+1]
        lat1 = 0
        lat2 = 0
        lat3 = 0
        lat4 = 0
        lat5 = 0
        for x in mydoc:
          
      
            print("111")
            frame = x["cnnframe"]
            # result = x["result"]
            cnnTime = x["cnnTime"]
            svmTime = x["svmTime"]
            ensembleTime = x["ensembleTime"]
            # auto
            lat1 = lat1 + cnnTime[2] - cnnTime[0]
            lat2 = lat2 + svmTime[2] - svmTime[0]
            lat3 = lat3 + cnnTime[4] - cnnTime[0]
            lat4 = lat4 + svmTime[4] - svmTime[0]
            lat5 = lat5 + max(ensembleTime[1] - cnnTime[0], ensembleTime[1] - svmTime[0])

        waferlabel.append(lat1 / totalCount)  # auto
        waferlabel.append(lat2 / totalCount)  # static
        waferlabel.append(lat3 / totalCount)  # cnn
        waferlabel.append(lat4 / totalCount)  # svm
        twoForkLabel.append(lat5 / totalCount) #ensemble

        waferdata.append(
            [totalCount, micocomponent[0], waferDateRate[0][3], waferDateRate[0][2], waferDateRate[0][1],
             waferDateRate[0][0], datemill,
             # "pubDevicepubtopics", "pubDevicepubvolum", "pubDevicesubtopics", "pubDevicesubcvolum", "pubDevicevolums", "pubDevicefre", "pubDevicecpuPercent",
             waferPi[0], waferPi[1], waferPi[2], waferPi[3], waferPi[4], picpurate, 0,
             topicVolume[waferip0][0], topicVolume[waferip0][1], topicVolume[waferip0][2], topicVolume[waferip0][3],
             topicVolume[waferip0][4],
             cpurate[waferip0], round(cpuNow[waferip0] / cpuTotal[waferip0], 2),
             0, totalCount, 0.5, waferPi[3], waferPi[2], waferPi[1], waferPi[0], datemill])
        # statis
        waferdata.append(
            [totalCount, micocomponent[1], waferDateRate[1][3], waferDateRate[1][2], waferDateRate[1][1],
             waferDateRate[1][0], datemill,
             # "pubDevicepubtopics", "pubDevicepubvolum", "pubDevicesubtopics", "pubDevicesubcvolum", "pubDevicevolums", "pubDevicefre", "pubDevicecpuPercent",
             waferPi[0], waferPi[1], waferPi[2], waferPi[3], waferPi[4], picpurate, 0,
             topicVolume[waferip1][0], topicVolume[waferip1][1], topicVolume[waferip1][2], topicVolume[waferip1][3],
             topicVolume[waferip1][4],
             cpurate[waferip1], round(cpuNow[waferip1] / cpuTotal[waferip1], 2),
             0, totalCount, 0.5, waferPi[3], waferPi[2], waferPi[1], waferPi[0], datemill])
        # cnn
        waferdata.append(
            [totalCount, micocomponent[2], waferDateRate[2][3], waferDateRate[2][2], waferDateRate[2][1],
             waferDateRate[2][0], datemill,
             # "pubDevicepubtopics", "pubDevicepubvolum", "pubDevicesubtopics", "pubDevicesubcvolum", "pubDevicevolums", "pubDevicefre", "pubDevicecpuPercent",
             topicVolume[waferip0][0], topicVolume[waferip0][1], topicVolume[waferip0][2], topicVolume[waferip0][3],
             topicVolume[waferip0][4],
             cpurate[waferip0], round(cpuNow[waferip0] / cpuTotal[waferip0], 2),
             topicVolume[waferip2][0], topicVolume[waferip2][1], topicVolume[waferip2][2], topicVolume[waferip2][3],
             topicVolume[waferip2][4], cpurate[waferip2],
             round(cpuNow[waferip2] / cpuTotal[waferip2], 2), lat1 / totalCount,
             totalCount, micocomponent[0], waferDateRate[0][2], waferDateRate[0][2], waferDateRate[0][1],
             waferDateRate[0][0], datemill])
        # svm
        waferdata.append(
            [totalCount, micocomponent[3], svmA[3], svmA[2], svmA[1], svmA[0], datemill,
             # "pubDevicepubtopics", "pubDevicepubvolum", "pubDevicesubtopics", "pubDevicesubcvolum", "pubDevicevolums", "pubDevicefre", "pubDevicecpuPercent",
             topicVolume[waferip1][0], topicVolume[waferip1][1], topicVolume[waferip1][2], topicVolume[waferip1][3],
             topicVolume[waferip1][4],
             cpurate[waferip1], round(cpuNow[waferip1] / cpuTotal[waferip1], 2),
             topicVolume[0][0], topicVolume[0][1], topicVolume[0][2], topicVolume[0][3],
             topicVolume[0][4], cpurate[0],
             round(cpuNow[0] / cpuTotal[0], 2), lat2 / totalCount,
             totalCount, micocomponent[1], waferDateRate[1][3], waferDateRate[1][2], waferDateRate[1][1],
             waferDateRate[1][0], datemill])
        #ensemble
        twoForkdata.append(
            [totalCount, micocomponent[4], waferDateRate[3][3], waferDateRate[3][2], waferDateRate[3][1],
             waferDateRate[3][0], datemill,
             # "pubDevicepubtopics", "pubDevicepubvolum", "pubDevicesubtopics", "pubDevicesubcvolum", "pubDevicevolums", "pubDevicefre", "pubDevicecpuPercent",
             topicVolume[waferip2][0], topicVolume[0][0],
             topicVolume[waferip2][1], topicVolume[0][1],
             topicVolume[waferip2][2], topicVolume[0][2],
             topicVolume[waferip2][3], topicVolume[0][3],
             topicVolume[waferip2][4], topicVolume[0][4],
             cpurate[waferip2], cpurate[0],
             round(cpuNow[waferip2] / cpuTotal[waferip2], 2),
             round(cpuNow[0] / cpuTotal[0], 2),
             topicVolume[waferip3][0], topicVolume[waferip3][1], topicVolume[waferip3][2], topicVolume[waferip3][3],
             topicVolume[waferip3][4], cpurate[waferip3],
             round(cpuNow[waferip3] / cpuTotal[waferip3], 2), lat3 / totalCount, lat4 / totalCount,
             totalCount, micocomponent[2], waferDateRate[2][3], waferDateRate[2][2], waferDateRate[2][1],
             waferDateRate[2][0], datemill,
             totalCount, micocomponent[3], svmA[3], svmA[2], svmA[1], svmA[0], datemill])
    # wafer one
    dataPD = pd.DataFrame(columns=dataAtt, data=waferdata)
    dataPD.to_csv("features-bytotalcount/"+str(totalCount) + "-cloud-wafer-one-data.csv",mode="a+")
    labelPD = pd.DataFrame(columns=labelAtt, data=waferlabel)
    labelPD.to_csv("features-bytotalcount/"+str(totalCount) + "-cloud-wafer-one-label.csv",mode="a+")

    # wafer two
    dataPD = pd.DataFrame(columns=dataAttTwo, data=twoForkdata)
    dataPD.to_csv("features-bytotalcount/"+str(totalCount) + "-cloud-two-data.csv",mode="a+")
    labelPD = pd.DataFrame(columns=labelAtt, data=twoForkLabel)
    labelPD.to_csv("features-bytotalcount/"+str(totalCount) + "-cloud-two-label.csv",mode="a+")

