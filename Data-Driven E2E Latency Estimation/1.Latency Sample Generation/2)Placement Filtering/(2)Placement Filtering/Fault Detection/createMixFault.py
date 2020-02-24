import os
import pandas as pd
#xgboost在miniserver上
ip=['192.168.0.53','192.168.0.86','192.168.0.190','39.100.79.76']
#Xgboost is on  minserver  Miniseriver is device 2
#Losso is not on the nano
#ensemble is not on the nano
number=[10,20,30,40]
#python3 source.py ${number} fault-losso ${sourceSubIp}

#nano,lattop,miniserver,aliyun
#1.43,2.2,3.6,2.5
container=['losso','knn','svm','ensemble']
#wafer

#soureVolumes=['/home/wym/code/waferedgeaidemomqtt/wafersource:/exp','/home/zjq/wym/code/waferedgeaidemomqtt/wafersource:/exp','/home/dns/wym/code/waferedgeaidemomqtt/wafersource:/exp','/root/wym/code/waferedgeaidemomqtt/wafersource:/exp']
volumes=[['/home/nano/code/fault/losso:/exp','/home/ljr/code/fault/losso:/exp','/home/zjq/wym/code/fault/losso:/exp','/root/wym/code/fault/losso:/exp'],
['/home/nano/code/fault/knn:/exp','/home/ljr/code/fault/knn:/exp','/home/zjq/wym/code/fault/knn:/exp','/root/wym/code/fault/knn:/exp'],
['/home/nano/code/fault/svm:/exp','/home/ljr/code/fault/svm:/exp','/home/zjq/wym/code/fault/svm:/exp','/root/wym/code/fault/svm:/exp'],
['/home/nano/code/fault/ensemble:/exp','/home/ljr/code/fault/ensemble:/exp','/home/zjq/wym/code/fault/ensemble:/exp','/root/wym/code/fault/ensemble:/exp'],
#['/home/wym/code/fault/storage:/exp','/mnt/d/fault/storage:/exp','/home/zjq/wym/code/fault/storage:/exp','/root/wym/code/fault/storage:/exp'],
]
address=[]
for i in range(0,3):#0,1,2,3
    for j in range(0,3):
        for z in range(0,3):
            for s in range(0,3):
                a=[i,j,z,s]
                address.append(a)        

results=[]
envfileContents=[]


