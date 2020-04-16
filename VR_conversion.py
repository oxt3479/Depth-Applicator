# COPYWRITE OWEN THOMPSON
import numpy as np
import os
import cv2

class VR_scene:
    def __init__(self):
        self.frame = np.zeros(shape=(2880,1440))
        self.movies = os.listdir('./movie')
        self.depths = os.listdir('./depth')
        self.movies.sort()
        self.depths.sort()

    def make_dispirate_pair(self, rgbIMG, disparity, HW, baseline=10):
        '''
        Input: rgbIMG = np array H x W x 3 for Color IMG
        disparity = np array H x W for disparity indeces
        HW = (heigh, width) of input image.
        baseline = scalar to attenuate disparity to how you perfer, ~10 generally works.
        returns: left, right images with complimentary disparity.
        '''
        disparity -= int(255/2) # 0 corresponds to no disparity now.
        H = HW[0]
        W = HW[1]
	
        to_W = np.linspace(0, W-1, W).astype(np.int)
        to_H = np.linspace(0, H-1, H).astype(np.int)
        Ys = np.zeros(shape=(H,W)).astype(np.int)
        Xs = np.zeros(shape=(H,W)).astype(np.int)
        for i in range(0, W):
           Ys[:,i] = to_H
        for i in range(0, H):
           Xs[i,:] = to_W

        Xs_L = Xs - disparity//baseline
        Xs_R = Xs + disparity//baseline
        Xs_L = np.clip(Xs_L, 0, W-1)
        Xs_R = np.clip(Xs_R, 0, W-1)
        left = rgbIMG[Ys,Xs_L,:]
        right = rgbIMG[Ys,Xs_R,:]
        return left, right

def main():
    HW = (256, 640)
    new_scene = VR_scene()
    L_video = cv2.VideoWriter('left.avi',cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,256))
    R_video = cv2.VideoWriter('right.avi',cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,256))
    for i, movie in enumerate(new_scene.movies):
        rgbIMG = cv2.imread(f'movie/{movie}',1) # (H, W, 3)
        disparity = cv2.imread(f'depth/{new_scene.depths[i]}',0).astype(np.int) # (H, W), NO UNSIG
        left, right = new_scene.make_dispirate_pair(rgbIMG, disparity, HW)
        L_video.write(left)
        R_video.write(right)
    L_video.release()
    R_video.release()

if __name__ == "__main__": main()

