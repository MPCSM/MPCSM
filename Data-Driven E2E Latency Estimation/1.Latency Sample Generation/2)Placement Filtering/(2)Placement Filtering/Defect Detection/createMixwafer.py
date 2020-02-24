import os
import pandas as pd
ip=['192.168.0.53','192.168.0.86','192.168.0.190','39.100.79.76']
#The SVM is fixed on nano;
#Statis is not placed on nano, and ensemble is not fixed on nano
#nano,lattop,miniserver,aliyun
#1.43,2.2,3.6,2.5

container=['auto','statis','cnn','ensemble']
#wafer
number=[25]
#soureVolumes=['/home/wym/code/waferedgeaidemomqtt/wafersource:/exp','/home/zjq/wym/code/waferedgeaidemomqtt/wafersource:/exp','/home/dns/wym/code/waferedgeaidemomqtt/wafersource:/exp','/root/wym/code/waferedgeaidemomqtt/wafersource:/exp']
volumes=[['/home/nano/code/wafer/auto:/exp','/home/ljr/code/wafer/auto:/exp','/home/zjq/wym/code/wafer/auto:/exp','/root/wym/code/wafer/auto:/exp'],
['/home/nano/code/wafer/statis:/exp','/home/ljr/code/wafer/statis:/exp','/home/zjq/wym/code/wafer/statis:/exp','/root/wym/code/wafer/statis:/exp'],
['/home/nano/code/wafer/cnn:/exp','/home/ljr/code/wafer/cnn:/exp','/home/zjq/wym/code/wafer/cnn:/exp','/root/wym/code/wafer/cnn:/exp'],
['/home/nano/code/wafer/ensemble:/exp','/home/ljr/code/wafer/ensemble:/exp','/home/zjq/wym/code/wafer/ensemble:/exp','/root/wym/code/wafer/ensemble:/exp'],
#['/home/wym/code/wafer/storage:/exp','/mnt/d/wafer/storage:/exp','/home/zjq/wym/code/wafer/storage:/exp','/root/wym/code/wafer/storage:/exp'],
]
address=[]
for i in range(0,4):#0,1,2,3
    for j in range(0,4):
        if(j==3):
            continue;
        for z in range(0,4):
            for s in range(0,4):
                #for e in range(0,4):
                    #for x in range(0,4):
                a=[i,j,z,s]
                address.append(a)       

cloudaddress=address

for i in range(len(address)):
    for j in range(0,4):
        if (address[i][j]==3):
            if j==0:
                cloudaddress[i][j+2]=3
                cloudaddress[i][j + 3] = 3
                break
            if j==1:
                cloudaddress[i][j + 2] = 3
                break
            if j==2:
                cloudaddress[i][j + 1] = 3
                break

def getNonRepeatList3(data):
    return [i for n, i in enumerate(data) if i not in data[:n]]
address=getNonRepeatList3(cloudaddress)
print(address)
results=[]
envfileContents=[]
realAddress=[]

