import sys, os
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageFilter
from transforms import RGBTransform

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

