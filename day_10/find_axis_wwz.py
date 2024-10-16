import cv2
import numpy as np
import os
from PIL import Image

'''
def Bit16to8(Proj_path,Proj_path_8bit): #导入16位文件输入路径和8位文件输出路径
    bacepath = Proj_path #将导入的文件地址进行命名
    savepath = Proj_path_8bit

    f_n  = os.listdir(bacepath) #读取文件列表
    #print(f_n)
    for n in f_n: #对文件列表进行遍历
        imdir = bacepath + '/' + n
        #print(imdir)
        img = cv2.imread(imdir) #opencv读取文件
        #print(img)
        cropped = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #将图像转换为灰度图
        cv2.imwrite(savepath + '/' +n.split('.')[0]+'_8bit.tif', cropped)#不改变图像类型，存储图像
'''

def Bit16to8(importpath, importpath_8bit):
    img = Image.open(importpath)
    img = img.convert("I;16")  # 转换为 16 位图像
    img_array = np.array(img)

    # 将 16 位图像归一化到 8 位
    img_8bit = cv2.normalize(img_array, None, 0, 255, cv2.NORM_MINMAX)
    img_8bit = np.uint8(img_8bit)  # 转换为 8 位图像

    cv2.imwrite(importpath_8bit, img_8bit)  # 保存 8 位图像

def threshold_By_OTSU(input_img_file,projs_num): #导入8位文件输入路径和图像数量
    center_x_data = np.zeros(projs_num) #创建与图像数量等同的0数组，用于存放每张图的图像中心
    f_n = [os.path.join(input_img_file, img) for img in os.listdir(input_img_file) ]
    for filename in os.listdir(input_img_file):
        print(filename)
    num = -1 #图像索引计数
    for n in f_n: #对文件列表进行遍历

        image=cv2.imread(n)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   ##要二值化图像，必须先将图像转为灰度图
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) #对图像进行二值化

        cv2.waitKey(0)
        cv2.destroyAllWindows()


        size=binary.shape #获取图像的尺寸
        w=binary.shape[1]
        h=binary.shape[0]
        zero_number = 0 #计算灰度值为零的像素个数
        x_coor = 0 #计算灰度值为零的坐标并进行累加
        for y in range(h): #先对y方向进行遍历
            for x in range(w): #然后对x方向进行遍历
                if binary[y,x] == 0: #如果有0值就记录，然后计数并累加坐标
                    zero_number += 1
                    x_coor = x + x_coor

        center_x = x_coor/zero_number #对整张图象遍历完以后可得出坐标和and像数和，由此得出图像中心
        num += 1 #每计算完一张，num作为计数器就＋1，然后打印出来告知用户目前进度
        print(num)
        center_x_data[num] = center_x #对于每一张图像的中心都放到先前的0数组中存储
    X_axis_center = np.mean(center_x_data) #将所有的0数组填充完成后，求取所有图像中心的中心值，就是旋转中心
    print("旋转轴中心是",X_axis_center)
    return X_axis_center #将旋转中心传给上一级的函数

def Automatic_correction(Proj_path,Proj_path_8bit,projs_num):#将用于计算旋转中心的量都传给枢纽函数，包括16位图像/8位图像路径还有图像数量
    importpath_8bit = Proj_path_8bit #将传进来的形参重新命名，包括（16位图像/8位图像路径还有图像数量），便于查看
    importpath = Proj_path
    projsnum = projs_num
    Bit16to8(importpath,importpath_8bit) #执行图像位数转换
    return_center = threshold_By_OTSU(importpath_8bit,projsnum) #执行旋转中心找回
    return return_center #返回旋转中心值

if __name__ == '__main__':


    Proj_path = r'C:\BrowserDownload\axis\p_d_1600'
    Proj_path_8bit = r'C:\BrowserDownload\new_set_wwz'
    projs_num = input('nums of img ==')
    u_offset = Automatic_correction(Proj_path,Proj_path_8bit,projs_num) #调用前面的枢纽函数，将找回的中心赋给u_offset