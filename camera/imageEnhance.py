import sys, os
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from transforms import RGBTransform
#import cv2
#import numpy as np

#def imageAlign(img, saveImg, obj=False):
#    if not obj:
#        img = cv2.imread(img)
#    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#    edges = cv2.Canny(gray,50,150,apertureSize = 3)
#    rows,cols, ch = img.shape
#    lines = cv2.HoughLines(edges,1,np.pi/180,200)
#    if len(lines) > 0:
#        for rho,theta in lines[0]:
#            a = np.cos(theta)
#            b = np.sin(theta)
#            x0 = a*rho
#            y0 = b*rho
            #x1 = int(x0 + 1000*(-b))
            #y1 = int(y0 + 1000*(a))
            #x2 = int(x0 - 1000*(-b))
            #y2 = int(y0 - 1000*(a))
            #print(theta)
            #print(a)
            #print(b)
#            if abs(a) > abs(b):
#                sign = 1 if a > 0 else -1
#            else:
#                sign = -1 if a > 0 else 1
            #cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
#            M = cv2.getRotationMatrix2D((cols/2,rows/2),theta*2*sign,1)
#            dst = cv2.warpAffine(img,M,(cols,rows))
#    if obj: 
#        return dst
#    else: 
#        cv2.imwrite(saveImg,dst)

def simpleImageEnhance(img, saveImg):
    img1 = Image.open(img)
    converter = ImageEnhance.Color(img1)
    img2 = converter.enhance(1.0)
    enhancer = ImageEnhance.Sharpness(img2)
    img3 = enhancer.enhance(2.0)
    contrast = ImageEnhance.Contrast(img3)
    img4 = contrast.enhance(1.75)
    img4 = img4.crop((316,58,1596,1018)) 
    img4 = img4.convert('RGB')
    img4 = RGBTransform().mix_with((100, 80, 100),factor=.30).applied_to(img4)
    img4.save(saveImg)

if __name__ == "__main__":
    simpleImageEnhance('mountain.jpg', 'enhanced_mountain.jpeg')

