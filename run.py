from src.hdr import *
import os.path as osp


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage:  python run.py [image_path]")
        sys.exit()

    image_path = sys.argv[1]
    image_name, image_extension = osp.splitext(osp.basename(image_path))

    # 读取图像文件
    image = cv2.imread(image_path, -1)

    # 添加 HDR 过滤器
    # True: 使用加权融合; False: 平均融合。
    HDR_Filer = FakeHDR(True)
    output_image = HDR_Filer.process(image)

    # 保存和显示最终结果
    output_filename = f'./result/{image_name}_hdr{image_extension}'

    hdr_output_path = f'./result/{image_name}_hdr.hdr'

    cv2.imwrite(hdr_output_path, 255 * output_image)
    cv2.imwrite(output_filename, 255 * output_image)

    # Show_origin_and_output(image, output_image)

