import pandas as pd
totalcount=10
#1
df=pd.read_csv(str(totalcount)+'-mix-one-data.csv')
df=df.drop(columns=['microPubTopic','pubDevicefre','upComponent','upPubVolum','upSubVolum','upPubTopic','microSubtopic','microRate','pubDevicesubtopics','upRate'])
df.to_csv(str(totalcount)+'-mix-one-data-1.csv')
#2

df=pd.read_csv(str(totalcount)+'-mix-two-data.csv')
df=df[['upLatency1','upLatency2','totalCount','pubDevicesubcvolum1','pubDevicepubtopics1','pubDevicepubvolum1',
'upCount1','pubDevicecpubvolum2','pubDevicesubtopics1','pubDevicecpuPercent1','subDevicePubTopic','subDevicePubVolum',
'pubDevicesubcvolum2','subDeviceSubVolum','pubDevicevolums1','pubDevicefre1','subDeviceFrequency','pubDevicesubtopics2',
'pubDevicecpuPercent2','subDeviceSubTopic','pubDevicepubtopics2','subDeviceCpuPercent','upCount2','subDeviceVolums']]
df.to_csv(str(totalcount)+'-mix-two-data-1.csv')
#3
df=pd.read_csv(str(totalcount)+'-mix-three-data.csv')
df=df[['upLatency1','upLatency2','totalCount','upLatency3','subDevicePubVolum','pubDevicepubvolum1','pubDevicesubcvolum1',
'subDeviceSubVolum','pubDevicepubvolum2','pubDevicesubcvolum3','pubDevicesubcvolum2','upCount1','pubDevicesubtopics3',
'pubDevicesubtopics1','pubDevicecpuPercent2','pubDevicecpuPercent1','pubDevicepubvolum3','pubDevicesubtopics2',
'pubDevicecpuPercent3','subDeviceSubTopic','pubDevicepubtopics2','pubDevicepubtopics1','subDeviceCpuPercent',
'subDevicePubTopic','upCount2','subDeviceVolums','pubDevicevolums3','pubDevicepubtopics3','pubDevicevolums1','pubDevicevolums2',
'pubDevicefre2','subDeviceFrequency','pubDeviceFrequency','pubDevicefre1']]
df.to_csv(str(totalcount)+'-mix-three-data-1.csv')
