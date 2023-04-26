"""
This script performs analysis on the video data of a continuum robot moving.

INPUT
Each video data clip captures the robot moving from one position to another through a single servo change.
The robot has 3 servos, and the combinations of servo angles are as follows:
Servo 1: 60 - 180, 30 degree increments
Servo 2: 0 - 240, 30 degree increments
Servo 3: 0 - 240, 30 degree increments
The video data files are labeled f"movement_seg1_{j}_seg2_{i}_seg3_{k}.avi", where i, j, and k are the end servo angles.

OUTPUT
The output of this script is:
1. A csv file containing the following data columns:
-Video Filename
-Frame (first or last)
-Servo1 Angle
-Servo2 Angle
-Servo3 Angle
-Joint1 Position
-Joint2 Position
-Joint3 Position
-EndEffector Position
-Seg1 Curvature
-Seg2 Curvature
-Seg3 Curvature
-End Curvature
2. Video data files that contain analysis overlays, including joint markers, curvature lines, and a coordinate system grid.

IMPLEMENTATION
-Set configuration variables (directories, bounding box coordinates, blue detection range, real world measurements, etc.)
-Loop through video files and store the # of frames in each video in a list
-Concatenate all video files into one large file
-Crop and flip large video file
-Loop through frames in large video file and perform analysis
For each frame:
-Detect all blue objects
-Identify Joint1, Joint2, Joint3, and EndEffector by finding the closest blue object to each previous point
-Fit curvature 
-Draw overlays for joint position, curvature, and coordinate system
-If the frame corresponds to the first or last frame of a smaller video file, store joint, curvature data in dataframe with corresponding video filename
-Save the dataframe to a csv file

If needed: use continuity to assist joint detection, via closeness nearby search
"""

import cv2
import os
import numpy as np

"""
DEFINE CONFIGURATION VARIABLES
"""

# Set the directory where the videos are stored
video_dir = "testvideodata/"

# Set the output directory for the cropped videos
output_dir = "testvideodata_analyzed/"

# Set the coordinates of the bounding box corners
top_right = (118, 61) # (456, 44)
bottom_right = (100, 476) # (470, 474)
top_left = (444, 51) # (130, 56)
bottom_left = (460, 476) # (114, 466)

end_effector = (286,184)
joint3 = (249,199)
joint2 = (164,212)
joint1 = (77,202)

# Set the desired aspect ratio for the cropped video
aspect_ratio = (int(48*2), int(58.5*2))

"""
DEFINE VISUALIZATION FUNCTIONS
"""

def add_origin_marker(frame):
    # Draw a bright red circle at the origin
    origin = (0, 205)
    radius = 3
    color = (0, 0, 255)
    thickness = -1
    cv2.circle(frame, origin, radius, color, thickness)

    # Draw a horizontal line across 202
    line_start = (0, 205)
    line_end = (frame.shape[1], 202)
    line_color = (0, 0, 255)
    line_thickness = 1
    cv2.line(frame, line_start, line_end, line_color, line_thickness)

    return frame

