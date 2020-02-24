import os
from time import sleep

import numpy as np
import pandas as pd
from PIL import Image


def find_dim0(x):
    dim0=np.size(x,axis=0)

    return dim0


def find_dim1(x):
    dim1=np.size(x,axis=1)
    return dim1

# Remove unlabeled data
# wafermap = pd.read_pickle("./LSWMD.pkl")
# print(wafermap.info())
# wafermap['failureNum'] = wafermap.failureType
# wafermap['trainTestNum'] = wafermap.trianTestLabel
# mapping_type = {'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
# mapping_traintest = {'Training':0,'Test':1}
# wafermap = wafermap.replace({'failureNum':mapping_type, 'trainTestNum':mapping_traintest})
# df_withlabel = wafermap[(wafermap['failureNum']>=0) & (wafermap['failureNum']<=8)]
# df_withlabel = df_withlabel.reset_index()
# df_withlabel = df_withlabel.drop(columns=['dieSize', 'lotName', 'waferIndex'])
# df_withlabel.to_pickle("wafermap_withlabel.pkl")

# Remove images that are too small
# wafermap_withlabel = pd.read_pickle("./wafermap_withlabel.pkl")
# wafermap_withlabel = wafermap_withlabel.drop(columns=['index'])
# print(wafermap_withlabel.info())
# wafermap_withlabel['waferMapDim0']=wafermap_withlabel.waferMap.apply(find_dim0)
# wafermap_withlabel['waferMapDim1']=wafermap_withlabel.waferMap.apply(find_dim1)
# sub_df = wafermap_withlabel.loc[wafermap_withlabel['waferMapDim0'] >= 26]
# sub_df = wafermap_withlabel.loc[wafermap_withlabel['waferMapDim1'] >= 26]
# sub_df = sub_df.reset_index()
# print(sub_df.info())
# sub_df.to_pickle("wafermap_withlabel_big.pkl")

# Convert data into pictures
df = pd.read_pickle("./wafermap_withlabel_big.pkl")
# df = df.drop(columns=['index'])
print(df.info())
df_withlabel =df.reset_index()
# df_withlabel = df[(df['failureNum']>=0) & (df['failureNum']<=8)]
# df_withlabel =df_withlabel.reset_index()
# df_withpattern = df[(df['failureNum']>=0) & (df['failureNum']<=7)]
# df_withpattern = df_withpattern.reset_index()
# df_nonpattern = df[(df['failureNum']==8)]
# print(df_withlabel.shape[0], df_withpattern.shape[0], df_nonpattern.shape[0])
class_text_num = {'Center': 0, 'Donut': 0, 'Edge-Loc': 0, 'Edge-Ring': 0, 'Loc': 0, 'Random': 0, 'Scratch': 0,
             'Near-full': 0, 'none': 0}
class_train_num = {'Center': 0, 'Donut': 0, 'Edge-Loc': 0, 'Edge-Ring': 0, 'Loc': 0, 'Random': 0, 'Scratch': 0,
             'Near-full': 0, 'none': 0}

for index, row in df_withlabel.iterrows():
    usage = str(row['trianTestLabel'][0][0])
    img_dir = str(row['failureType'][0][0])
    if not os.path.isdir(usage+'/'+img_dir):
        os.makedirs(usage+'/'+img_dir)
    # if usage == 'Test':
    #     img = Image.fromarray(row['waferMap'] * 127).resize((28, 28)).convert('L')
    #     img.save('./'+usage+'/'+img_dir+'/'+str(class_text_num[img_dir]) + '.png')
    #     class_text_num[img_dir] += 1
    # elif usage == 'Training':
    #     img = Image.fromarray(row['waferMap'] * 127).resize((28, 28)).convert('L')
    #     img.save('./'+usage+'/'+img_dir+'/'+str(class_train_num[img_dir]) + '.png')
    #     class_train_num[img_dir] += 1

    if usage == 'Test':
        color = np.array([(row['waferMap'] == 2) * 240 + (row['waferMap'] == 1) * 94, (row['waferMap'] == 2) * 168 +
                          (row['waferMap'] == 1) * 204, (row['waferMap'] == 2) * 60 + (row['waferMap'] == 1) * 204])
        color = np.swapaxes(color, 2, 0)
        img = Image.fromarray(color.astype(np.uint8), 'RGB').resize((28, 28))
        img.save('./'+usage+'/'+img_dir+'/'+str(class_text_num[img_dir]) + '.png')
        class_text_num[img_dir] += 1
    elif usage == 'Training':
        color = np.array([(row['waferMap'] == 2)*240 + (row['waferMap'] == 1)*94, (row['waferMap'] == 2)*168 +
                          (row['waferMap'] == 1)*204, (row['waferMap'] == 2)*60 + (row['waferMap'] == 1)*204])
        color = np.swapaxes(color, 2, 0)
        img = Image.fromarray(color.astype(np.uint8), 'RGB').resize((28, 28))
        img.save('./'+usage+'/'+img_dir+'/'+str(class_train_num[img_dir]) + '.png')
        class_train_num[img_dir] += 1

