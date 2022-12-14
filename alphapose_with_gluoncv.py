# AlphaPose implemented using pretrained models

import argparse
from __future__ import absolute_import, division
# from decord import VideoReader
from IPython.display import clear_output
import cv2
from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
from gluoncv.data.transforms.pose import detector_to_alpha_pose, heatmap_to_coord_alpha_pose
import numpy as np
import mxnet as mx
import random
#from ..filesystem import try_import_cv2

"""Function for plotting the keypoints """

parser = argparse.ArgumentParser()
parser.add_argument("--video_dir", type=str, required=True, help='path to video file')
args = parser.parse_args()

video = args.video_dir

def cv_plot_keypoints(img, coords, confidence, class_ids, bboxes, scores,
                      box_thresh=0.5, keypoint_thresh=0.2, scale=1.0, **kwargs):
    

    if isinstance(img, mx.nd.NDArray):
        img = img.asnumpy()
    if isinstance(coords, mx.nd.NDArray):
        coords = coords.asnumpy()
    if isinstance(class_ids, mx.nd.NDArray):
        class_ids = class_ids.asnumpy()
    if isinstance(bboxes, mx.nd.NDArray):
        bboxes = bboxes.asnumpy()
    if isinstance(scores, mx.nd.NDArray):
        scores = scores.asnumpy()
    if isinstance(confidence, mx.nd.NDArray):
        confidence = confidence.asnumpy()

    joint_visible = confidence[:, :, 0] > keypoint_thresh
    joint_pairs = [[0, 1], [1, 3], [0, 2], [2, 4],
                   [5, 6], [5, 7], [7, 9], [6, 8], [8, 10],
                   [5, 11], [6, 12], [11, 12],
                   [11, 13], [12, 14], [13, 15], [14, 16]]

    person_ind = class_ids[0] == 0

    colormap_index = np.linspace(0, 1, len(joint_pairs))
    coords *= scale
    for i in range(coords.shape[0]):
        pts = coords[i]
        for cm_ind, jp in zip(colormap_index, joint_pairs):
            if joint_visible[i, jp[0]] and joint_visible[i, jp[1]]:
                cm_color = tuple([int(x * 255) for x in plt.cm.cool(cm_ind)[:3]])
                pt1 = (int(pts[jp, 0][0]), int(pts[jp, 1][0]))
                pt2 = (int(pts[jp, 0][1]), int(pts[jp, 1][1]))
                cv2.line(img, pt1, pt2, cm_color, 2)
    return img

"""Loading the pre-trained model"""

detector = model_zoo.get_model('yolo3_mobilenet1.0_coco', pretrained=True)
pose_net = model_zoo.get_model('alpha_pose_resnet101_v1b_coco', pretrained=True)

# I reset the classes of the detector to only include
# human, so that the NMS process is faster.

detector.reset_class(["person"], reuse_weights=['person'])

"""Extracting Information of the given video"""

cap = cv2.VideoCapture(video)
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

"""Processing the video frame-by-frame"""

i = 1 
out = cv2.VideoWriter('output_AlphaPose.avi', fourcc, fps, (frameWidth, frameHeight))
success,image = cap.read()
while(success):
    cv2.imwrite(r'frames/frame%d.png' % i, image) # Writing each frame to a file 
    clear_output(wait=True)
    print("Frame Number: %d/%d" %(i, length))
    x, img = data.transforms.presets.yolo.load_test((r'frames/frame%d.png' % i), short=400) # Finding humans in the frame using YOLO
    success,image = cap.read()
    i += 1
    class_IDs, scores, bounding_boxs = detector(x) 
    pose_input, upscale_bbox = detector_to_alpha_pose(img, class_IDs, scores, bounding_boxs)
    predicted_heatmap = pose_net(pose_input)
    pred_coords, confidence = heatmap_to_coord_alpha_pose(predicted_heatmap, upscale_bbox)
    ax = cv_plot_keypoints(img, pred_coords, confidence,
                              class_IDs, bounding_boxs, scores,
                              box_thresh=0.5, keypoint_thresh=0.2)
    canvas = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    canvas = cv2.resize(canvas,(frameWidth, frameHeight), interpolation= cv2.INTER_LINEAR)
    out.write(canvas)
    #cv2.imshow("frame", canvas)
    
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()

