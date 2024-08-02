from flask import Flask, request
from PIL import Image
import cv2
import numpy as np
from flask_cors import CORS
import os
save_directory = 'uploadimg'
app = Flask(__name__)
CORS(app)  # 允许所有来源的请求
stored_data = {}


    #高斯模糊
def apply_gaussian_blur(image_array, kernel_size=(5, 5), sigmaX=10):
    blurred = cv2.GaussianBlur(image_array, kernel_size, sigmaX)
    return blurred

    #中值模糊
def apply_median_blur(image_array, ksize=5):
    blurred = cv2.medianBlur(image_array, ksize)
    return blurred
    #双边滤波
def apply_bilateral_filter(image_array, d=9, sigmaColor=75, sigmaSpace=75):
    filtered = cv2.bilateralFilter(image_array, d, sigmaColor, sigmaSpace)
    return filtered


def jointimg(imageori,imageprocess):
    width1, height1 = imageori.size
    width2, height2 = imageprocess.size
    new_width = width1 + width2
    new_height = height1

    new_img = Image.new('RGB', (new_width, new_height))

    new_img.paste(imageori, (0, 0))
    new_img.paste(imageprocess, (width1, 0))

    return new_img


def joint4img(imageori,modifyimg,grayimg,blurimg):
    grayimg = grayimg.convert('RGB')

    width,height = imageori.size

    new_width = 2*width
    new_height = 2*height

    new_img = Image.new('RGB',(new_width,new_height))

    new_img.paste(imageori, (0, 0))
    new_img.paste(grayimg,(0,height))
    new_img.paste(blurimg,(width,height))


    new_img.paste(modifyimg,(width,0))

    return new_img




def enhanceImg(file):
    global stored_data

    image = Image.open(file)
    #image.show()
    image_array = np.array(image)

    # 裁剪/缩放
    modifysize = stored_data['modifysize']
    width, height = modifysize.split('*')
    width = int(width)
    height = int(height)
    # 图片实际大小
    img_height, img_width = image_array.shape[:2]
    if (int(stored_data['radiochoice']) == 2):
        modifyimg = cv2.resize(image_array, (width, height))
    else:
        # 裁剪图片为矩形
        x_center = img_width // 2
        y_center = img_height // 2

        x1 = max(0, x_center - width // 2)
        x2 = min(img_width, x_center + width // 2)
        y1 = max(0, y_center - height // 2)
        y2 = min(img_height, y_center + height // 2)

        if x2 - x1 < width:
            x1 = max(0, x2 - width)
        if y2 - y1 < height:
            y1 = max(0, y2 - height)

        modifyimg = image_array[y1:y2, x1:x2]
    modify_img = Image.fromarray(modifyimg)
    modify_img.show()


    #转换灰度图片
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    if(int(stored_data['radiocompar']) == 1):
        print(1)
        gray_img = cv2.equalizeHist(gray)
    # Convert the NumPy array to a PIL Image
    gray_img = Image.fromarray(gray)
    gray_img.show()


    # 降噪
    if(stored_data['methodsblur'] == 1):
        # 高斯模糊
        xsigma = int(stored_data['gsPara']['xsigma'])
        kernel = int(stored_data['gsPara']['kernel'])
        gaussian_blurred = apply_gaussian_blur(image_array, (kernel, kernel),xsigma)
        denoise_img = Image.fromarray(gaussian_blurred)  # 显示高斯模糊结果
    elif(stored_data['methodsblur'] == 2):
        # 中值模糊
        kernel = int(stored_data['mdPara']['kernel'])
        median_blurred = apply_median_blur(image_array, kernel)
        denoise_img = Image.fromarray(median_blurred)  # 显示中值模糊结果
    else:
        # 双边滤波
        dpara = int(stored_data['sidePara']['dPara'])
        sigma = int(stored_data['sidePara']['sigma'])
        sigmaspace = int(stored_data['sidePara']['sigmaspace'])
        bilateral_filtered = apply_bilateral_filter(image_array, dpara, sigma, sigmaspace)
        denoise_img = Image.fromarray(bilateral_filtered)  # 显示双边滤波结果

    result_img = jointimg(image,denoise_img)
    result_img.show()

    #保存 拼接
    result_joint4img = joint4img(image,gray_img,modify_img,denoise_img)
    result_joint4img.show()
    gray_img.save(os.path.join(save_directory, 'gray_img.jpg'))
    modify_img.save(os.path.join(save_directory, 'modify_img.jpg'))
    denoise_img.save(os.path.join(save_directory, 'denoise_img.jpg'))
    result_joint4img.save(os.path.join(save_directory, 'joint_img.jpg'))


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']

        if file.filename == '':
            return 'No selected file', 400

        if file:
            file.save(f"uploadimg/{file.filename}")
            return 'File successfully uploaded', 200
    except Exception as e:
        # 捕获并输出详细错误信息
        return f'An error occurred: {e}', 500

@app.route('/processimg',methods=['POST'])
def process_img():
    try:
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']

        if file.filename == '':
            return 'No selected file', 400

        if file:

            enhanceImg(file)
        return 'File successfully uploaded', 200
    except Exception as e:
        # 捕获并输出详细错误信息
        return f'An error occurred: {e}', 500

@app.route('/testpara',methods=['POST'])
def printPara():
    global stored_data

    request_data = request.get_json()
    stored_data = request_data
    # 打印请求体
    print(request_data)
    return "Data received", 200


if __name__ == '__main__':
    app.run(debug=True)
