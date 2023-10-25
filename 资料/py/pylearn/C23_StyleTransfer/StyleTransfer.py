import glob,os
import cv2 as cv    #导入opencv库
from matplotlib import pyplot as plt

class App:
    def __init__(self):
        self.idxImage = 0   #当前被风格迁移的图片在images列表中的下标
        self.idxModel = 0   #当前使用的模型文件在models列表中的下标
        self.images = glob.glob("images/*.jpg")  
        self.paintings,self.models = [],[] 
        t = glob.glob("models/*.jpg")
        for x in t:
            m = x[:-3] + "t7"       #模型文件的扩展名为.t7, 基本名与对应的风格图片相同
            if os.path.exists(m):   #仅在风格图片及模型文件同时存在时，将二者加入列表
                self.paintings.append(x)
                self.models.append(m)

    def styleTransfer(self):
        net = cv.dnn.readNetFromTorch(self.models[self.idxModel])
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        inImg = cv.imread(self.images[self.idxImage])
        inp = cv.dnn.blobFromImage(inImg, 1.0, (inImg.shape[1],inImg.shape[0]),
                              (103.939, 116.779, 123.68), swapRB=False, crop=False)
        net.setInput(inp)
        outImg = net.forward()
        outImg = outImg.reshape(3, outImg.shape[2], outImg.shape[3])
        outImg[0] += 103.939
        outImg[1] += 116.779
        outImg[2] += 123.68
        outImg /= 255
        outImg = outImg.transpose(1, 2, 0)
        return inImg, outImg

    def refresh(self,fig,axStyle,axIn,axOut):
        print("Style tranfering...")
        self.idxImage = self.idxImage % len(self.images)
        self.idxModel = self.idxModel % len(self.models)
        inImg, outImg = self.styleTransfer()
        print("Rendering...")
        styleImg = cv.imread(self.paintings[self.idxModel])
        axStyle.imshow(cv.cvtColor(styleImg,cv.COLOR_BGR2RGB))
        axIn.imshow(cv.cvtColor(inImg, cv.COLOR_BGR2RGB))
        axOut.imshow(cv.cvtColor(outImg, cv.COLOR_BGR2RGB))
        fig.canvas.draw()

def on_key_release(event):
    if event.key == 'up':
        app.idxImage-=1
    elif event.key == 'down':
        app.idxImage+=1
    elif event.key == 'left':
        app.idxModel-=1
    elif event.key == 'right':
        app.idxModel+=1
    else:
        return
    app.refresh(fig,axStyle,axIn,axOut)


app = App()
if len(app.images) == 0:
    print("No pictures found in sub-dir images.") 
    exit()   
if len(app.models) == 0:
    print("No trained model files found in sub-dir models, download first.")
    exit()

fig = plt.figure(figsize=(12,6))
axStyle = plt.subplot(231)
axIn = plt.subplot(234)
axOut = plt.subplot2grid((2,3),(0,1),rowspan=2,colspan=2)
plt.subplots_adjust(0,0,1,1,0,0)
for ax in (axStyle,axIn,axOut):
    ax.set_axis_off()
app.refresh(fig,axStyle,axIn,axOut)
fig.canvas.mpl_connect('key_release_event',on_key_release)
plt.show()