import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

#Parses Arguments and returns Path to Image
def parse_args():
    if len(sys.argv) < 2:
        raise ValueError('No Arguments Provided!\nMethod of Use:\npython3 [script] -f [path to file]')
    elif '-f' not in sys.argv:
        raise ValueError('-f flag not found!')
    else:
        return sys.argv[2]

def load_images(templatepath, imgpath):
    img1 = cv2.imread(templatepath, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
    return img1, img2

def load_video(templatepath, videopath):
    cap = cv2.VideoCapture(videopath)
    img1 = cv2.imread(templatepath, cv2.IMREAD_GRAYSCALE)
    _, img2 = cap.read()
    return cap, (img1, img2)

def load_files(templatepath, filepath):
    extension = filepath.split('.')[-1]
    if extension.lower() == 'mp4':
        return load_video(templatepath, filepath)
    else:
        return None, (load_images(templatepath, filepath))

def apply_SIFT(img1, img2):
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    src_pts = []
    dst_pts = []
    for m in good:
        src_pts.append(kp1[m[0].queryIdx].pt)
        dst_pts.append(kp2[m[0].trainIdx].pt)
    src_pts = np.array(src_pts)
    dst_pts = np.array(dst_pts)
    return src_pts, dst_pts

def get_corners(img1, src_pts, dst_pts):
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    h, w = img1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    return dst

def test_corners(imgpath, dst):
    img3 = cv2.imread(imgpath)

    image = cv2.circle(img3, (dst[0][0][0], dst[0][0][1]), radius=25, color=(255, 0, 0), thickness=-1)
    image = cv2.circle(img3, (dst[1][0][0], dst[1][0][1]), radius=25, color=(0, 255, 0), thickness=-1)
    image = cv2.circle(img3, (dst[2][0][0], dst[2][0][1]), radius=25, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(img3, (dst[3][0][0], dst[3][0][1]), radius=25, color=(255, 255, 255), thickness=-1)
    plt.imshow(image)
    plt.show()

def change_perspective(dst, video_cap, img1, img2, movieout_filename):
    orig = np.array([[0, 0], [img1.shape[0], 0], [img1.shape[0], img1.shape[1]], [0, img1.shape[1]]]).astype(np.float32)
    dst = dst.ravel().reshape(4, 2)
    M = cv2.getPerspectiveTransform(dst, orig)
    image = cv2.warpPerspective(img2, M, (img1.shape[0], img1.shape[1]))
    image = image.transpose()

    if video_cap is None:
        plt.imshow(image)
        plt.show()

    else:
        out = cv2.VideoWriter(movieout_filename, cv2.VideoWriter_fourcc(*'MP4V'), 15, (img1.shape[1], img1.shape[0]))
        out.write(image)
        has_frame, image = video_cap.read()
        i = 0
        while has_frame:
            image = cv2.warpPerspective(image, M, (img1.shape[0], img1.shape[1]))
            image = image.transpose((1, 0, 2))
            out.write(image)
            has_frame, image = video_cap.read()
        out.release()

'''
def main():
    filepath = parse_args()
    video_cap, (img1, img2) = load_files(filepath)
    src_pts, dst_pts = apply_SIFT(img1, img2)
    dst = get_corners(img1, src_pts, dst_pts)
    change_perspective(dst, video_cap, img1, img2)

if __name__ == '__main__':
    main()
'''

def part1(templname, moviein_filename, movieout_filename): 
    video_cap, (img1, img2) = load_files(templname, moviein_filename)
    src_pts, dst_pts = apply_SIFT(img1, img2)
    dst = get_corners(img1, src_pts, dst_pts)
    change_perspective(dst, video_cap, img1, img2, movieout_filename)
