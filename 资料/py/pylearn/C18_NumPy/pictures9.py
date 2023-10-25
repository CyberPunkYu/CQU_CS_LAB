import glob
import numpy as np
from cv2 import imread,imwrite

imgs,heights,widths = [],[],[]
for f in glob.glob("pictures/*.jpg"):
    img = imread(f,-1)
    print("original:",img.shape)
    h,w = img.shape[:2]
    heights.append(h)
    widths.append(w)
    imgs.append(img)

#制作缩略图，纵横向每3个像素抽一个
minHeight = min(heights)
minWidth = min(widths)
for i,x in enumerate(imgs):
    imgs[i] = x[:minHeight:3,:minWidth:3,:]
    print("thumbnail:",imgs[i].shape)

#横向沿轴1拼接
img = np.concatenate(imgs,1)
print("concatenated by axis1:",img.shape)
imwrite("concatenated_1.jpg",img)

#方法1
img0 = np.concatenate(imgs[:3],1)
img1 = np.concatenate(imgs[3:6],1)
img2 = np.concatenate(imgs[6:],1)
img9 = np.concatenate([img0,img1,img2],0)
print("3x3_0, shape:",img9.shape)
imwrite("3x3_0.jpg",img9)

#方法2
img = np.concatenate(imgs,0)
img1 = img.reshape(3,3,265,427,3)
# imwrite("0_1.jpg",img1[0][1])
# imwrite("2_0.jpg",img1[2][0])

img9 = img1.swapaxes(1,2).reshape(795,1281,3)
print("3x3_1, shape:",img9.shape)
imwrite("3x3_1.jpg",img9)

