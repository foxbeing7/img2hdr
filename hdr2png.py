# -*- coding: utf-8 -*-

# 用于将HDR格式的文件转成PNG方便可视化， 颜色上会有一定的丢失。

import os
import cv2
import time

def loadHdr(imName):
    im = cv2.imread(imName)[:, :, ::1]
    return im



def batchConvertHdrToPng(inputFolder, outputFolder):


    if not os.path.exists(inputFolder):
        print(f'{inputFolder}路径不存在，检查路径是否正确。')
        return

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    count = 0
    # 遍历输入文件夹中的所有HDR图像
    for filename in os.listdir(inputFolder):
        if filename.endswith(".hdr"):
            # 构建输入和输出文件路径
            inputPath = os.path.join(inputFolder, filename)
            outputFilename = os.path.splitext(filename)[0] + "_hdr.png"
            outputPath = os.path.join(outputFolder, outputFilename)

            imBatch = loadHdr(inputPath)
            cv2.imwrite(outputPath, imBatch)
            count += 1
            print(f"{inputPath} to {outputPath}")
    return count

inputFolder = "./input_folder"
outputFolder = "./output_folder"
if __name__ == '__main__':
    time1 = time.time()
    num = batchConvertHdrToPng(inputFolder, outputFolder)
    time2 = time.time()
    cost_time = round(time2 - time1,1)
    print(f'转换成功，一共处理了{num}张图像，HDR保存在{outputFolder},共用时{cost_time}')
