import sys, os
from PIL import Image
from PIL import ImageEnhance

def simpleImageEnhance(img, saveImg):
    img1 = Image.open(img)
    converter = ImageEnhance.Color(img1)
    img2 = converter.enhance(1.5)
    enhancer = ImageEnhance.Sharpness(img2)
    img3 = enhancer.enhance(2.0)
    img3 = img3.crop((316,58,1596,1018)) 
    img3.save(saveImg)

if __name__ == "__main__":
    simpleImageEnhance('mountain.jpg', 'enhanced_mountain.jpeg')

