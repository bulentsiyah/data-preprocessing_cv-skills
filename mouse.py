'''
https://learnopencv.com/mouse-and-trackbar-in-opencv-gui/

'''
import cv2


# Sınırlayıcı kutu koordinatlarını saklamak için listeler oluşturulur.
top_left_corner=[]
bottom_right_corner=[]
 

# fare input unda çağrılacak işlev
def drawRectangle(action, x, y, flags, *userdata):
  # global variable lara referans verme 
  global top_left_corner, bottom_right_corner
  # Sol fare düğmesine basıldığında sol üst köşeyi işaretleyin
  if action == cv2.EVENT_LBUTTONDOWN:
    top_left_corner = [(x,y)]
    # Sol fare düğmesi bırakıldığında, sağ alt köşeyi işaretleyin
  elif action == cv2.EVENT_LBUTTONUP:
    bottom_right_corner = [(x,y)]   
    # Dikdörtgeni çiz
    cv2.rectangle(image, top_left_corner[0], bottom_right_corner[0], (0,255,0),2, 8)
    cv2.imshow("Window",image)
 

image = cv2.imread("_images_must/sample.jpg")
# girdi görüntüsünü kopyalıyoruz
temp = image.copy()
# Adlandırılmış bir pencere oluşturun
cv2.namedWindow("Window")


# fare olayları meydana geldiğinde çağrılan highgui fonksiyonu
'''
cv2.setMouseCallback(winname, onMouse, userdata)

- winname: Pencerenin adı
- onMouse: Fare olayları için geri arama işlevi
- userdata: Geri aramaya aktarılan isteğe bağlı bağımsız değişken
'''
cv2.setMouseCallback("Window", drawRectangle)
 

k=0
# q tuşuna basıldığında pencereyi kapatın
while k!=113:
  cv2.imshow("Window", image)
  k = cv2.waitKey(0)
  # c'ye basılırsa, kopyalanan görüntüyü kullanarak pencereyi temizleyin
  if (k == 99):
    image= temp.copy()
    cv2.imshow("Window", image)
 
cv2.destroyAllWindows()