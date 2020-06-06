from tensorflow import keras
from tensorflow_core.python.keras.engine.sequential import Sequential
from tensorflow_core.python.keras.layers.core import Flatten,Dense,Dropout
from tensorflow_core.python.keras.layers.convolutional import Conv2D
from tensorflow_core.python.keras.engine.input_layer import InputLayer
from tensorflow_core.python.keras.layers.pooling import MaxPool2D
from tensorflow_core.python.keras.layers.normalization import BatchNormalization

from tensorflow.keras.preprocessing.image import ImageDataGenerator

#from tensorflow_core.python.keras.preprocessing.image import ImageDataGenerator

# from tensorflow.keras import Sequential
# from tensorflow.keras.layers import Flatten,Dense,Dropout,InputLayer,BatchNormalization,Conv2D,MaxPool2D
import os
import cv2

modelpath="./model/00.h5"
id_path="./model"
classes = os.listdir(id_path)[1:]

if os.path.exists(modelpath)==False:

    #图片生成器
    datagen=ImageDataGenerator(rescale=1./255)
    img_width = 120
    img_height = 120
    batch_size = 10
    train_generator=datagen.flow_from_directory(directory=id_path,classes=classes,target_size=(img_width,img_height),
                                                batch_size=batch_size,color_mode="grayscale",class_mode="sparse")
    model = Sequential()
    model.add(InputLayer((120,120,1)))
    model.add(Conv2D(32,(3,3),padding="same",activation="relu",kernel_initializer="he_uniform"))
    model.add(Conv2D(64,3,padding="same",activation="relu"))
    model.add(Conv2D(128,3,padding="same",activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPool2D(2,2))
    model.add(Dropout(0.2))

    model.add(Conv2D(256,3,padding="same",activation="relu",kernel_initializer="he_uniform"))
    model.add(Conv2D(256,3,padding="same",activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPool2D(2,2))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(200,activation="relu"))
    model.add(Dropout(0.5))
    #model.add(Dense(1,activation="sigmoid"))
    model.add(Dense(len(classes),activation="softmax"))

    model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])
    history = model.fit_generator(train_generator,steps_per_epoch=len(train_generator),epochs=8,verbose=1)
    model.save(id_path+"./00.h5")
else:
    model = keras.models.load_model(modelpath)

def recognize(img):
    #img=cv2.imread(img)
    img=cv2.resize(img,(120,120))
    img=img.reshape(1,120,120,1)
    a=model.predict_classes(img,batch_size=1)
    #print(a)
    id_name=classes[a[0]]
    #print(id_name)
    return id_name
#recognize("./model/hzh/20200530-173239.jpg")