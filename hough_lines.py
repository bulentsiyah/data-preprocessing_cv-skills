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
	global img
	global dst
	global gray

	dst = np.copy(img)

	th1 = max_slider 
	th2 = th1 * 0.4
	edges = cv2.Canny(img, th1, th2)

    # Çizgi tespiti için Hough Transform fonksiyonunu ekleyin.
	'''
    HoughLinesP: (image, rho, theta, threshold, lines=, minLineLength=, maxLineGap=)

	image: Girdi görüntü
    rho: Çözünürlük parametresi, piksel cinsinden.
    theta: Parametrenin çözünürlüğü radyan cinsinden.
    threshold: Bir çizgiyi algılamak için minimum kesişen nokta sayısı.
    lines: Çizginin başlangıç ve bitiş koordinatlarını saklayan bir vektör.
    '''
	lines = cv2.HoughLinesP(edges, 2, np.pi/180.0, 50, minLineLength=10, maxLineGap=100)

	# Tespit edilen çizgileri çizdirin.
	for line in lines:
		x1, y1, x2, y2 = line[0]
		cv2.line(dst, (x1, y1), (x2, y2), (0,0,255), 1)

	cv2.imshow("Result Image", dst)	
	cv2.imshow("Edges",edges)
    

if __name__ == "__main__":
	
	img = cv2.imread('_images_must/lanes.jpg')

	# Girdi görüntüsünü kopyalayın
	dst = np.copy(img)

	# Girdi görüntüsünü gray-scale e dönüştürün
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Bir görüntüleme penceresi oluşturun
	cv2.namedWindow("Edges")
	cv2.namedWindow("Result Image")
	  


	# Giriş threshold value
	initThresh = 500

	# Maximum threshold value
	maxThresh = 1000

    # Trackbar oluşturun
	cv2.createTrackbar("threshold", "Result Image", initThresh, maxThresh, onTrackbarChange)
	onTrackbarChange(initThresh)

	while True:
		key = cv2.waitKey(1)
		if key == 27:
			break

	cv2.destroyAllWindows()