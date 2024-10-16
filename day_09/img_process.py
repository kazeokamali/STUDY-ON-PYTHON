import math
import cv2
import os
import numpy as np
import rawpy
from PIL import Image
import tifffile as tiff

from scipy.constants import value


# global参数设置
black_line_lp = 2
black_line_lp_2 = 30
min_val_ofBlack = 200
max_val_ofBlack = 8000

choose_directory = input('输入包含待处理image的目录/路径')
# C:\BrowserDownload\raw_img
# C:\BrowserDownload\tet1
black_white_Filepath = r'C:\BrowserDownload\CT_pro'
# out_insert_path = r'C:\BrowserDownload\test'
out_bwsub_path = r'C:\BrowserDownload\w_b'
out_rbsub_path = r'C:\BrowserDownload\r_b'
out_b_insert = r'C:\BrowserDownload\test'
out_rb_inser_path = r'C:\BrowserDownload\rb_ins'

black_tif = black_white_Filepath + r'\black.tif'
white_tif = black_white_Filepath + r'\white.tif'

out_final_processed = r'C:\BrowserDownload\final'


# file_out_tiff = os.path.join('C:\BrowserDownload\CT_pro\ ', "out_tiff")
# file_out_p = os.path.join(choose_directory, "out_p")
# file_out_p_d = os.path.join(choose_directory, "out_p_d")
# os.makedirs(file_out_tiff, exist_ok=True)
# os.makedirs(file_out_p, exist_ok=True)
# os.makedirs(file_out_p_d, exist_ok=True)

# 判断像素值是否在规定范围
def is_valid(pixel):
    if min_val_ofBlack < pixel < max_val_ofBlack:
        return True
    else:
        return False

# 判断像素值是否梯度过大
def is_permitted(pixel,lp,rp):
    p_bar = lp + rp
    if abs(  (p_bar - pixel) / (pixel+1e-5) ) <= 30:
        return True
    else:
        return False


# I_I对象用于读取，计算，存储图像
class Image_Information():
    def __init__(self, path):
        self.image_path = path
        self.width = 0.0
        self.height = 0.0
        self.black_line_len = 0.0
        #        self.img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        #        with rawpy.imread(self.image_path) as raw:
        #            self.img = raw.postprocess()
        self.img = np.array(Image.open(self.image_path))

    '''
    def load_image(self):
        return cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
    '''

# 获取长宽信息
    def get_length(self):

        self.height, self.width = float(self.img.shape[0]), float(self.img.shape[1])

    '''
    def convert_to_tif(self,out_path):

        cv2.imwrite(out_path,self.img)
    '''
    '''
    def convert_to_tif(self, out_path):
        img_pil = Image.fromarray(self.img)
        img_pil.save(out_path)
    '''
# 以tif格式存储于path
    def convert_to_tif(self, out_path):
        # 确保图像数据为浮点数格式
        float_img = self.img.astype(np.float32)
        tiff.imwrite(out_path, float_img, dtype='float32')  # 保存为浮点数

# 获取某点像素值
    def get_pixel(self, x, y):

        pixel_value = self.img[y, x]

        return pixel_value

# 重置某点像素值为参数value
    def set_pixel(self, x, y, value):

        self.img[y, x] = value

    '''
    def image_subtract(self,other):

        black_1 = cv2.imread(black_tif, cv2.IMREAD_GRAYSCALE)
        white_1 = cv2.imread(white_tif, cv2.IMREAD_GRAYSCALE)

        result_1 = cv2.subtract(white_1,black_1)
    '''


