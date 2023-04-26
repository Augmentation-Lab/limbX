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
-Servo1 Angle
-Servo2 Angle
-Servo3 Angle
-Joint1 Position
-Joint2 Position
-Joint3 Position
-EndEffector Position
2. Video data files that contain analysis overlays, including joint markers, curvature lines, and a coordinate system grid.

IMPLEMENTATION
-Set configuration variables (directories, bounding box coordinates, blue detection range, real world measurements, etc.)
For each frame:
-Transform the video frame by cropping
-Detect all blue objects
-Identify Joint1, Joint2, Joint3, and EndEffector by finding the closest blue object to each previous point
-Store this data in a pandas dataframe
-Fit curvature 
-Draw overlays for joint position, curvature, and coordinate system
-Save the dataframe to a csv file

If needed: use closeness / nearby search to distinguish joints
"""

import cv2
import os
import numpy as np
import view as v
import math

"""
DEFINE CONFIGURATION VARIABLES
"""

# Set the directory where the videos are stored
input_dir = "testvideodata/"

# Set the output directory for the cropped videos
output_dir = "testvideodata_analyzed/"

# Set the coordinates of the bounding box corners
top_right = (118, 61) # (456, 44)
bottom_right = (100, 476) # (470, 474)
top_left = (444, 51) # (130, 56)
bottom_left = (460, 476) # (114, 466)
origin = (0, 205)

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

def add_joint_markers(frame, joint_positions, aspect_ratio_scaled):
    # print(joint_positions)
        for joint, position in joint_positions.items():
            # print("joint: ", joint, "position: ", position)
            # Draw a bright red circle at the origin
            radius = 3
            color = (0, 0, 255)
            thickness = -1
            cv2.circle(frame, position, radius, color, thickness)
            position_real = pixel_to_real(position, aspect_ratio_scaled, frame)
            text = joint + ": (" + str(position_real[0]) + " in, " + str(position_real[1]) + " in)"
            cv2.putText(frame, text, (position[0] - 20, position[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
        return frame

def pixel_to_real(pixel_coord, aspect_ratio_scaled, frame):
    # Convert the pixel coordinates to real-world coordinates
    x_real = pixel_coord[0] * (48 / frame.shape[1])
    y_real = (pixel_coord[1] - 205) * (58.8 / frame.shape[0])
    # y_real = pixel_coord[1] * (58.8 / frame.shape[0])

    # Round the real-world coordinates to two decimal places
    x_real = round(x_real, 2)
    y_real = round(y_real, 2)

    return (x_real, y_real)

def add_coordinate_overlay(frame, aspect_ratio_scaled, grid_spacing=5):
    # Get the height and width of the frame
    height, width = frame.shape[:2]

    # Create a blank image to draw the grid on
    grid_img = np.zeros((height, aspect_ratio_scaled[0], 3), np.uint8)

    # Define the coordinate system origin in real-world coordinates
    origin = (0, 205) # in inches

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
            cv2.putText(grid_img, str(int((origin[0] + x) / (aspect_ratio_scaled[0] / 48))) + " in", (x - 20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

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

    # Apply the perspective transform to the frame
    warped = cv2.warpPerspective(frame, M, aspect_ratio_scaled)

    return warped

def add_overlays(frame, joint_positions, aspect_ratio_scaled):
    # Add joint markers
    frame = add_joint_markers(frame, joint_positions, aspect_ratio_scaled)

    # Add the real-world coordinate system as an overlay
    frame = add_coordinate_overlay(frame, aspect_ratio_scaled)

    # Add origin marker
    frame = add_origin_marker(frame)

    return frame

import pandas as pd

def extract_data(cropped_frame, filename):
    # Convert the cropped frame to HSV color space
    hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper ranges of blue color in HSV color space
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([140, 255, 255])

    # Threshold the cropped frame using the blue color range
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find the contours of the blue objects in the binary image 
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    frame_size = cropped_frame.shape[:2]
    # Filter out the contours that are within 10 pixels of the edge of the video
    contours_filtered = []
    for contour in contours:
        if (contour[:, 0, 0] > 10).all() and (contour[:, 0, 0] < frame_size[1] - 10).all() and (contour[:, 0, 1] > 10).all() and (contour[:, 0, 1] < frame_size[0] - 10).all():
            contours_filtered.append(contour)
    contours = contours_filtered

    # Sort the contours by size in descending order and take the largest three
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]
    # Find center of mass of each contour as tuple of ints
    joints = [tuple(map(int, np.mean(contour, axis=0)[0])) for contour in contours]

    # Visualize the contours 
    cropped_frame = cv2.drawContours(cropped_frame, contours, -1, (255, 0, 0), 3)

    # Define a helper function to calculate the distance between two points
    def distance(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    # Define a list of joint labels
    joint_labels = ["Joint1", "Joint2", "Joint3", "EndEffector"]

    # Initialize an empty dictionary to store the joint positions
    joint_positions = {}

    # Find the joints in order
    for i, label in enumerate(joint_labels):
        if i == 0: # Joint1 is closest to the origin
            joint_positions[label] = min(joints, key=lambda p: distance(p, (0, 205)))
        else: # Find the closest joint that is not already labeled
            joints.remove(joint_positions[joint_labels[i-1]])
            joint_positions[label] = min(joints, key=lambda p: distance(p, joint_positions[joint_labels[i-1]]))

    # Create a Pandas dataframe to store the joint position data
    servo_angles = filename.split("_")
    servo1_angle = servo_angles[1]
    servo2_angle = servo_angles[3]
    servo3_angle = servo_angles[5].split(".")[0]
    data = {"Video Filename": filename, "Servo1 Angle": servo1_angle, "Servo2 Angle": servo2_angle, "Servo3 Angle": servo3_angle, "Joint1 Position": str(joint_positions["Joint1"]), "Joint2 Position": str(joint_positions["Joint2"]), "Joint3 Position": str(joint_positions["Joint3"]), "EndEffector Position": str(joint_positions["EndEffector"])}

    return data, joint_positions, cropped_frame

# Define the function to process the video
def process_video(filename, df):
    # Load the video file
    cap = cv2.VideoCapture(os.path.join(input_dir, filename))

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
        data, joint_positions, cropped_frame = extract_data(cropped_frame, filename)
        overlayed_frame = add_overlays(cropped_frame, joint_positions, aspect_ratio_scaled)
        final_frame = overlayed_frame
        if frame_num == 200:
            print("Final frame")
            new_row = pd.DataFrame(data, index=[0])
            # Append the new row to the global dataframe
            df = df.append(new_row, ignore_index=True)
            # Save an image of the frame
            cv2.imwrite(os.path.join(output_dir, f"{filename.split('.')[0]}_final_frame.jpg"), final_frame)
        
        # Write the frame to the output video file
        out.write(final_frame)

    # Release the video file and output video file
    cap.release()
    out.release()
    return df

def sort_by_file_order(file_list):
    # Sort the file list in place based on the order they were taken
    file_list.sort(key=lambda x: (
        int(x.split("_")[1]),  # sort by j value
        int(x.split("_")[3]),  # then by i value
        int(x.split("_")[5].split(".")[0])  # then by k value
    ))
    # reverse file list
    file_list.reverse()

    return file_list

df = pd.DataFrame(columns=["Video Filename", "Servo1 Angle", "Servo2 Angle", "Servo3 Angle", "Joint1 Position", "Joint2 Position", "Joint3 Position", "EndEffector Position"])
# Loop through all the videos in the directory
# joint_positions = {}
for filename in sort_by_file_order(os.listdir(input_dir)):
        # Crop the video
        print("Preprocessing:", filename)
        df = process_video(filename, df)

# Save the dataframe to a CSV file
df.to_csv("data.csv", index=False)
print("All done.")
cv2.destroyAllWindows()

v.play_videos_from_directory(output_dir)
