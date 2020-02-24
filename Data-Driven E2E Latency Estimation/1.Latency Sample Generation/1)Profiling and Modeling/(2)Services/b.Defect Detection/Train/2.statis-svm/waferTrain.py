from os.path import join
from scipy import interpolate
import numpy as np
import pandas as pd
from skimage import measure
from scipy import stats
from skimage.transform import radon

if __name__ == "__main__":
    df = pd.read_pickle("./wafermap_withlabel.pkl")
    df_withpattern = df[(df['failureNum'] >= 0) & (df['failureNum'] <= 7)]
    df_withpattern = df_withpattern.reset_index()
    df_nonpattern = df[(df['failureNum'] == 8)]
    df_withpattern.info()

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


    def find_regions(x):
        rows = np.size(x, axis=0)
        cols = np.size(x, axis=1)
        ind1 = np.arange(0, rows, rows // 5)
        ind2 = np.arange(0, cols, cols // 5)

        reg1 = x[ind1[0]:ind1[1], :]
        reg3 = x[ind1[4]:, :]
        reg4 = x[:, ind2[0]:ind2[1]]
        reg2 = x[:, ind2[4]:]

        reg5 = x[ind1[1]:ind1[2], ind2[1]:ind2[2]]
        reg6 = x[ind1[1]:ind1[2], ind2[2]:ind2[3]]
        reg7 = x[ind1[1]:ind1[2], ind2[3]:ind2[4]]
        reg8 = x[ind1[2]:ind1[3], ind2[1]:ind2[2]]
        reg9 = x[ind1[2]:ind1[3], ind2[2]:ind2[3]]
        reg10 = x[ind1[2]:ind1[3], ind2[3]:ind2[4]]
        reg11 = x[ind1[3]:ind1[4], ind2[1]:ind2[2]]
        reg12 = x[ind1[3]:ind1[4], ind2[2]:ind2[3]]
        reg13 = x[ind1[3]:ind1[4], ind2[3]:ind2[4]]

        fea_reg_den = []
        fea_reg_den = [cal_den(reg1), cal_den(reg2), cal_den(reg3), cal_den(reg4), cal_den(reg5), cal_den(reg6),
                       cal_den(reg7), cal_den(reg8), cal_den(reg9), cal_den(reg10), cal_den(reg11), cal_den(reg12),
                       cal_den(reg13)]
        return fea_reg_den


    df_withpattern['fea_reg'] = df_withpattern.waferMap.apply(find_regions)

    def change_val(img):
        img[img == 1] = 0
        return img


    df_withpattern_copy = df_withpattern.copy()
    df_withpattern_copy['new_waferMap'] = df_withpattern_copy.waferMap.apply(change_val)

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
    df_withpattern_copy['fea_cub_mean'] = df_withpattern_copy.waferMap.apply(cubic_inter_mean)
    df_withpattern_copy['fea_cub_std'] = df_withpattern_copy.waferMap.apply(cubic_inter_std)
    df_all = df_withpattern_copy.copy()
    a = [df_all.fea_reg[i] for i in range(df_all.shape[0])]  # 13
    b = [df_all.fea_cub_mean[i] for i in range(df_all.shape[0])]  # 20
    c = [df_all.fea_cub_std[i] for i in range(df_all.shape[0])]  # 20
    d = [df_all.fea_geom[i] for i in range(df_all.shape[0])]  # 6
    fea_all = np.concatenate((np.array(a), np.array(b), np.array(c), np.array(d)), axis=1)  # 59 in total
    label = [df_all.failureNum[i] for i in range(df_all.shape[0])]
    label = np.array(label)

    df_all.to_csv('statisAttribute.csv',columns=['fea_reg','fea_cub_mean','fea_cub_std','fea_geom','failureType'])

    #----------------------------------------训练-------------------------------------------------
    from sklearn.svm import LinearSVC
    from sklearn.multiclass import OneVsOneClassifier
    from sklearn.cross_validation import train_test_split
    from sklearn.externals import joblib

    RANDOM_STATE = 42
    X = fea_all
    y = label
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    clf2 = OneVsOneClassifier(LinearSVC(random_state=RANDOM_STATE)).fit(X_train, y_train)
    #clf2.save_model('svm.model')
    joblib.dump(clf2, "svm.m")
    #clf2 = joblib.load("svm.m")
    #xgb_loadmodel = pickle.load(open("xbg.pickle.dat", "rb"))
    y_train_pred = clf2.predict(X_train)
    y_test_pred = clf2.predict(X_test)
    train_acc2 = np.sum(y_train == y_train_pred, axis=0, dtype='float') / X_train.shape[0]
    test_acc2 = np.sum(y_test == y_test_pred, axis=0, dtype='float') / X_test.shape[0]
    print('One-Vs-One Training acc: {}'.format(train_acc2 * 100))  # One-Vs-One Training acc: 80.36
    print('One-Vs-One Testing acc: {}'.format(test_acc2 * 100))  # One-Vs-One Testing acc: 79.04
    print("y_train_pred[:100]: ", y_train_pred[:100])
    print("y_train[:100]: ", y_train[:100])