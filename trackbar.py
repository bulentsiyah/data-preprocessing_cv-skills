"""

"""

import cv2


'''
scaleFactor: imajı ölçeklendirmek için tanımlayacağımız callback fonksiyonunda kullanılacaktır. 
maxScaleUp: izleme çubuğu konumunun kaydedeceği maksimum değerdir. Maksimum değer olarak 100'e 
sahip olmak en iyisidir, çünkü daha sonra bir şeyi yüzde olarak doğrudan ölçeklendirmek için 
izleme çubuğu konumunu kullanabiliriz.
'''
maxScaleUp = 100
scaleFactor = 1
windowName = "Resize Image"
trackbarValue = "Scale"
 

image = cv2.imread("_images_must/sample.jpg")
 
# Sonuçları görüntülemek için bir pencere oluşturun ve flag ı Otomatik Boyutlandır olarak ayarlayın
cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
 
# Callback fonksiyonu
def scaleImage(*args):
    # İzleme çubuğundan ölçek faktörünü alın
    scaleFactor = 1+ args[0]/100.0
    # Resmi yeniden boyutlandır
    scaledImage = cv2.resize(image, None, fx=scaleFactor, fy = scaleFactor, interpolation = cv2.INTER_LINEAR)
    cv2.imshow(windowName, scaledImage)
 
# Bir Trackbar oluşturun ve bir callback fonksiyonunu ilişkilendirin
'''
cv2.createTrackbar( trackbarName, windowName, value, count, onChange)

- trackbarname: Oluşturulan izleme çubuğunun adı.
- winname: Oluşturulan izleme çubuğunun üst penceresinin adı.
- value: Kaydırıcının varsayılan konumu. Bu isteğe bağlıdır.
- count: Kaydırıcının hangi değere kadar gideceği.
- onChange: Callback fonksiyonu.
'''
cv2.createTrackbar(trackbarValue, windowName, scaleFactor, maxScaleUp, scaleImage)
 

cv2.imshow(windowName, image)
c = cv2.waitKey(0)
cv2.destroyAllWindows()