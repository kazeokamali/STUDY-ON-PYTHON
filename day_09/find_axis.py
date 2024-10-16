from image_delete_blackline import Image_Information
from tqdm import tqdm
import os
import numpy as np

# global参数设置
column_default_index = 1350
critical_value = 0.7
# critical_value = 0.71

choose_file_path = r'C:\BrowserDownload\axis\p_d_1600'
out_set_val_path = r'C:\BrowserDownload\new_sett'

def is_value_background(val):
    if val >= critical_value:
        return True
    else:
        return False

# 继承I_I类
class image_axis_calibrate(Image_Information):

    # 二值化图像
    def value_set(self):

        self.get_length()

        for i in range( 1250,int( self.width )  ):
        #        for i in range( 1200 ):
            for j in range( int( self.height ) ):
                if is_value_background(self.get_pixel(i,j)):

                    self.set_pixel(i,j,1.0)

                else:
                    self.set_pixel(i,j,0.0)



    # 找到突变点的行数
    def find_mutate_point(self):

        self.get_length()

        mutate_row = []

        for j in  range(  10,int(self.height )-10 ) :

            i = column_default_index
#            print(f'pixel[{j}行] == {self.get_pixel(i,j)}')

            if  is_value_background(self.get_pixel(i,j)):

                if not is_value_background(self.get_pixel(i,j+1)):
                    if not  is_value_background(self.get_pixel(i,j+2)):
                        if not is_value_background(self.get_pixel(i,j+6)):
                            mutate_row.append(j+1)

                if not is_value_background(self.get_pixel(i,j-1)):
                    if not is_value_background(self.get_pixel(i,j-2)):
                        if not is_value_background(self.get_pixel(i, j - 6)):
                            mutate_row.append(j)

        return mutate_row


    def calc_center(self):
        self.get_length()
        y_poor = []
        for i in range( 1250,int(self.width) ):
            for j in range ( int(self.height) ):
                if not is_value_background( self.get_pixel(i,j) ) :
                    y_poor.append(j)

        return y_poor



def main_find():

    image_paths = [os.path.join(choose_file_path, img) for img in os.listdir(choose_file_path) if img.endswith('.tif')]

    '''
    for img_path in tqdm(image_paths,desc='set value'):
        try:
            temp_set_info = image_axis_calibrate(img_path)
            temp_set_info.value_set()
            new_set_path = os.path.join( out_set_val_path,os.path.basename(img_path).replace('.tif', 'set_.tif') )
            temp_set_info.convert_to_tif(new_set_path)


        except (IOError, IndexError) as e:
            print(f"Warning: Unable to process file {img_path}. Skipping... Error: {e}")
    '''

    record_center_axis = []

    for image_path in tqdm(image_paths, desc='img_find_mutate'):
        try:
            image_info = image_axis_calibrate(image_path)
            temp_list = image_info.find_mutate_point()

            # 调试输出
            print(f'Processing {image_path}---: {temp_list}')

            if len(temp_list) == 2:  # 确保有足够的突变点
                c = np.mean(temp_list)
                record_center_axis.append(c)
            else:
                print(f"Warning: Not enough  or too many mutate points found in {image_path}. Found: {len(temp_list)}")



        except (IOError, IndexError) as e:
            print(f"Warning: Unable to process file {image_path}. Skipping... Error: {e}")

    print(f'\n {record_center_axis} \n')

    if record_center_axis:  # 确保列表不为空以避免除以零
        sum_axis = sum(record_center_axis)
        average_axis = sum_axis / len(record_center_axis)

        print(f'{record_center_axis} \n')
        print(f'aver == {average_axis}')
    else:
        print("没有找到任何突变点。")

    image_paths_2 =  [os.path.join(out_set_val_path, img) for img in os.listdir(out_set_val_path) if img.endswith('.tif')]

    center_y_por = []
    for img_calc_all in tqdm(image_paths_2, desc='calcu center'):
        try:

            img_calc_info = image_axis_calibrate(img_calc_all)
            y_por = img_calc_info.calc_center()
            center_y_por.append( np.mean(y_por) )
            print(f'{np.mean(y_por)}')

        except (IOError, IndexError) as e:
            print(f"Warning: Unable to process file {img_calc_all}. Skipping... Error: {e}")


    if record_center_axis:  # 确保列表不为空以避免除以零
        sum_axis = sum(record_center_axis)
        average_axis = sum_axis / len(record_center_axis)

        print(f'{record_center_axis} \n')
        print(f'aver == {average_axis}')
    else:
        print("没有找到任何突变点。")

    print(f'{center_y_por}')
    print(f'\n center_y == { np.mean(center_y_por)}')





if __name__ == '__main__':

    main_find()

    print(f'All processed')
