"""
VISION SCRIPT
uses ml to process camera data
"""

from utilities.classes import TargetObj, TargetPos

# def get_obj_label(targetObj):
#     assert isinstance(targetObj, TargetObj), "targetObj must be of type TargetObj"
#     objLabel = "unknown"
#     # implement object labeling here
#     return objLabel

# def get_rel_pos(targetObj):
#     assert isinstance(targetObj, TargetObj), "targetObj must be of type TargetObj"
#     # map targetObj.imgData and targetObj.objLabel onto depth camera map to determine targetObj.relPos
#     targetRelPos = TargetPos(x=0, y=0, z=0)
#     return targetRelPos

import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from utilities import sift
from collections import defaultdict
import os
import matplotlib.pyplot as plt

def rectContains(rect,pt):
    logic = rect[0] < pt[0] and pt[0] < rect[2] and rect[1] < pt[1] and pt[1] < rect[3]
    return logic

def detect_objects(imgPath, model="yolov3", confidence=0.1):
    print("Detecting objects in image: ", imgPath)
    img = cv2.imread(imgPath)
    imgHeight, imgWidth = img.shape[:2]
    bboxes, label, conf = cv.detect_common_objects(img, confidence=confidence, model=model)
    for l, c in zip(label, conf):
        print(f"Detected object: {l} with confidence level of {c}\n")
    output_image = draw_bbox(img, bboxes, label, conf)
    cv2.imwrite(f'{imgPath.split(".")[0]}_boxed.png', output_image)
    return bboxes, (imgHeight, imgWidth)

def find_target_bbox(imgDimensions, bboxes, eyeData):
    height = imgDimensions[0]
    width = imgDimensions[1]
    eyeGaze = (eyeData['gp'][0]*width, eyeData['gp'][1]*height)

    bbox_matches = []
    for bbox in bboxes:
        if eyeGaze[0] > bbox[0] and eyeGaze[0] < bbox[0]+bbox[2] and eyeGaze[1] > bbox[1] and eyeGaze[1] < bbox[1]+bbox[3]:
            bbox_matches.append(bbox)
    if len(bbox_matches) == 0:
        raise Exception("No bbox found for eye gaze")
    # elif len(bbox_matches) > 1:
    #     raise Exception("Multiple bboxes found for eye gaze")
    else:
        return bbox_matches[0]

def crop_image(imgPath, bbox):
    print("Cropping image: ", imgPath, "using bbox: ", bbox)
    img = cv2.imread(imgPath)
    cropped_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    croppedImgPath = f'{imgPath.split(".")[0]}_cropped.png'
    cv2.imwrite(croppedImgPath, cropped_img)
    return croppedImgPath

def find_query_target(queryImgPath, targetImgPath):
    print("Finding query target: ", queryImgPath)
    queryBboxes, _ = detect_objects(queryImgPath)
    # points = [(pt[0], pt[1]) for pt in sift.match(queryImgPath, targetImgPath)]
    points = sift.match(queryImgPath, targetImgPath)
    # check which bbox contains the most points
    
    max_index = 0
    max_numpoints = 0
    print("QUERY: ", queryBboxes)
    for index, bbox in enumerate(queryBboxes):
        print("bbox", bbox)
        num_points = 0
        for point in points:
            print("point: ", point)
            if rectContains(bbox, point):
                num_points += 1
        print("Rect: ", bbox)
        print("num_points: ", num_points)
        if num_points > max_numpoints:
            max_numpoints = num_points
            max_index = index
            print("new max at index: ", index)
    # print("max_index: ", max_index)
    queryTargetBbox = queryBboxes[max_index]
        
    # max_index = max(num_points, key=num_points.get)
    # queryTargetBbox = targetBboxes[max_index]
    
    print("QUERY TARGET BBOX: ", queryTargetBbox)
    return queryTargetBbox

def find_center(bbox):
    print("Finding center of bbox: ", bbox)
    x = (bbox[1] + bbox[3])/2
    y = (bbox[0] + bbox[2])/2
    return (x, y)

def run_vision(queryImgPath, targetImgPath, eyeData):
    print("========================")
    print("Running vision on query: ", queryImgPath)
    targetBboxes, imgDimensions = detect_objects(targetImgPath)
    targetBbox = find_target_bbox(imgDimensions, targetBboxes, eyeData)
    croppedImgPath = crop_image(targetImgPath, targetBbox)
    queryTargetBbox = find_query_target(queryImgPath, croppedImgPath)
    queryTargetCenter = find_center(queryTargetBbox)
    img = cv2.imread(queryImgPath)
    plt.imshow(img, cmap=plt.cm.gray, interpolation='nearest')
    plt.plot(queryTargetCenter[1], queryTargetCenter[0], 'o')
    plt.savefig(f'{queryImgPath.split(".")[0]}_result.png')

    print("TARGET CENTER: ", queryTargetCenter)


# for imgFolder in os.listdir("data"):
#     imgFolderPath = f"data/{imgFolder}"
#     if os.path.isdir(imgFolderPath):
#         run_vision(f"{imgFolderPath}/query.png", f"{imgFolderPath}/target.png", (500,500))
#     else:
#         print(f"{imgFolderPath} is not a directory")