import numpy as np
import cv2
from matplotlib import pyplot as plt

def match(queryImgPath, targetImgPath):

    MIN_MATCH_COUNT = 10

    img1 = cv2.imread(targetImgPath, 0) # queryImage
    img2 = cv2.imread(queryImgPath, 0) # trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.9*n.distance:
            good.append(m)

    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    if len(good)>MIN_MATCH_COUNT:

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w, = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = matchesMask, # draw only inliers
                    flags = 2)

    # print("dst", dst)
    # print("dst_pts: ", dst_pts)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    newPath = queryImgPath.split(".")[0]
    cv2.imwrite(f"{newPath}_mapped.png", img3)

    plt.imshow(img2, 'gray')
    # plt.scatter(dst_pts[0], dst_pts[1], color='r', marker='x')
    # plt.savefig(f"{newPath}_good.png")

    return dst_pts[0]