demand = {
    0: 2,
    1: 11,
    2: 5,
    3: 15
}
flag=1
for k in range(len(address)):
    flag = 1
    d = {
        0: 2,
        1: 11,
        2: 5,
        3: 15
    }

    content=[]
    #auto ip
    aourePubIp=ip[address[k][0]]
    #statis ip
    sourePubIp=ip[address[k][1]]
    content.append(aourePubIp)
    content.append(sourePubIp)
    for z in range(len(container)):
        volume = "export "+container[z] + "Volumes=" + volumes[z][address[k][z]]
        subip = "export "+container[z] + "SubIp=" + ip[address[k][z]]
        if container[z]=="auto" or container[z]=="cnn" or container[z]=="statis":
            #print("hhhh")
            d[address[k][z]]=d[address[k][z]]-3
            #cpu = "export "+container[z] + "Cpu=" + str(d[address[k][z]])+","+str(d[address[k][z]]-1)+","+str(d[address[k][z]]-2)

            if (int(d[address[k][z]]) >= -1):
                cpu = "export " + container[z] + "Cpu=" + str(d[address[k][z]]+1) + "," + str(d[address[k][z]] + 2) + "," + str(d[address[k][z]] + 3)
            else:
                flag = 0
        elif container[z]=="ensemble":
            #print("hhhh")
            d[address[k][z]]=d[address[k][z]]-2
            #cpu = "export "+container[z] + "Cpu=" + str(d[address[k][z]])+","+str(d[address[k][z]]-1)+","+str(d[address[k][z]]-2)

            if (int(d[address[k][z]]) >= -1):
                cpu = "export " + container[z] + "Cpu=" + str(d[address[k][z]]+1) + "," + str(d[address[k][z]] + 2)
            else:
                flag = 0
        else:
            #print("meijinlai ")
            d[address[k][z]]=d[address[k][z]]-1
            #cpu = "export "+container[z] + "Cpu=" + str(d[address[k][z]])
            if (int(d[address[k][z]]) >=-1):
                cpu = "export "+container[z] + "Cpu=" + str(d[address[k][z]]+1)
            else:
                flag=0;
        if z!=len(container)-1:#2
            if(container[z]=="auto"):
                pubip = "export " + container[z] + "PubIp=" + ip[address[k][2]]
            elif(container[z]=="statis"):
                pubip = "export " + container[z] + "PubIp=192.168.0.53"
            elif(container[z]=="cnn"):
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
attribute=['auto','statis','cnn','ensemble']
addressPD=pd.DataFrame(columns=attribute,data=realAddress)
addressPD.to_csv("wafer-edge-address.csv")

for decisionk in  range(len(realAddress)):
    os.makedirs('decision' + str(decisionk))

    for num in number:
        # python3 source.py ${number} fault-losso ${sourceSubIp}
        filesource = 'decision' + str(decisionk) + "/source"+str(num)+".sh"#
        filesourcedown = 'decision' + str(decisionk) + "/sourcedown" + str(num) + ".sh"
        with open(filesource, 'a+') as f:
            f.write("export number=" + str(num) + '\n')
            f.write("export sourceSubIp1=" + envfileContents[decisionk][0] + '\n')
            f.write("export sourceSubIp2=" + envfileContents[decisionk][1] + '\n')
            f.write("docker-compose -f ../end.yml up -d" + '\n')
            f.write("docker-compose -f ../source.yml up -d" + '\n')

        with open(filesourcedown, 'a+') as f:
            f.write("docker-compose -f ../end.yml down" + '\n')
            f.write("docker-compose -f ../source.yml down" + '\n')


    decision=realAddress[decisionk]
    ensembleIP = '0'
    for conk in range(len(decision)):
        device=decision[conk]
        if (conk == 3):
            ensembleIP = ip[device]
        filename='decision' + str(decisionk)+"/device"+str(decisionk)+str(device)+".sh"
        downname='decision' + str(decisionk)+"/down"+str(decisionk)+str(device)+".sh"

        if(os.path.exists(filename)):
            with open(filename, 'a+') as f:
                f.write("docker-compose -f ../"+container[conk] +".yml up -d"+ '\n')
            with open(downname, 'a+') as f:
                f.write("docker-compose -f ../" + container[conk] + ".yml down" + '\n')
            with open(filename, 'a+') as f:
                f.write("export decision=decision" + str(decisionk) + '\n')
        else:
            with open(filename, 'a+') as f:
                f.write("export decision=decision" + str(decisionk) + '\n')
            with open(filename, 'a+') as f:
                for strs in envfileContents[decisionk]:
                    f.write(strs+ '\n')
                f.write("docker-compose -f ../" + container[conk] + ".yml up -d" + '\n')

            with open(downname, 'a+') as f:
                f.write("docker-compose -f ../" + container[conk] + ".yml down" + '\n')



    filename = 'decision' + str(decisionk) + "/device" + str(decisionk) + str(0) + ".sh"
    downname = 'decision' + str(decisionk) + "/down" + str(decisionk) + str(0) + ".sh"


    with open(filename, 'a+') as f:
        f.write("export svmVolumes=/home/nano/code/wafer/svm:/exp" + '\n')
        f.write("export svmSubIp=192.168.0.53" + '\n')
        f.write("export svmPubIp=" + str(ensembleIP) + '\n')
        f.write("export svmCpu=3" + '\n')

        f.write("docker-compose -f ../svm.yml up -d" + '\n')

    with open(downname, 'a+') as f:
        f.write("docker-compose -f ../svm.yml down" + '\n')