demand = {
    0: 2,
    1: 11,
    2: 5,
    3: 23
}
waferaddress=pd.read_csv("wafer-edge-address.csv").values
for waferId in range(len(waferaddress)):
    realAddress = []


    for k in range(len(address)):
        # 3, 3, 3, 2
        d = {
            0: 2,
            1: 11,
            2: 5,
            3: 23
        }
        waferip1 = waferaddress[waferId][1]
        waferip2 = waferaddress[waferId][2]
        waferip3 = waferaddress[waferId][3]
        waferip4 = waferaddress[waferId][4]
        print(d[waferip1], d[waferip2], d[waferip3], d[waferip4])
        d[waferip1] = int(d[waferip1]) - 3
        d[waferip2] = int(d[waferip2]) - 3
        d[waferip3] = int(d[waferip3]) - 3
        d[waferip4] = int(d[waferip4]) - 2
        print(d[0], d[1], d[2], d[3])

        flag = 1

        content=[]
        #losso的ip
        aourePubIp=ip[address[k][0]]

        content.append(aourePubIp)
        #content.append(sourePubIp)
        for z in range(len(container)):

            volume = "export "+container[z] + "Volumes=" + volumes[z][address[k][z]]
            subip = "export "+container[z] + "SubIp=" + ip[address[k][z]]
            if container[z]=="svm" or container[z]=="knn" or container[z]=="ensemble" or container[z]=="losso":
                #print("hhhh")
                d[address[k][z]]=d[address[k][z]]-2
                #cpu = "export "+container[z] + "Cpu=" + str(d[address[k][z]])+","+str(d[address[k][z]]-1)+","+str(d[address[k][z]]-2)

                if (int(d[address[k][z]]) >=-1):
                    cpu = "export " + container[z] + "Cpu=" + str(d[address[k][z]]+1) + "," + str(d[address[k][z]] +2)
                else:
                    flag = 0
            else:

               d[address[k][z]] = d[address[k][z]] - 1
            # cpu = "export "+container[z] + "Cpu=" + str(d[address[k][z]])
               if (int(d[address[k][z]]) >=-1):
                 cpu = "export " + container[z] + "Cpu=" + str(d[address[k][z]]+1)
               else:
                flag = 0;
            if z!=len(container)-1:#2
                if(container[z]=="losso"):
                    pubip = "export lossoPubIp1=" + ip[address[k][1]]+"\n"+"export lossoPubIp2=" + ip[address[k][2]]+"\n"+"export lossoPubIp3=192.168.0.190"

                elif(container[z]=="knn" or container[z]=="svm"):
                    pubip = "export " + container[z] + "PubIp=" + ip[address[k][3]]

                if (flag != 0):
                    content.append(volume)
                    content.append(pubip)
                    content.append(subip)
                    content.append(cpu)
               # content.append(cpu)

            else:
                #if (ip[address[k][z]] == "202.117.219.111"):
                 #   mongoip = "export mongoIp=192.168.0.101"
                #else:
                 #   mongoip = "export mongoIp=" + ip[address[k][z]]
                if (flag != 0):
                    content.append(volume)
                    content.append(subip)
                    content.append(cpu)
                   # content.append(mongoip)
                    results.append(subip)
        if (flag != 0):
            realAddress.append(address[k])
            envfileContents.append(content)

    for i in range(len(realAddress)):
        print(i,realAddress[i])
    attribute=['losso','knn','svm','ensemble']
    addressPD=pd.DataFrame(columns=attribute,data=realAddress)
    addressPD.to_csv("fault-edge-address-mix"+str(waferId)+".csv")

    for decisionk in  range(len(realAddress)):
        os.makedirs( "wafer"+str(waferId)+'/decision' + str(decisionk))
        for num in number:
            # python3 source.py ${number} fault-losso ${sourceSubIp}
            filesource = "wafer"+str(waferId)+'/decision' + str(decisionk) + "/source"+str(num)+".sh"#
            filesourcedown = "wafer"+str(waferId)+'/decision' + str(decisionk) + "/sourcedown" + str(num) + ".sh"
            with open(filesource, 'a+') as f:
                f.write("export number=" + str(num) + '\n')
                f.write("export sourceSubIp=" + envfileContents[decisionk][0] + '\n')
                f.write("docker-compose -f ../../end.yml up -d" + '\n')
                f.write("docker-compose -f ../../source.yml up -d" + '\n')

            with open(filesourcedown, 'a+') as f:
                f.write("docker-compose -f ../../end.yml down" + '\n')
                f.write("docker-compose -f ../../source.yml down" + '\n')

        decision=realAddress[decisionk]
        ensembleIP = '0'
        for conk in range(len(decision)):
            device=decision[conk]
            if (conk == 3):
                ensembleIP = ip[device]
            filename="wafer"+str(waferId)+'/decision' + str(decisionk)+"/device"+str(decisionk)+str(device)+".sh"
            downname="wafer"+str(waferId)+'/decision' + str(decisionk)+"/down"+str(decisionk)+str(device)+".sh"

            if(os.path.exists(filename)):
                with open(filename, 'a+') as f:
                    f.write("docker-compose -f ../../"+container[conk] +".yml up -d"+ '\n')
                with open(downname, 'a+') as f:
                    f.write("docker-compose -f ../../" + container[conk] + ".yml down" + '\n')
                with open(filename, 'a+') as f:
                    f.write("export decision=decision" + str(decisionk) + '\n')
            else:
                with open(filename, 'a+') as f:
                    f.write("export decision=decision" + str(decisionk) + '\n')
                with open(filename, 'a+') as f:
                    for strs in envfileContents[decisionk]:
                        f.write(strs+ '\n')
                    f.write("docker-compose -f ../../" + container[conk] + ".yml up -d" + '\n')

                with open(downname, 'a+') as f:
                    f.write("docker-compose -f ../../" + container[conk] + ".yml down" + '\n')



        filename = "wafer"+str(waferId)+'/decision' + str(decisionk) + "/device" + str(decisionk) + str(2) + ".sh"
        downname = "wafer"+str(waferId)+'/decision' + str(decisionk) + "/down" + str(decisionk) + str(2) + ".sh"

    #guding
        with open(filename, 'a+') as f:
            f.write("export xgboostVolumes=/home/zjq/wym/code/fault/xgboost:/exp" + '\n')
            f.write("export xgboostSubIp=192.168.0.190" + '\n')
            f.write("export xgboostPubIp=" + str(ensembleIP) + '\n')
            f.write("export xgboostCpu=7,6" + '\n')

            f.write("docker-compose -f ../../xgboost.yml up -d" + '\n')

        with open(downname, 'a+') as f:
            f.write("docker-compose -f ../../xgboost.yml down" + '\n')










