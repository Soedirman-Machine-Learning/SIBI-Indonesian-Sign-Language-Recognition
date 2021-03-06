import cv2
import numpy as np
import time
# import re

#Mengambil YOLO
net = cv2.dnn.readNetFromDarknet("yolov4-tiny-custom.cfg",r"yolov4-tiny-custom_best.weights")

classes = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Terima Kasih','Makan','Tolong','Hello','I Love You','Ke','Mau','Saya','Nama','Salam','_','Del']
label = " "
kata = ""
DelCounter = 0
LastLabel = ""

cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc(*"MJPG")
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# VideoWriter = cv2.VideoWriter(r'C:\python2\flask_bootstraps\video\hasil_realtime5.avi', fourcc, 20,(680,480) )

timeframe = time.time()
frame_id = 0

waktu = int(round(time.time() * 1000))
waktu_sebelum = int(round(time.time() * 1000))

while 1:
    waktu = int(round(time.time() * 1000))
    _, img = cap.read()
    frame_id += 1
    img = cv2.resize(img,(680,480))
    hight,width,_ = img.shape

#Mendeteksi Objek
    blob = cv2.dnn.blobFromImage(img, 1/255,(416,416),(0,0,0),swapRB = True,crop= False)
    net.setInput(blob)
    output_layers_name = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_name)

#Menampilkan Informasi pada screen 
    boxes =[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3]* hight)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)


    indexes = cv2.dnn.NMSBoxes(boxes,confidences,.5,.4)

    boxes =[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3]* hight)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,.8,.4)
    # Non-maximum suppression:
    results = [(class_ids[i], boxes[i]) for i in range(len(boxes)) if i in indexes]
    
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0,255,size =(len(boxes),3))
    # if  len(indexes)>0:
    #     for i in indexes.flatten(): 
    #         x,y,w,h = boxes[i]
    #         label = str(classes[class_ids[i]])
    #         confidence = str(round(confidences[i],2))
    #         color = colors[i]
    #         cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
    #         cv2.putText(img,label + " " + confidence, (x,y+100),font,2,color,2)

    # elapsed_time = time.time() - timeframe
    # fps = frame_id / elapsed_time
    # cv2.putText(img, str(round(fps,2)), (10,50), font, 2, (255, 255, 255), 2) #FPS value
    # cv2.putText(img, "FPS", (220,50), font, 2, (255, 255, 255), 2) #FPS Label
    if  len(indexes)>0:
        for i in indexes.flatten():
                    x,y,w,h = boxes[i]
                    label = str(classes[class_ids[i]])
                    if ((waktu-waktu_sebelum) > 3000 and kata != " "):
                        if (label == "Del" and DelCounter >= 1):
                            kata = ""
                            DelCounter = 0
                            # kata = kata[:-1]
                        elif (label == "Del" and kata != ""):
                            l = len(kata)
                            kata = kata[:l-1]
                            if (LastLabel == "Del"):
                                DelCounter = DelCounter + 1
                            elif (LastLabel != "Del"):
                                DelCounter = 0
                        elif (label == "_"):
                            kata = kata + " "
                        else: 
                            kata = kata + label
                        LastLabel = label
                        print(kata)
                        waktu_sebelum = waktu
                    confidence = str(round(confidences[i],2))
                    color = colors[i]
                    cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
                    cv2.putText(img,label + " " + confidence, (x,y+100),font,2,color,2)
    cv2.putText(
            img,
            kata,
            (10,50),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255,0,0),
            2
        )

    # VideoWriter.write(img)
    cv2.imshow('COBA',img)
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()