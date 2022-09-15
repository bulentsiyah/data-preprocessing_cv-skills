import gradio as gr
from PIL import Image
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Conv2DTranspose, Concatenate, Input
from tensorflow.keras.layers import AveragePooling2D, GlobalAveragePooling2D, UpSampling2D, Reshape, Dense, Dropout, concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet_v2 import ResNet101V2
from tensorflow.keras.utils import to_categorical   
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator
print(f"GPU AVAILABLE: {tf.test.is_gpu_available()}")

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from os import listdir
from os.path import isfile, join

from sklearn.model_selection import train_test_split
from skimage import io
import random
from skimage import transform
from tqdm import tqdm

import numpy as np
import time
from matplotlib import pyplot as plt
import cv2
import os
cwd = os.getcwd()

rgb_representations = np.array([(0,0,0), (128,64,128),(130,76,0),(0,102,0), (112,103,87),(28,42,168),(48,41,30), (0,50,89), (107,142,35),(70,70,70), (102,102,156),(254,228,12),
                      (254,148,12), (190,153,153),(153,153,153), (255,22,96), (102,51,0), (9,143,150), (119,11,32), (51,51,0), (190,250,190), (112,150,146), 
                       (2,135,115), (255,0,0)], np.uint8)

classes = ['unlabeled', 'paved-area', 'dirt', 'grass', 'gravel', 'water', 'rocks', 'pool', 'vegetation', 'roof', 'wall', 'window', 'door', 'fence', 
           'fence-pole', 'person', 'dog', 'car', 'bicycle', 'tree', 'bald-tree', 'ar-marker', 'obstacle', 'conflicting']

@tf.function
def dice_loss(y_true, y_pred):
    numerator = tf.reduce_sum(y_true * y_pred)
    denominator = tf.reduce_sum(y_true * y_true) + tf.reduce_sum(y_pred * y_pred) - tf.reduce_sum(y_true * y_pred)

    return 1 - numerator / denominator

class MyMeanIOU(tf.keras.metrics.MeanIoU):
    def update_state(self, y_true, y_pred, sample_weight=None):
        return super().update_state(tf.argmax(y_true, axis=-1), tf.argmax(y_pred, axis=-1), sample_weight)