# 用于图像的去坏线，w-b，r-b
    def image_calculate(self):

        self.get_length()
        lower_value_number = [0 for _ in range( int(self.width) )]
        value_column = [0.0 for _ in range( int(self.width ) )]

        for i in range( int(self.width  ) ):

            lower_value_number[i] = 0


            for j in range( int( self.height ) ):


                if not is_valid(self.get_pixel(i, j)):
                    #                if self.get_pixel(i,j) <= min_val_ofBlack or self.get_pixel(i,j) >= max_val_ofBlack:
                    lower_value_number[i] += 1


        #            print(f"Column {i}: all values = {column_values}")
        #           print(f"Column {i}: valid values = {valid_column_values}")



        black_line_len = (self.height / black_line_lp)
        delta_l = 1
        delta_r = 1
        temp = 0.0

        # 如果是坏线，左右线性插值
        # width溢出问题未解决
        for i in range(1, int( self.width-1 )):
            if lower_value_number[i] > black_line_len:
                for j in range(int( self.height )):
                    if is_valid(self.get_pixel(i - delta_l, j)):
                        temp = self.get_pixel(i - delta_l, j)
                    else:
                        while True:
                            delta_l += 1
                            if i - delta_l >= 0:
                                if is_valid(self.get_pixel(i - delta_l, j)):
                                    temp = self.get_pixel(i - delta_l, j)
                                    break
                            else:
                                if delta_l > 1:
                                    delta_l -= 1
                                    break
                    if is_valid(self.get_pixel(i + delta_r, j)):
                        temp += self.get_pixel(i + delta_r, j)
                    else:
                        while True:
                            delta_r += 1
                            if i + delta_r <= self.width - 1:
                                if is_valid(self.get_pixel(i + delta_r, j)):
                                    temp += self.get_pixel(i + delta_r, j)
                                    break
                            else:
                                if delta_r > 1:
                                    delta_r -= 1
                                    break
                    temp = temp / (delta_l + delta_r)
                    self.set_pixel(i, j, temp)
                    temp = 0.0
                    delta_l = 1
                    delta_r = 1

# r-b没去掉的黑线，二次进行去坏线
    def image_inserted_delete_bline(self):
        self.get_length()
        lower_value_number = [0 for _ in range( int( self.width ) )]

        for i in range(1, int( self.width-1 ) ):
            lower_value_number[i] = 0
            for j in range(int( self.height )):
                if not is_permitted(self.get_pixel(i, j),self.get_pixel(i-1, j),self.get_pixel(i+1, j) ):
                    lower_value_number[i] += 1

        black_line_len = self.height / black_line_lp_2


        for i in range(1, int( self.width-1 )):
            if lower_value_number[i] >= black_line_len:
                print(f'2坏线列：{i}')
                for j in range(int( self.height )):
                    temp =  float( self.get_pixel(i-1,j) + self.get_pixel(i+1,j) )
                    temp = temp/2.0
                    self.set_pixel(i,j,temp)

    #        self.convert_to_tif(out_insert_path)
    '''
    def image_subtract(self,other):
        self.get_length()
        other.get_length()

        for i in range(self.width):
            for j in range(self.height):
                temp_val = self.get_pixel(i,j) - other.get_pixel(i,j)
                if temp_val >= 0:
                    self.set_pixel(i,j,temp_val)
                else:
                    self.set_pixel(i,j,0)


    def image_divide(self,other):
        self.get_length()
        other.get_length()

        for i in range(self.width):
            for j in range(self.height):
#                temp_val = (self.get_pixel(i, j) * abs( self.get_pixel(i, j) - other.get_pixel(i,j) )/ (self.get_pixel(i, j) + other.get_pixel(i,j)))

                if other.get_pixel(i,j) != 0:
                    temp_val = round(  self.get_pixel(i, j) /  other.get_pixel(i,j) )
                else:
                    temp_val = self.get_pixel(i,j)


                self.set_pixel(i, j,temp_val)


    def image_divide(self, other):
        try:
            self.get_length()
            other.get_length()

            # 确保两个图像的尺寸相同
            if self.width != other.width or self.height != other.height:
                raise ValueError("Images must have the same dimensions.")

            self_img = self.img.astype(np.float32)
            other_img = other.img.astype(np.float32)

            with np.errstate(divide='ignore', invalid='ignore'):
                result = np.where(other_img != 0, self_img / other_img, 0)

            result = np.clip(result, 0, 255).astype(np.uint8)
            self.img = result
        except Exception as e:
            print(f"Error in image_divide: {e}")
    '''

