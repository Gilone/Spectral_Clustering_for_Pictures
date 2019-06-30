import os
from PIL import Image


# 返回图片列表里面的图片名称
def get_photos(path, formats):
    if path == '':
        return ''
    else:
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(formats)]


# 处理输出路径
def set_outpath(file, name, path=''):
    r = os.path.join(path, file, name)
    b = os.path.join(path, file)
    if os.path.exists(b) == 0:    # 不存在就创建文件夹
        os.makedirs(b)
    r.replace('\\', '/')
    return r


# 处理输出文件名
def set_outname(no, fformat):
    return no+fformat


# 将图片格式变换为jpg
def change_format(filelist):
    for infile in filelist:
        outfile = os.path.splitext(infile)[0] + ".jpg"
        if infile != outfile:
            try:
                Image.open(infile).save(outfile)
            except IOError:
                print("cannot convert", infile)
