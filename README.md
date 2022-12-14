# Multi-person pose estimation using AlphaPose and OpenPose
Pose estimation(PE) aims to identify the skeletal structure of humans in motion. Depending on the number of subjects, the problem can be either single- person PE or multi-person PE. Multi-person PE is a harder of the two tasks because of various problems like, number of subjects, subject overlapping, etc. There are mainly two approaches to solve this problem: Top Down and Bottom Up: 
|                                                                                                                                         Bottom Up                                                                                                                                        |                                                                                                                                    Top Down                                                                                                                                    |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| In this approach, we first detect all the keypoints(eyes, neck, joints, etc) in the frame, irrespective of the person. Then we proceed by finding the appropriate pairs among these keypoints such that the pair, when connected by a line, should represent a part of the same person. | In this approach, we start by identifying each person in the frame, using classic detection algorithms like YOLO. Then we proceed by finding the keypoints for each person detected, individually, and then we connect these keypoints to form the appropriate skeleton figure. |
| The Bottom-up approach works well when the frame contains few persons and that too, well separated from each other.                                                                                                                                                                     | The Top-down approach has been shown to be more effective when encountering situations like overlapping persons.                                                                                                                                                                |
| Example: OpenPose(CMU-Pose)                                                                                                                                                                                                                                                             | Example: AlphaPose                                                                                                                                                                                                                                                              |
| <img src='OpenPose.gif'>                                                                                                                                                                                                                                                                | <img src='AlphaPose.gif'>                                                                                                                                                                                                                                                       |



## Requirements
Install the required libraries:
```bash
 pip  install requirements.txt
```
Download the pretrained caffe model for OpenPose from [here](http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/mpi/pose_iter_160000.caffemodel) and place it in the [models](https://github.com/tanmay1024/Pose-Estimation/tree/main/models) directory.
## Inference
OpenPose:
```bash
 python 3.x openpose.py --video_dir path\to\video\file
```
AlphaPose:
```bash
 python 3.x alphapose_with_gluoncv.py --video_dir path\to\video\file
```