def deeplab_plus(input_size = (512,512, 3), n_classes = 24,threshold = 0.5):
    def SqueezeAndExcite(inputs, ratio=8):
        init = inputs
        filters = init.shape[-1]
        se_shape = (1, 1, filters)

        se = GlobalAveragePooling2D()(init)
        se = Reshape(se_shape)(se)
        se = Dense(filters // ratio, activation='relu', kernel_initializer='he_normal', use_bias=False)(se)
        se = Dense(filters, activation='sigmoid', kernel_initializer='he_normal', use_bias=False)(se)
        x = init * se
        return x

    def ASPP(inputs):
        """ Image Pooling """
        shape = inputs.shape
        y1 = AveragePooling2D(pool_size=(shape[1], shape[2]))(inputs)
        y1 = Conv2D(256, 1, padding="same", use_bias=False)(y1)
        y1 = BatchNormalization()(y1)
        y1 = Activation("relu")(y1)
        y1 = UpSampling2D((shape[1], shape[2]), interpolation="bilinear")(y1)

        """ 1x1 conv """
        y2 = Conv2D(256, 1, padding="same", use_bias=False)(inputs)
        y2 = BatchNormalization()(y2)
        y2 = Activation("relu")(y2)

        """ 3x3 conv rate=6 """
        y3 = Conv2D(256, 3, padding="same", use_bias=False, dilation_rate=6)(inputs)
        y3 = BatchNormalization()(y3)
        y3 = Activation("relu")(y3)

        """ 3x3 conv rate=12 """
        y4 = Conv2D(256, 3, padding="same", use_bias=False, dilation_rate=12)(inputs)
        y4 = BatchNormalization()(y4)
        y4 = Activation("relu")(y4)

        """ 3x3 conv rate=18 """
        y5 = Conv2D(256, 3, padding="same", use_bias=False, dilation_rate=18)(inputs)
        y5 = BatchNormalization()(y5)
        y5 = Activation("relu")(y5)

        y = Concatenate()([y1, y2, y3, y4, y5])
        y = Conv2D(256, 1, padding="same", use_bias=False)(y)
        y = BatchNormalization()(y)
        y = Activation("relu")(y)

        return y
        
    
    """ Input """
    inputs = Input(input_size)

    """ Encoder """
    encoder = ResNet50(weights="imagenet", include_top=False, input_tensor=inputs)

    image_features = encoder.get_layer("conv4_block6_out").output
    x_a = ASPP(image_features)
    x_a = UpSampling2D((4, 4), interpolation="bilinear")(x_a)

    x_b = encoder.get_layer("conv2_block2_out").output
    x_b = Conv2D(filters=48, kernel_size=1, padding='same', use_bias=False)(x_b)
    x_b = BatchNormalization()(x_b)
    x_b = Activation('relu')(x_b)

    x = Concatenate()([x_a, x_b])
    x = SqueezeAndExcite(x)

    x = Conv2D(filters=256, kernel_size=3, padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv2D(filters=256, kernel_size=3, padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = SqueezeAndExcite(x)

    x = UpSampling2D((4, 4), interpolation="bilinear")(x)
    x = Conv2D(n_classes, 1, activation = "softmax")(x)

    model = Model(inputs, x)
    model.compile(optimizer = Adam(lr = 5e-4), loss = dice_loss,
                  metrics = [MyMeanIOU(num_classes = n_classes, name = 'my_mean_iou')])
    return model

model = deeplab_plus()

path_saved_model = cwd + "/model_representation/segmentation/saved_model/"
model.load_weights(path_saved_model+'best_deeplab.h5')

def decode_segmentation_masks(mask, colormap, n_classes):
    r = np.zeros_like(mask).astype(np.uint8)
    g = np.zeros_like(mask).astype(np.uint8)
    b = np.zeros_like(mask).astype(np.uint8)
    for l in range(0, n_classes):
        idx = mask == l
        r[idx] = colormap[l, 0]
        g[idx] = colormap[l, 1]
        b[idx] = colormap[l, 2]
    rgb = np.stack([r, g, b], axis=2)
    return rgb

def segmentation(input_image):
    IMAGE_SIZE = 512

    W = IMAGE_SIZE
    H = IMAGE_SIZE

    #print(" bb : "+type(input_image))
    """ Reading the image """
    #image = cv2.imread(input_image, cv2.IMREAD_COLOR)
    image = input_image
    h, w, _ = image.shape
    x = cv2.resize(image, (W, H))
    x = x/255.0
    x = x.astype(np.float32)
    x = np.expand_dims(x, axis=0)


    """ Prediction """
    y = model.predict(x)[0]
    #y = cv2.resize(y, (w, h))
    y = np.expand_dims(y, axis=-1)
    out = y

    out = np.squeeze(out)
    prediction_mask = np.argmax(out, axis=2)

    prediction_colormap = decode_segmentation_masks(prediction_mask, rgb_representations, len(classes))

    return prediction_colormap

def showing_image(input_image,out):
    fig, axs = plt.subplots(1, 2, figsize=(20, 20), constrained_layout=True)

    img_orig = Image.open(input_image)
    axs[0].imshow(img_orig)
    axs[0].set_title('original image')
    axs[0].grid(False)

    axs[1].imshow(out)
    axs[1].set_title('prediction image-out.png')
    axs[1].grid(False)

    plt.show()



#file="001"
#input_image = org_dir+file+".jpg"
#out= segmentation(input_image)
#showing_image(input_image,out)

title = "Aerial Segmentation"
description = "deeplab"
article = " "
inputs = gr.inputs.Image()
outputs = gr.outputs.Image(type="pil", label="Output Image")

path_folder = cwd + "/model_representation/segmentation/datasets/"
examples = [[path_folder+'001.jpg'], [path_folder+'002.jpg'],[path_folder+'003.jpg']]
gr.Interface(segmentation, inputs, outputs, title=title, description=description, article=article, examples=examples, analytics_enabled=False).launch(
    debug=True)

'''


git init
git config user.name bulentsiyah
git config user.email bulentsiyahmb@gmail.com
git add *
git commit -m "WriteCommit"
git push origin master


'''