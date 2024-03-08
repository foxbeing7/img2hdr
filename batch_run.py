# -*- coding: utf-8 -*-
'''
LDR到HDR批量，输入一个图片文件夹，会在输出目录得到对应的HDR包括: 1. png
                                                      2. hdr

'''
import os
import time

import cv2
import numpy as np
from src.hdr import FakeHDR
import imageio

def batch_process_images(folder_path,output_path):

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    #test
    # 创建 FakeHDR 对象
    hdr_filter = FakeHDR(True)
    # True: 使用加权融合; False: 平均融合。

    # 获取文件夹中所有图片文件的路径
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)
                   if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # 读取图像文件
        image = cv2.imread(image_file, -1)
        single_image_time1 = time.time()
        # 添加 HDR 过滤器并处理图像
        output_image = hdr_filter.process(image)

        # 生成输出文件名
        image_name, image_extension = os.path.splitext(os.path.basename(image_file))
        # 这里将生成的文件名写成输入的文件名+后缀的形式
        png_filename = f'{image_name}_hdr.png'

        output_filename = f'{image_name}_hdr.hdr'


        # 保存 HDR 图像
        hdr_path = os.path.join(output_path, output_filename)
        png_path = os.path.join(output_path, png_filename)

        cv2.imwrite(png_path, 255 * output_image)


        img_normalized = output_image.astype(np.float32)

        # 转换为线性RGB色彩空间,其实就是tonemapping后进行了伽马校正，现在要保存为.hdr的话还要进行回调
        linear_rgb = np.where(img_normalized <= 0.04045, img_normalized / 12.92,
                              ((img_normalized + 0.055) / 1.055) ** 2.4)

        # 保存为HDR格式
        cv2.imwrite(hdr_path, linear_rgb)
        single_image_time2 = time.time()
        cac_time = single_image_time2 - single_image_time1
        print(f'成功处理{image_file} -> 保存在 {output_path}, 用时{cac_time}秒.')

if __name__ == '__main__':
    folder_path = './test_image/229'
    output_path = './result/229'
    start_time = time.time()
    batch_process_images(folder_path,output_path)
    end_time = time.time()
    time_cac = end_time - start_time
    print(f'LDR to HDR完成，总共用时{time_cac}秒')
