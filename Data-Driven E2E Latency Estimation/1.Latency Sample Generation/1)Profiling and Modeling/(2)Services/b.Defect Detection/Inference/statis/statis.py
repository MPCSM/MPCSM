# coding=utf8
import paho.mqtt.client as mqtt
import datetime
import sys
from opPub import pub
import logging
import pickle
import time
from scipy import interpolate
import numpy as np
import pandas as pd
from skimage import measure
from scipy import stats
from skimage.transform import radon

logging.basicConfig(level=logging.DEBUG)
#-------------sys parameter----------

#Downstream of the topic
pubTopic=sys.argv[1]
#Downstream of the ip
pubIp=sys.argv[2]

subTopic=sys.argv[3]
subIp=sys.argv[4]



#compact features
def on_message(client, userdata, msg):
    # -------Receive a message----------------
    subTim =time.time()
    
    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    #print(payload_decoded)
    txtArray =payload_decoded[0]
    frame=payload_decoded[1]
    pubTime=payload_decoded[2]

    def cal_dist(img, x, y):
        dim0 = np.size(img, axis=0)
        dim1 = np.size(img, axis=1)
        dist = np.sqrt((x - dim0 / 2) ** 2 + (y - dim1 / 2) ** 2)
        return dist


    def fea_geom(img):
        norm_area = img.shape[0] * img.shape[1]
        norm_perimeter = np.sqrt((img.shape[0]) ** 2 + (img.shape[1]) ** 2)

        img_labels = measure.label(img, neighbors=4, connectivity=1, background=0)

        if img_labels.max() == 0:
            img_labels[img_labels == 0] = 1
            no_region = 0
        else:
            info_region = stats.mode(img_labels[img_labels > 0], axis=None)
            no_region = info_region[0][0] - 1

        prop = measure.regionprops(img_labels)
        prop_area = prop[no_region].area / norm_area
        prop_perimeter = prop[no_region].perimeter / norm_perimeter

        prop_cent = prop[no_region].local_centroid
        prop_cent = cal_dist(img, prop_cent[0], prop_cent[1])

        prop_majaxis = prop[no_region].major_axis_length / norm_perimeter
        prop_minaxis = prop[no_region].minor_axis_length / norm_perimeter
        prop_ecc = prop[no_region].eccentricity
        prop_solidity = prop[no_region].solidity

        return prop_area, prop_perimeter, prop_majaxis, prop_minaxis, prop_ecc, prop_solidity


    def cal_den(x):
        return 100 * (np.sum(x == 2) / np.size(x))


    #df_withpattern['fea_reg'] = df_withpattern.waferMap.apply(find_regions)

    def change_val(img):
        img[img == 1] = 0
        return img


    df_withpattern_copy = txtArray.copy()
    #print(df_withpattern_copy.info())
    df_withpattern_copy['new_waferMap'] = df_withpattern_copy.waferMap.apply(change_val)
    #print(df_withpattern_copy[:1])
    def cubic_inter_mean(img):
        theta = np.linspace(0., 180., max(img.shape), endpoint=False)
        sinogram = radon(img, theta=theta)
        xMean_Row = np.mean(sinogram, axis=1)
        x = np.linspace(1, xMean_Row.size, xMean_Row.size)
        y = xMean_Row
        f = interpolate.interp1d(x, y, kind='cubic')
        xnew = np.linspace(1, xMean_Row.size, 20)
        ynew = f(xnew) / 100  # use interpolation function returned by `interp1d`
        return ynew


    def cubic_inter_std(img):
        theta = np.linspace(0., 180., max(img.shape), endpoint=False)
        sinogram = radon(img, theta=theta)
        xStd_Row = np.std(sinogram, axis=1)
        x = np.linspace(1, xStd_Row.size, xStd_Row.size)
        y = xStd_Row
        f = interpolate.interp1d(x, y, kind='cubic')
        xnew = np.linspace(1, xStd_Row.size, 20)
        ynew = f(xnew) / 100  # use interpolation function returned by `interp1d`
        return ynew


    df_withpattern_copy['fea_geom'] = df_withpattern_copy.waferMap.apply(fea_geom)
    #print("a",df_withpattern_copy[:1])

    df_withpattern_copy['fea_cub_mean'] = df_withpattern_copy.waferMap.apply(cubic_inter_mean)
    #print("b", df_withpattern_copy[:1])
    df_withpattern_copy['fea_cub_std'] = df_withpattern_copy.waferMap.apply(cubic_inter_std)

    #print("c", df_withpattern_copy[:1])
    df_all = df_withpattern_copy.copy()

    mean= pd.Series.as_matrix(df_all.fea_cub_mean)
    std=pd.Series.as_matrix(df_all.fea_cub_std)
    geom=pd.Series.as_matrix(df_all.fea_geom)

    b = [mean[i] for i in range(df_all.shape[0])]  # 20
    c = [std[i] for i in range(df_all.shape[0])]  # 20
    d = [geom[i] for i in range(df_all.shape[0])]  # 6
    fea_all = np.concatenate((np.array(b), np.array(c), np.array(d)), axis=1)
    #print(type(b),type(c),type(d))

    print("e",len(fea_all))

    payload = [fea_all,frame]

    thetime = time.time()
    pubTime.append(subTim)
    pubTime.append(thetime)
    payload.append(pubTime)
    payload = pickle.dumps(payload)
    pub(pubTopic, pubIp, payload)

client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(subIp, 1883, 60)
client.subscribe(topic=subTopic, qos=2)
client.loop_forever()





	
