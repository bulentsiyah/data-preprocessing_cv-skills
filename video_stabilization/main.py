'''
https://joseywallace.github.io/blog/image-stabilization/


'''

import cv2
import numpy as np
import imageio
import matplotlib.pyplot as plt
from scipy import signal
from scipy.ndimage import convolve
from stabilize import *
import os
import sys

#load the images and create a plot of the trajectory
OUT_PATH = './_outputs/video_stabilization_result_drone/'
imgs, name = load_images('_videos/video_stabilization_2.mp4', OUT_PATH=OUT_PATH), 'video_stabilization_result_drone'

if os.path.exists(OUT_PATH)==False:
    os.mkdir(OUT_PATH)

#imgs = load_images('./run1.mp4', OUT_PATH='./frames_result2/'), 'result2'
#imgs = load_images('./run2.mp4', OUT_PATH='./frames_result3/'), 'result3'
ws = create_warp_stack(imgs)

i,j = 0,2
plt.scatter(np.arange(len(ws)), ws[:,i,j], label='X Velocity')
plt.plot(np.arange(len(ws)), ws[:,i,j])
plt.scatter(np.arange(len(ws)), np.cumsum(ws[:,i,j], axis=0), label='X Trajectory')
plt.plot(np.arange(len(ws)), np.cumsum(ws[:,i,j], axis=0))
plt.legend()
plt.xlabel('Frame')
plt.savefig('./_outputs/'+name+'_trajectory.png')

#calculate the smoothed trajectory and output the zeroed images
smoothed_warp, smoothed_trajectory, original_trajectory = moving_average(ws, sigma_mat= np.array([[1000,15, 10],[15,1000, 10]]))
new_imgs = apply_warping_fullview(images=imgs, warp_stack=ws-smoothed_warp, PATH='./out/')

#plot the original and smoothed trajectory
f, (a0, a1) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[1, 1]})

i,j = 0,2
a0.scatter(np.arange(len(original_trajectory)), np.array(original_trajectory)[:,i,j], label='Original')
a0.plot(np.arange(len(original_trajectory)), np.array(original_trajectory)[:,i,j])
a0.scatter(np.arange(len(smoothed_trajectory)), np.array(smoothed_trajectory)[:,i,j], label='Smoothed')
a0.plot(np.arange(len(smoothed_trajectory)), np.array(smoothed_trajectory)[:,i,j])
a0.legend()
a0.set_ylabel('X trajectory')
a0.xaxis.set_ticklabels([])

i,j = 0,1
a1.scatter(np.arange(len(original_trajectory)), np.array(original_trajectory)[:,i,j], label='Original')
a1.plot(np.arange(len(original_trajectory)), np.array(original_trajectory)[:,i,j])
a1.scatter(np.arange(len(smoothed_trajectory)), np.array(smoothed_trajectory)[:,i,j], label='Smoothed')
a1.plot(np.arange(len(smoothed_trajectory)), np.array(smoothed_trajectory)[:,i,j])
a1.legend()
a1.set_xlabel('Frame')
a1.set_ylabel('Sin(Theta) trajectory')
plt.savefig('./_outputs/'+name+'_smoothed.png')

#create a images that show both the trajectory and video frames
filenames = imshow_with_trajectory(images=new_imgs, warp_stack=ws-smoothed_warp, PATH='./_outputs/'+name+'/', ij=(0,2))

#create gif
create_gif(filenames, './_outputs/'+name+'.gif')
