'''
https://learnopencv.com/image-filtering-using-convolution-in-opencv/

'''
import cv2
import numpy as np

image = cv2.imread('_images_must/test_image.jpg')
 
# Resim boşsa hata mesajı yazdır
if image is None:
    print('Could not read image')
 
# <identity kernel uygula>
kernel1 = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]])

# filter2D ile filtre uygulama
'''
filter2D(src, ddepth, kernel)

- İlk argüman kaynak görüntüdür
- İkinci argüman, ddepth elde edilen görüntünün derinliğini belirtir. -1 değeri, 
son görüntünün de kaynak görüntüyle aynı derinliğe sahip olacağını belirtir.
- Son girdi argümanı, kaynak görüntüye uyguladığımız filtre.
''' 
identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)

cv2.imshow('Original', image)
cv2.imshow('Identity', identity)
     
cv2.waitKey()
cv2.imwrite('_outputs/identity.jpg', identity)
cv2.destroyAllWindows()
 

# <blurring kernel uygula>
kernel2 = np.ones((5, 5), np.float32) / 25
img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2)
 
cv2.imshow('Original', image)
cv2.imshow('Kernel Blur', img)
     

cv2.waitKey()
cv2.imwrite('_outputs/blur_kernel.jpg', img)
cv2.destroyAllWindows()


# <blur() kullanarak bulanıklaştırma>
img_blur = cv2.blur(src=image, ksize=(5,5)) 

 
cv2.imshow('Original', image)
cv2.imshow('Blurred', img_blur)
 
cv2.waitKey()
cv2.imwrite('_outputs/blur.jpg', img_blur)
cv2.destroyAllWindows()


# <GaussianBlur() kullanarak bulanıklaştırma>
'''
GaussianBlur(src, ksize, sigmaX[, dst[, sigmaY[, borderType]]])

- İlk argüman kaynak görüntüdür
- İkinci argüman, Gauss çekirdeğinin boyutunu tanımlayan ksize. Burada 5x5 çekirdek kullanıyoruz.
- sigmaX ve sigmaY, her ikisi de 0'a ayarlanır. Bunlar, X(yatay) ve Y(dikey) yönündeki Gauss çekirdeği standart sapmalarıdır. 
sigmaY varsayılan ayarı sıfırdır. sigmaX i sıfıra ayarlarsanız, standart sapmalar çekirdek boyutundan 
(sırasıyla genişlik ve yükseklik) hesaplanır. Ayrıca her bağımsız değişkenin boyutunu sıfırdan büyük pozitif değerlere ayarlayabilirsiniz.
'''
gaussian_blur = cv2.GaussianBlur(src=image, ksize=(5,5), sigmaX=0, sigmaY=0)
 
cv2.imshow('Original', image)
cv2.imshow('Gaussian Blurred', gaussian_blur)
     
cv2.waitKey()
cv2.imwrite('_outputs/gaussian_blur.jpg', gaussian_blur)
cv2.destroyAllWindows()



# <medianBlur() kullanarak bulanıklaştırma>
'''
medianBlur(src, ksize)
- İlk argüman kaynak görüntüdür.
- İkincisi, tek, pozitif bir tamsayı olması gereken çekirdek boyutudur.
'''
median = cv2.medianBlur(src=image, ksize=5)

cv2.imshow('Original', image)
cv2.imshow('Median Blurred', median)
     
cv2.waitKey()
cv2.imwrite('_outputs/median_blur.jpg', median)
cv2.destroyAllWindows()



# <filter2D ile görüntü netleştirme>
kernel3 = np.array([[0, -1,  0],
                   [-1,  5, -1],
                    [0, -1,  0]])

sharp_img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel3)
 
cv2.imshow('Original', image)
cv2.imshow('Sharpened', sharp_img)
     
cv2.waitKey()
cv2.imwrite('_outputs/sharp_image.jpg', sharp_img)
cv2.destroyAllWindows()



# <Görüntüye ikili filtreleme uygulamak>
'''
bilateralFilter(src, d, sigmaColor, sigmaSpace)

- İlk argüman kaynak görüntüdür.
- Sonraki argüman d, filtreleme için kullanılan piksel komşuluğunun çapını tanımlar.
- Sonraki iki argümandan, (1D) sigmaColor renk yoğunluğu dağılımının ve (2D) sigmaSpace uzamsal dağılımın 
standart sapmasını tanımlar.
- sigmaSpace, hem x hem de y yönlerinde çekirdeğin uzamsal kapsamını tanımlar (tıpkı daha önce açıklanan 
Gauss bulanıklaştırma filtresi gibi).
- sigmaColor, piksel yoğunluğundaki farklılıkların tolere edilme derecesini belirten tek boyutlu 
Gauss dağılımını tanımlar.
'''
bilateral_filter = cv2.bilateralFilter(src=image, d=9, sigmaColor=75, sigmaSpace=75)

cv2.imshow('Original', image)
cv2.imshow('Bilateral Filtering', bilateral_filter)


cv2.waitKey(0)
cv2.imwrite('_outputs/bilateral_filtering.jpg', bilateral_filter)
cv2.destroyAllWindows()