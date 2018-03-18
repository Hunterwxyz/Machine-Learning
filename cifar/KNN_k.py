#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 3/17/2018 15:30
# @Author   : YLD10
# @Email    : yl1315348050@yahoo.com
# @File     : KNN_k.py
# @Software : PyCharm
# @reference: https://zhuanlan.zhihu.com/p/20894041?refer=intelligentunit

import pandas as pd
import numpy as np
import matplotlib as mpl
import scipy.misc as mi


class NearestNeighbor(object):
    def __init__(self):
        self.xtr = 0
        self.ytr = 0
        pass

    def train(self, x_l, y_l):
        """ x is N x D where each row is an example. y is 1-dimension of size N """
        # the nearest neighbor classifier simply remembers all the training data
        self.xtr = x_l
        self.ytr = y_l

    def predict(self, x_l, k_l=1):
        """ x is N x D where each row is an example we wish to predict label for """
        num_test = x_l.shape[0]
        # lets make sure that the output type matches the input type
        ypred = np.zeros(num_test, dtype=self.ytr.dtype)

        # loop over all test rows
        for i_l in range(num_test):
            print(i_l)
            # find the nearest training image to the i'th test image
            # using the L1 distance (sum of absolute value differences)
            distances = np.sum(np.abs(self.xtr - x_l[i_l, :]), axis=1)
            # distances = np.sqrt(np.sum(np.square(self.xtr - x[i, :]), axis=1))  # L2 distance
            # print(distances.shape)
            topn_index = np.argsort(distances)[:k_l]  # get the index with top k_l small distance
            topn_label = self.ytr[topn_index]  # indexs are converted into labels
            # print(topn_label)
            tmp_list = sorted([(np.sum(topn_label == e), e) for e in set(topn_label)])  # 统计各标签的出现次数
            # print(tmp_list)
            most_label = tmp_list[-1][1]  # 取出重复次数最多的标签
            # print(most_label)
            ypred[i_l] = most_label  # predict the label of the k_l nearest example

        return ypred


# 加载pickle压缩的包
def unpickle(file):
    import pickle

    with open(file, 'rb') as fo:
        dic = pickle.load(fo, encoding='bytes')
    return dic


# 加载cifar-10的所有数据
def load_cifar10(file_path):
    # print('yte_l: ', yte_l.shape)
    dic_d1 = unpickle(file_path + data1_file)
    dic_d2 = unpickle(file_path + data2_file)
    dic_d3 = unpickle(file_path + data3_file)
    dic_d4 = unpickle(file_path + data4_file)
    dic_d5 = unpickle(file_path + data5_file)
    dic_t = unpickle(file_path + test_file)

    print(dic_d1)

    xtr_l = np.concatenate(
        [dic_d1[b'data'], dic_d2[b'data'], dic_d3[b'data'], dic_d4[b'data'], dic_d5[b'data']],
        axis=0)  # 多维数组按行(竖向)拼接
    # print('xtr_l: ', xtr_l.shape)
    xte_l = dic_t[b'data']
    # print('xte_l: ', xte_l.shape)

    ytr_l = np.concatenate(
        [dic_d1[b'labels'], dic_d2[b'labels'], dic_d3[b'labels'], dic_d4[b'labels'], dic_d5[b'labels']],
        axis=0)  # 一维数组默认按列(横向)拼接
    # print('ytr_l: ', ytr_l.shape)
    yte_l = np.array(dic_t[b'labels'])

    return xtr_l, ytr_l, xte_l, yte_l


# 只取前n个图像数据进行训练和测试
def cut_x_y(xtr_l, ytr_l, xte_l, yte_l, n_l=100):
    return xtr_l[:n_l, :], ytr_l[:n_l], xte_l[:n_l, :], yte_l[:n_l]


if __name__ == '__main__':
    # 设置控制台显示宽度以及取消科学计数法
    pd.set_option('display.width', 300)
    np.set_printoptions(suppress=True)

    # 解决图表的中文以及负号的乱码问题
    mpl.rcParams['font.sans-serif'] = [u'simHei']
    mpl.rcParams['axes.unicode_minus'] = False

    MODEL_PATH = './'
    CIFAR_PATH = 'cifar-10/cifar-10-python/cifar-10-batches-py/'

    batches = 'batches.meta'
    data1_file = 'data_batch_1'
    data2_file = 'data_batch_2'
    data3_file = 'data_batch_3'
    data4_file = 'data_batch_4'
    data5_file = 'data_batch_5'
    test_file = 'test_batch'

    # 保存第一张图片，验证图片数据是否准确提取
    # img_dict = unpickle(MODEL_PATH + CIFAR_PATH + data1_file)
    #
    # # print(img_dict[b'data'].dtype)
    #
    # r = np.zeros((32, 32), dtype=img_dict[b'data'].dtype)
    # g = np.zeros((32, 32), dtype=img_dict[b'data'].dtype)
    # b = np.zeros((32, 32), dtype=img_dict[b'data'].dtype)
    #
    # r = img_dict[b'data'][:1, :1024].reshape(32, 32)
    # g = img_dict[b'data'][:1, 1024:2048].reshape(32, 32)
    # b = img_dict[b'data'][:1, 2048:].reshape(32, 32)
    #
    # print(r)
    # print(g)
    # print(b)
    #
    # img = np.dstack([r, g, b])
    #
    # print(img.shape)
    #
    # mi.imsave('one.jpg', img)

    # 设置要训练的数据量
    ntr = 1000
    nval = int(ntr * 0.2)

    xtr, ytr, xte, yte = load_cifar10(MODEL_PATH + CIFAR_PATH)
    xtr, ytr, xte, yte = cut_x_y(xtr, ytr, xte, yte, ntr)  # 减少数据量至ntr个，缩短时间

    # 增加验证集，从训练集中划分出来
    xval = xtr[:nval, :]  # take first nval for validation
    yval = ytr[:nval]
    xtr = xtr[nval:, :]  # keep last ntr-nval for train
    ytr = ytr[nval:]

    print('xtr: ', xtr.shape)  # 50000 x 3072
    print('xte: ', xte.shape)  # 10000 x 3072
    print('ytr: ', ytr.shape)  # 1 x 50000
    print('yte: ', yte.shape)  # 1 x 10000

    # find hyperparameters that work best on the validation set
    validation_accuracies = []
    for k in range(1, 15):
        # use a particular value of k and evaluation on validation data
        nn = NearestNeighbor()  # create a Nearest Neighbor classifier class
        nn.train(xtr, ytr)  # train the classifier on the training images and labels
        # here we assume a modified NearestNeighbor class that can take a k as input
        yval_predict = nn.predict(xval, k_l=k)  # predict labels on the validation images
        # and now print the classification accuracy, which is the average number
        # of examples that are correctly predicted (i.e. label matches)
        acc = np.mean(yval_predict == yval)
        print('accuracy: %f' % (acc,))

        # keep track of what works on the validation set
        validation_accuracies.append((k, acc))

    print(validation_accuracies)
