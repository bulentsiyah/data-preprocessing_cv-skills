'''
Hough dönüşümü, bir görüntüdeki daire, çizgi vb. gibi basit şekilleri algılamak için bir özellik çıkarma yöntemidir.

"Basit" bir şekil, yalnızca birkaç parametre ile temsil edilebilen bir şekildir. Örneğin, bir çizgi iki parametreyle 
(eğim, kesişme noktası) temsil edilebilir ve bir dairenin üç parametresi vardır (merkezin koordinatları ve yarıçap (x, y, r)).
Hough dönüşümü, bir görüntüde bu tür şekilleri bulmada mükemmel bir iş çıkarır.

Hough Transform kullanmanın temel avantajı, oklüzyona karşı duyarsız olmasıdır.

https://learnopencv.com/hough-transform-with-opencv-c-python/

'''
import cv2
import numpy as np


def onTrackbarChange(max_slider):
    cimg = np.copy(img)

    p1 = max_slider
    p2 = max_slider * 0.4

    # Çember tespiti için Hough Transform fonksiyonunu ekleyin.
    '''
    HoughCircles: (image, method, dp, minDist, circles=, param1=, param2=, minRadius=, maxRadius=)

    image: Girdi görüntü
    method: Detection yöntemi.
    dp: akümülatör çözünürlüğünün ve görüntü çözünürlüğünün ters oranı.
    minDist: tespit edilen daireler ile merkezler arasındaki minimum mesafe.
    param_1 and param_2: Bunlar metoda özel parametrelerdir.
    min_Radius : algılanacak dairenin minimum yarıçapı.
    max_Radius: algılanacak maksimum yarıçap.
    '''
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, cimg.shape[0]/64, param1=p1, param2=p2, minRadius=25, maxRadius=50)

    # Eğer en az bir çember tespit edilirse:
    
    if circles is not None:
        cir_len = circles.shape[1] # bulunan çemberlerin uzunlukları
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Bulunan çemberleri çizmek
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Bulunan çemberlerin merkezini çizmek
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    else:
        cir_len = 0 # Çember bulunamadı
    
    # Çıktı görüntüsünü görüntüleyin
    cv2.imshow('Result_Image', cimg)    

    # Edge image for debugging
    edges = cv2.Canny(gray, p1, p2)
    cv2.imshow('Edges', edges)

    

    
if __name__ == "__main__":

    image = cv2.imread('_images_must/brown_eyes.jpg')
    img = image.copy()

    # Girdi görüntüsünü gray-scale e dönüştürün

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Bir görüntüleme penceresi oluşturun
    cv2.namedWindow("Edges")
    cv2.namedWindow("Result_Image")
    

    # Giriş threshold value
    initThresh = 105 

	# Maximum threshold value
    maxThresh = 200 

    # Trackbar oluşturun
    cv2.createTrackbar("Threshold", "Result_Image", initThresh, maxThresh, onTrackbarChange)
    onTrackbarChange(initThresh)
    
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break

    cv2.destroyAllWindows()
