# This script pre-processes the video data by flipping & cropping by bounding box

import cv2
import os
import numpy as np

# Set the directory where the videos are stored
video_dir = "testvideodata/"

# Set the output directory for the cropped videos
output_dir = "testvideodata_preprocessed/"

# Set the coordinates of the bounding box corners
top_right = (118, 61) # (456, 44)
bottom_right = (100, 476) # (470, 474)
top_left = (444, 51) # (130, 56)
bottom_left = (460, 476) # (114, 466)

# Set the desired aspect ratio for the cropped video
aspect_ratio = (int(48*2), int(58.5*2))

# def add_joint_markers(frame):
#     # Convert the frame to HSV color space
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # Define the range of blue color in HSV
#     # lower_blue = np.array([100, 50, 50])
#     # upper_blue = np.array([130, 255, 255])
#     lower_blue = np.array([27, 90, 160])
#     upper_blue = np.array([234, 168, 120])

#     # Threshold the HSV image to get only blue colors
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)

#     # Find contours in the mask
#     contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Draw bright red circles on top of each blue joint marker
#     radius = 5
#     color = (0, 0, 255)
#     thickness = -1
#     for contour in contours:
#         (x, y, w, h) = cv2.boundingRect(contour)
#         cv2.circle(frame, (x + int(w/2), y + int(h/2)), radius, color, thickness)

#     return frame

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

# Define the function to crop the video
def crop_video(filename):
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

    # Calculate the perspective transform matrix
    src = np.float32([top_left, top_right, bottom_left, bottom_right])
    dst = np.float32([(0, 0), (aspect_ratio_scaled[0], 0), (0, aspect_ratio_scaled[1]), aspect_ratio_scaled])
    M = cv2.getPerspectiveTransform(src, dst)
    # Calculate the perspective transform matrix
    # src = np.float32([top_left, top_right, bottom_left, bottom_right])
    # dst = np.float32([(aspect_ratio_scaled[0], aspect_ratio_scaled[1]), (0, aspect_ratio_scaled[1]), (aspect_ratio_scaled[0], 0), (0, 0)])
    # M = cv2.getPerspectiveTransform(src, dst)

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

        # # Rotate the frame by 180 degrees
        # frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Apply the perspective transform to the frame
        warped = cv2.warpPerspective(frame, M, aspect_ratio_scaled)

        # Add the real-world coordinate system as an overlay
        warped = add_coordinate_overlay(warped, aspect_ratio_scaled)
        
        # Add origin marker
        warped = add_origin_marker(warped)

        # Write the frame to the output video file
        out.write(warped)

    # Release the video file and output video file
    cap.release()
    out.release()

# Loop through all the videos in the directory
for filename in os.listdir(video_dir):
    if filename.endswith(".mp4") or filename.endswith(".avi"):
        # Crop the video
        print("Cropping:", filename)
        crop_video(filename)

# Close all windows
cv2.destroyAllWindows()
