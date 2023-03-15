
import cv2

class MotionDEt:

    def __init__(self):

        pass

    #thresholding
    def thresholding(self, image):
        ret0,th0 = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # global thresholding
        ret1,th1 = cv2.threshold(image,100,255,cv2.THRESH_BINARY)
        # Otsu's thresholding
        ret2,th2 = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(image,(5,5),0)
        ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return th1



    def hareketlikik(self,):

        cap = cv2.VideoCapture('_videos/02a8b666e30848c890d719c8c37ade9b.mp4')
        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        color = (0,255,0)

        frame1=cv2.resize(frame1, (612, 512))
        frame2=cv2.resize(frame2, (612, 512))

        while cap.isOpened():

                        

            '''# Optical flow hesaplamaları için ayarları belirleyin
            params = dict(winSize=(15, 15),
                        maxLevel=4,
                        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

            # Optical flow hesaplayın
            p1, st, err = cv2.calcOpticalFlowPyrLK(gray1, gray2, None, None, **params)

            # Hareketleri sabitleyin
            frame2_stable = cv2.remap(frame2, p1, None, cv2.INTER_LINEAR)

            # İki kareyi gösterin
            cv2.imshow('frame1', frame1)
            cv2.imshow('frame2', frame2)
            cv2.imshow('frame2_stable', frame2_stable)'''

            
            diff = cv2.absdiff(frame1, frame2)
            cv2.imshow("Diffrence",diff)
            
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            #blur = cv2.GaussianBlur(gray, (5,5), 0)
            #cv2.imshow("Blurred",blur)
            
            _,thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations = 3)
            
            contours,_ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #cv2.drawContours(frame1, contours, -1, color, 3)

            for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow("Feed",frame1)
            
            frame1 = frame2
            ret, frame2 = cap.read()

            frame2=cv2.resize(frame2, (612, 512))
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            
            if cv2.waitKey(30) & 0XFF == ord("q"):
                break
            
        cap.release()
        cv2.destroyAllWindows()
            


        # diff = cv2.absdiff(frame1, frame2)

        # cv2.imshow("frame1", frame1)
        # cv2.imshow("frame2", frame2)
        # cv2.imshow("diff", diff)


    def hareketlikik2(self,):
        # Video dosyasını aç
        cap = cv2.VideoCapture('_videos/02a8b666e30848c890d719c8c37ade9b.mp4')
        

        # Background Subtraction yöntemi için nesne oluştur
        fgbg = cv2.createBackgroundSubtractorMOG2()

        frame2 = None

        while True:
            # Bir kare yakala
            ret, frame = cap.read()
            
            if ret:
                frame=cv2.resize(frame, (612, 512))

                if frame2 is None:
                    frame2=cv2.resize(frame, (612, 512))

                frame = cv2.absdiff(frame, frame2)

                # Kareyi griye dönüştür
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Background Subtraction yöntemi ile hareketli nesneleri tespit et
                fgmask = fgbg.apply(gray)
                
                # Hareketli nesnelerin çevresine dikdörtgen çiz
                contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Kareyi göster
                cv2.imshow('frame', frame)
                
                # 'q' tuşuna basıldığında döngüyü sonlandır
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                frame2=cv2.resize(frame, (612, 512))
            else:
                break

        # Kaynakları serbest bırak
        cap.release()
        cv2.destroyAllWindows()


    def hreketlikik3(self,):
        cap = cv2.VideoCapture('_videos/02a8b666e30848c890d719c8c37ade9b.mp4')
        

        # Background subtractor
        backSub = cv2.createBackgroundSubtractorMOG2()
        frame2 = None
        while True:
            # Read frame from video
            ret, frame = cap.read()
            
            if not ret:
                break

            if frame2 is None:
                frame2=cv2.resize(frame, (612, 512))


            frame=cv2.resize(frame, (612, 512))

            #frame = cv2.absdiff(frame, frame2)
            
            # Apply background subtraction
            fgMask = backSub.apply(frame)
            
            # Apply morphology operations to remove noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
            
            # Find contours of moving objects
            contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Draw bounding boxes around moving objects
            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Show the resulting frame
            cv2.imshow('Frame', frame)
            
            # Press 'q' to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            frame2=cv2.resize(frame, (612, 512))

        # Release the video capture and destroy all windows
        cap.release()
        cv2.destroyAllWindows()


    def hreketlikik4(self,):

        cap = cv2.VideoCapture('_videos/02a8b666e30848c890d719c8c37ade9b.mp4')
        
        ret, prev_frame = cap.read()

        prev_frame=cv2.resize(prev_frame, (612, 512))

        prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        while True:
            ret, curr_frame = cap.read()

            if not ret:
                break

            curr_frame=cv2.resize(curr_frame, (612, 512))
            
            curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            
            flow = cv2.calcOpticalFlowFarneback(prev_frame_gray, curr_frame_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            
            curr_frame_stabilized = curr_frame.copy()
            for y in range(0, curr_frame.shape[0], 5):
                for x in range(0, curr_frame.shape[1], 5):
                    dx, dy = flow[y, x]
                    if abs(dx) > 1 or abs(dy) > 1:
                        curr_frame_stabilized[y, x] = [0, 0, 0]
            
            cv2.imshow('stabilized', curr_frame_stabilized)
            
            if cv2.waitKey(1) == ord('q'):
                break
            
            prev_frame_gray = curr_frame_gray
            
        cap.release()
        cv2.destroyAllWindows()

            



if __name__ == '__main__':
    m = MotionDEt()
    m.hareketlikik()
    #m.hareketlikik2()
    #m.hreketlikik3()
    #m.hreketlikik4()










