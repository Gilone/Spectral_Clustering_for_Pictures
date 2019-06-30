from photos_operator import *
from PIL import Image
from pylab import *
from scipy.cluster.vq import *
import pca


def clustercore(clusteringmethod, get_path, out_path, vnumber, knumber, step, pbar):

    step += 1
    pbar.setValue(step)

    if (out_path == '') | (get_path == ''):
        return 0  # 输入或者输出路径未选择

    if clusteringmethod == 2:
        return 1  # 未选择聚类方法

    step += 1
    pbar.setValue(step)

    imlist = get_photos(get_path, '.jpg')    # 得到图片名称
    imnbr = len(imlist)

    if imnbr == 0:
        return 2  # 缺乏图片的情况

    pic = []
    kk = knumber

    step += 2
    pbar.setValue(step)

    if clusteringmethod == 0:   # 快速聚类

        for j in range(imnbr):
            pic.append(Image.open(imlist[j]).convert('L'))  # 对图像进行灰度化，去除颜色的干扰
            pic[j] = pic[j].resize((10, 10))        # 需要计算协方差矩阵，时间空间开销巨大，为了追求速度，需要将图片压缩

        immatrix = array([array(pic[i]).flatten() for i in range(imnbr)], 'f')  # 得到图像矩阵

        step += 16
        pbar.setValue(step)

        v, s, immean = pca.pca(immatrix)

        step += 30
        pbar.setValue(step)

        for i in range(imnbr):
            immatrix[i] = immatrix[i] - immean[i]

        step += 5
        pbar.setValue(step)

        projected = dot(immatrix, v[:vnumber].T)   # 完成图像的投影
        features = whiten(projected)

        step += 15
        pbar.setValue(step)

    else:    # 精准聚类
        for j in range(imnbr):
            pic.append(Image.open(imlist[j]).convert('L'))  # 对图像进行灰度化，去除颜色的干扰
            pic[j] = pic[j].resize((640, 480))     # 该算法本身速度较好，为了追求质量，保留图片大部分信息

        immatrix = array([array(pic[i]).flatten() for i in range(imnbr)], 'f')  # 得到图像矩阵

        step += 16
        pbar.setValue(step)

        n = len(immatrix)
        s = array([[sqrt(sum((immatrix[i]-immatrix[j])**2))for i in range(n)] for j in range(n)], 'f')  # 采用欧式距离判断

        step += 10
        pbar.setValue(step)

        rowsum = sum(s, axis=0)
        d = diag(1 / sqrt(rowsum))

        step += 10
        pbar.setValue(step)

        i = identity(n)
        l = i - dot(d, dot(s, d))

        step += 5
        pbar.setValue(step)

        u, sigma, v = linalg.svd(l)

        step += 15
        pbar.setValue(step)

        features = array(v[:kk]).T
        features = whiten(features)

        step += 10
        pbar.setValue(step)

    centroids, distortion = kmeans(features, kk)  # 返回聚类中心和方差
    code, distance = vq(features, centroids)      # 通过聚类中心进行分类

    step += (30 - (6*kk))
    pbar.setValue(step)

    for c in range(kk):
        ind = where(code == c)[0]
        figure()
        gray()
        for i in range(minimum(len(ind), 30)):
            im = Image.open(imlist[ind[i]])
            outname = set_outname(str(i), '.jpg')
            outpath = set_outpath(str(c+1), outname, out_path)     # 实现自定义输出路径和分文件夹存放
            im = im.convert('RGB')
            im.save(outpath)
            subplot(5, 6, i+1)
            imshow(array(im))
            axis('equal')
            axis('off')
        step += 6
        pbar.setValue(step)

    show()

    return 3


'''
谱聚类前使用PCA可能会损失更多图像信息，不使用虽然慢一点点，但是效果似乎更好
V, Ss, immean = pca.pca(immatrix)   
immean = immean.flatten()
projected = array([dot(immatrix[i]-immean, V[:10].T) for i in range(imnbr)])
projected = whiten(projected)
n = len(projected)
S = array([[sqrt(sum((projected[i]-projected[j])**2))for i in range(n)] for j in range(n)], 'f')
'''

'''
alpha = 1
S = array([[(numpy.e**(-1*((sum((immatrix[i]-immatrix[j])**2))/(2*(alpha**2)))))for i in range(n)] for j   
         in range(n)], 'f')    # 高斯核函数根本不可行
'''