# 图像减法，w-b，r-b的具体实现
    def image_subtract(self, other):
        self.get_length()
        other.get_length()

        # 将图像转换为浮点数以避免溢出
        self_img = self.img.astype(np.float32)
        other_img = other.img.astype(np.float32)

        # 执行减法，允许负数输出
        result = self_img - other_img

        # 将结果保存为浮点数，不进行裁剪
        self.img = result  # 保持为浮点数

# r-b / w-b 的具体实现
    def image_divide(self, other):
        try:
            self.get_length()
            other.get_length()

            # 确保两个图像的尺寸相同
            if self.width != other.width or self.height != other.height:
                raise ValueError("Images must have the same dimensions.")

            # 将图像转换为浮点数以避免溢出
            self_img = self.img.astype(np.float32)
            other_img = other.img.astype(np.float32)

            with np.errstate(divide='ignore', invalid='ignore'):
                # 进行除法运算，避免除以零
                result = np.where(other_img != 0, self_img / other_img, 0)

            # 不进行裁剪，保持浮点数格式
            self.img = result  # 保持为浮点数
        except Exception as e:
            print(f"Error in image_divide: {e}")


def main():
    # 选择处理文件路径，需tif格式文件
    image_paths = [os.path.join(choose_directory, img) for img in os.listdir(choose_directory) if img.endswith('.tif')]

    # 白减黑背底
    black_info = Image_Information(black_tif)
    white_info = Image_Information(white_tif)
    w_b_path = os.path.join(out_bwsub_path, os.path.basename(white_tif).replace('.tif', '_result.tif'))
    white_info.image_subtract(black_info)
    white_info.convert_to_tif(w_b_path)

    # w-b进行初次插值去坏线
    white_sub_black = w_b_path
    w_sub_b_info = Image_Information(white_sub_black)
    w_sub_b_info.image_calculate()
    w_b_insert_path = os.path.join(out_bwsub_path, os.path.basename(white_tif).replace('.tif', '_result_insert.tif'))
    w_sub_b_info.convert_to_tif(w_b_insert_path)
    print(w_b_insert_path)
    last_denominator = Image_Information(w_b_insert_path)

    # 黑背底初次去坏线
    black_info.image_calculate()
    black_insert_path = os.path.join(out_b_insert, os.path.basename(black_tif).replace('.tif', 'b_i.tif'))
    black_info.convert_to_tif(black_insert_path)
    b_insert_info = Image_Information(black_insert_path)

    # 对选择的目录下文件进行减黑背底，并初次去坏线
    for image_path in image_paths:
        try:
            image_info = Image_Information(image_path)
            image_info.image_subtract(b_insert_info)
            image_info.image_calculate()
            raw_b_path = os.path.join(out_rbsub_path, os.path.basename(image_path).replace('.tif', '_sub_result.tif'))
            image_info.convert_to_tif(raw_b_path)

        except IOError:
            print(f"Warning: Unable to process file {image_path}. Skipping...")

    # r-b后二次去坏线
    o_rb_path = [os.path.join(out_rbsub_path, img) for img in os.listdir(out_rbsub_path) if img.endswith('.tif')]
    for i in o_rb_path:
        try:
            r_sub_b_info = Image_Information(i)
            r_sub_b_info.image_inserted_delete_bline()
            r_b_sub_insert_path = os.path.join(out_rb_inser_path, os.path.basename(i).replace('.tif', 'rb_sub_ins.tif'))
            r_sub_b_info.convert_to_tif(r_b_sub_insert_path)

        except IOError:
            print(f"Warning: Unable to process file {i}. Skipping...")

    last_step_img_paths = [os.path.join(out_rb_inser_path, img) for img in os.listdir(out_rb_inser_path) if
                           img.endswith('.tif')]

    # r-b/w-b
    for last_path in last_step_img_paths:
        try:
            img_info = Image_Information(last_path)
            img_info.image_divide(last_denominator)
            #            img_info.image_subtract(last_denominator)
            final_path = os.path.join(out_final_processed, os.path.basename(last_path).replace('.tif', 'final.tif'))
            img_info.convert_to_tif(final_path)
        except IOError:
            print(f"Warning: Unable to process file {last_path}. Skipping...")


if __name__ == '__main__':
    main()
    print(f'All processed')