def add_coordinate_overlay(frame, aspect_ratio_scaled, grid_spacing=5):
    # Get the height and width of the frame
    height, width = frame.shape[:2]

    # Create a blank image to draw the grid on
    grid_img = np.zeros((height, aspect_ratio_scaled[0], 3), np.uint8)

    # Define the coordinate system origin in real-world coordinates
    origin = (0, 202) # in inches

    # Define the x and y grid spacing in inches
    x_spacing = grid_spacing
    y_spacing = grid_spacing

    # Convert the x and y grid spacing to pixel spacing
    x_spacing_px = int(x_spacing * aspect_ratio_scaled[0] / 48) # 48 inches is the width of the video
    y_spacing_px = int(y_spacing * aspect_ratio_scaled[1] / 58.5) # 58.5 inches is the height of the video

    # Draw the vertical grid lines
    for x in range(0, aspect_ratio_scaled[0], x_spacing_px):
        cv2.line(grid_img, (x, 0), (x, height), (255, 255, 255), 1)
        if x > 0:
            cv2.putText(grid_img, str(int(origin[0] + x / (aspect_ratio_scaled[0] / 48))) + " in", (x - 20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Draw the horizontal grid lines
    for y in range(0, height, y_spacing_px):
        cv2.line(grid_img, (0, y), (aspect_ratio_scaled[0], y), (255, 255, 255), 1)
        if y > 0:
            cv2.putText(grid_img, str(int((y - origin[1]) / (aspect_ratio_scaled[1] / 58.8))) + " in", (20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Resize the grid image to match the aspect ratio of the frame
    grid_img_resized = cv2.resize(grid_img, (width, height))

    # Add the grid overlay to the frame
    frame_with_grid = cv2.addWeighted(frame, 0.8, grid_img_resized, 0.2, 0)

    return frame_with_grid

"""
DEFINE VIDEO PROCESSING FUNCTIONS
"""

def crop_frame(frame, aspect_ratio_scaled):
    # Calculate the perspective transform matrix
    src = np.float32([top_left, top_right, bottom_left, bottom_right])
    dst = np.float32([(0, 0), (aspect_ratio_scaled[0], 0), (0, aspect_ratio_scaled[1]), aspect_ratio_scaled])
    M = cv2.getPerspectiveTransform(src, dst)
    # src = np.float32([top_left, top_right, bottom_left, bottom_right])
    # dst = np.float32([(0, 0), (aspect_ratio_scaled[0], 0), (0, aspect_ratio_scaled[1]), aspect_ratio_scaled])
    # M = cv2.getPerspectiveTransform(src, dst)

    # Apply the perspective transform to the frame
    warped = cv2.warpPerspective(frame, M, aspect_ratio_scaled)

    # Add the real-world coordinate system as an overlay
    warped = add_coordinate_overlay(warped, aspect_ratio_scaled)

    # Add origin marker
    warped = add_origin_marker(warped)

    return warped

# def setup_video(filename):
#     # Load the video file
#     cap = cv2.VideoCapture(filename)

#     # Check if the video file was opened successfully
#     if not cap.isOpened():
#         print("Error opening video file:", filename)
#         return None, None, None, None

#     # Get the total number of frames in the video
#     num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     # Get the dimensions of the video
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # Scale up the aspect ratio to meet the current resolution
#     aspect_ratio_scaled = (int(height * aspect_ratio[0] / aspect_ratio[1]), height)

#     # Create a VideoWriter object to save the cropped video
#     out_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(filename))[0] + ".avi")
#     fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#     out = cv2.VideoWriter(out_filename, fourcc, 30.0, (aspect_ratio_scaled[0], aspect_ratio_scaled[1]))

#     return aspect_ratio_scaled

# # Define the function to process the video frames
# def process_video_frames(cap, num_frames, aspect_ratio_scaled, out, start_frame_idx):
#     # Loop through all the frames in the video
#     for frame_num in range(num_frames):
#         # Read the next frame from the video
#         ret, frame = cap.read()

#         if not ret:
#             break

#         # Crop the frame
#         cropped_frame = crop_frame(frame, aspect_ratio_scaled)

#         # Write the frame to the output video file
#         out.write(cropped_frame)

#     # Release the video file and output video file
#     cap.release()
#     out.release()
    
#     # Return the start frame index of the next video
#     return start_frame_idx + num_frames

# Define the function to crop the video
def process_video(filename):
    # Load the video file
    cap = cv2.VideoCapture(os.path.join(video_dir, filename))

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error opening video file:", filename)
        return

    # Get the total number of frames in the video
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get the dimensions of the video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Scale up the aspect ratio to meet the current resolution
    aspect_ratio_scaled = (int(height * aspect_ratio[0] / aspect_ratio[1]), height)

    # Create a VideoWriter object to save the cropped video
    out_filename = os.path.join(output_dir, os.path.splitext(filename)[0] + ".avi")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(out_filename, fourcc, 30.0, (aspect_ratio_scaled[0], aspect_ratio_scaled[1]))

    # Loop through all the frames in the video
    for frame_num in range(num_frames):
        # Read the next frame from the video
        ret, frame = cap.read()

        if not ret:
            break

        # Crop the frame
        cropped_frame = crop_frame(frame, aspect_ratio_scaled)
        print("frame", frame_num, "of", num_frames)

        # Write the frame to the output video file
        out.write(cropped_frame)
    print("Done")

    # Release the video file and output video file
    cap.release()
    out.release()

process_video("seg1_60_seg2_0_seg3_0.avi")

# # Initialize the list to store start frames
# start_frames = []

# # Loop through all the videos in the directory
# for filename in sorted(os.listdir(video_dir)):
#     if filename.endswith(".mp4") or filename.endswith(".avi"):
#         # Load the video file
#         cap = cv2.VideoCapture(os.path.join(video_dir, filename))

#         # Check if the video file was opened successfully
#         if not cap.isOpened():
#             print("Error opening video file:", filename)
#             continue

#         # Get the total number of frames in the video
#         num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#         # Get the dimensions of the video
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#         # Scale up the aspect ratio to meet the current resolution
#         aspect_ratio_scaled = (int(height * aspect_ratio[0] / aspect_ratio[1]), height)

#         # Calculate the perspective transform matrix
#         src = np.float32([top_left, top_right, bottom_left, bottom_right])
#         dst = np.float32([(0, 0), (aspect_ratio_scaled[0], 0), (0, aspect_ratio_scaled[1]), aspect_ratio_scaled])
#         M = cv2.getPerspectiveTransform(src, dst)

#         # Initialize the frame counter
#         frame_count = 0

#         # Loop through all the frames in the video
#         for frame_num in range(num_frames):
#             # Read the next frame from the video
#             ret, frame = cap.read()

#             if not ret:
#                 break

#             # Apply the perspective transform to the frame
#             warped = cv2.warpPerspective(frame, M, aspect_ratio_scaled)

#             # Add the real-world coordinate system as an overlay
#             warped = add_coordinate_overlay(warped, aspect_ratio_scaled)
            
#             # Add origin marker
#             warped = add_origin_marker(warped)

#         # Release the video file
#         cap.release()

# Close all windows
cv2.destroyAllWindows()
