import cv2
from face_recognize import recognize
def face_detect(img):
    # face_class = ["", "hzh", "wyc"]
    # 调用人脸识别特征分类器
    frontface_cascade = cv2.CascadeClassifier("./data/haarcascade_frontalface_alt2.xml")
    profileface_cascade = cv2.CascadeClassifier("./data/haarcascade_profileface.xml")
    #siverware_cascade = cv2.CascadeClassifier("./data/haarcascade_smile.xml")

    # frontface_cascade = cv2.CascadeClassifier("./data/lbpcascades/lbpcascade_frontalface_improved.xml")
    #profileface_cascade = cv2.CascadeClassifier("./data/lbpcascades/lbpcascade_profileface.xml")
    # siverware_cascade = cv2.CascadeClassifier("./data/lbpcascades/lbpcascade_silverware.xml")

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = cv2.equalizeHist(img)   # 直方图均衡化通过有效地扩展常用的亮度来实现这种功能,对于背景和前景都太亮或者太暗的图像非常有用

    front_face = frontface_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5,flags=cv2.CASCADE_SCALE_IMAGE)  # 返回人脸的list
    profile_face = profileface_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5,flags=cv2.CASCADE_SCALE_IMAGE)  # 返回侧脸的list

    # 检测人脸
    #print(front_face)
    if len(front_face) == 0:
        if len(profile_face)==0:
            cv2.putText(img,"no face",(200,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
            face_area = []
        else:
            for (x, y, w, h) in profile_face:
                face_area = img_gray[y:(y + h), x:(x + w)]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 3)
                cv2.putText(img,recognize(face_area),(x,y-30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),1,cv2.LINE_AA)
    else:
        for (x, y, w, h) in front_face:
            face_area = img_gray[y:(y + h), x:(x + w)]
            # 画矩形
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
            cv2.putText(img, recognize(face_area), (x, y-30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1, cv2.LINE_AA)
            #siverware = siverware_cascade.detectMultiScale(face_area, scaleFactor=1.2,minNeighbors=5)  # 返回smile的list
            # for (ex, ey, ew, eh) in siverware:
            #     # 将眼睛区域转成原图的绝对坐标
            #     cv2.rectangle(img, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)
    #cv2.imshow("img", img)
    return (img,face_area)
