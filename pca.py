from numpy import *


def pca(data):
    num_data, dim = data.shape
    mean_data = data.mean(axis=1)  # 当处理自然图像时，将每个特征减去图像本身的均值，而不是减去该特征的均值
    for i in range(num_data):
        data[i] = data[i] - mean_data[i]
    if dim > num_data:
        m = dot(data.T, data)/dim  # 协方差矩阵
        ee, ev = linalg.eigh(m)
        s = sqrt(ee)
        v = ev
    else:
        u, s, v = linalg.svd(data)
        v = v[:num_data]        # 为了将对应的，奇异值为零的量舍去
    return v, s, mean_data

