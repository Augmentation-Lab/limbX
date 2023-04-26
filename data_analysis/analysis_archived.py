import cv2
import pandas as pd
import numpy as np
import os

# Set the directory where the video files are stored
video_dir = "testvideodata"

# Set the directory where the analyzed videos will be saved
output_dir = "testvideodata_analyzed"

# Set the dimensions of the blue box in inches
box_width = 48.0
box_height = 58.5

# Create an empty dataframe to store the data
columns = ["Video Filename", "Frame", "Servo1 Angle", "Servo2 Angle", "Servo3 Angle", 
           "Joint1 Position", "Joint2 Position", "Joint3 Position", "EndEffector Position", 
           "Seg1 Curvature", "Seg2 Curvature", "Seg3 Curvature", "End Curvature"]
dataframe = pd.DataFrame(columns=columns)

# Loop through all the video files in the directory
for filename in os.listdir(video_dir):
    print("Analyzing:", filename)
    if filename.endswith(".avi"):
        # Load the video file
        cap = cv2.VideoCapture(os.path.join(video_dir, filename))

        # Check if the video file was opened successfully
        if not cap.isOpened():
            print("Error opening video file:", filename)
            continue

        # Get the total number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Rotate the video 180 degrees
        rotation_matrix = cv2.getRotationMatrix2D((0, 0), 180, 1)
        flipped = False

        # Loop through all the frames in the video
        for frame_num in range(num_frames):
            # Read the next frame from the video
            ret, frame = cap.read()

            if not ret:
                break

            # Flip the frame if it hasn't been flipped yet
            if not flipped:
                frame = cv2.flip(frame, -1)
                flipped = True

            # Find the blue box in the video
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([90, 50, 50])
            upper_blue = np.array([130, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                contour = max(contours, key=cv2.contourArea)
                box = cv2.minAreaRect(contour)
                box_width_pixels = box[1][0]
                box_height_pixels = box[1][1]
                x, y = box[0]
                cv2.drawContours(frame, [np.int0(cv2.boxPoints(box))], 0, (255, 0, 0), 2)
                
                # Crop the video by the blue box
                box_width_pixels = int(box_width_pixels)
                box_height_pixels = int(box_height_pixels)
                x, y = int(x), int(y)
                cropped_frame = frame[y-box_height_pixels//2:y+box_height_pixels//2, x-box_width_pixels//2:x+box_width_pixels//2]
                cv2.imshow("Cropped Frame", cropped_frame)

                # Calculate the scale factor to convert pixels to inches
                x_scale = box_width / box_width_pixels
                y_scale = box_height / box_height_pixels

            # Find the blue markers on the robot
            # lower_blue = np.array([100, 50, 50])
            # upper_blue = np.array([140, 255, 255])
            lower_blue = np.array([27, 90, 160])
            upper_blue = np.array([234, 168, 120])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            joint_positions = []
            for contour in contours:
                if cv2.contourArea(contour) < 100:
                    # Find the center point of the contour and scale it to inches
                    M = cv2.moments(contour)
                if M["m00"] > 0:
                    cx = M["m10"] / M["m00"]
                    cy = M["m01"] / M["m00"]
                    x_inches = (cx - x) * x_scale
                    y_inches = (cy - y) * y_scale
                    joint_positions.append((x_inches, y_inches))

            # Calculate the joint positions and segment curvatures
            if len(joint_positions) == 4:
                joint1_pos = joint_positions[0]
                joint2_pos = joint_positions[1]
                joint3_pos = joint_positions[2]
                end_pos = joint_positions[3]

                # Calculate the segment curvatures
                seg1_curv = 1 / cv2.arcLength(np.array([joint1_pos, joint2_pos]), True)
                seg2_curv = 1 / cv2.arcLength(np.array([joint2_pos, joint3_pos]), True)
                seg3_curv = 1 / cv2.arcLength(np.array([joint3_pos, end_pos]), True)
                end_curv = 1 / cv2.arcLength(np.array([joint1_pos, joint2_pos, joint3_pos, end_pos]), True)

                # Get the servo angles from the filename
                servo1_angle = int(filename.split("_")[2])
                servo2_angle = int(filename.split("_")[4])
                servo3_angle = int(filename.split("_")[6][:-4])

                # Add a row of data to the dataframe
                row = [filename, frame_num == num_frames - 1, servo1_angle, servo2_angle, servo3_angle, 
                       joint1_pos, joint2_pos, joint3_pos, end_pos, seg1_curv, seg2_curv, seg3_curv, end_curv]
                dataframe = pd.concat([dataframe, pd.Series(row)], ignore_index=True)
                # dataframe = dataframe.append(pd.Series(row, index=columns), ignore_index=True)

                # Display the frame with the joint positions and segment curvatures overlaid
                font = cv2.FONT_HERSHEY_SIMPLEX
                for i, pos in enumerate(joint_positions):
                    cv2.putText(frame, f"Joint{i+1}: ({pos[0]:.2f}, {pos[1]:.2f})", (50, 50+i*50), font, 1, (255, 0, 0), 2)
                    cv2.circle(frame, (int(pos[0]/x_scale+x), int(pos[1]/y_scale+y)), 10, (255, 0, 0), -1)
                cv2.putText(frame, f"Seg1 Curvature: {seg1_curv:.3f}", (50, 250), font, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Seg2 Curvature: {seg2_curv:.3f}", (50, 300), font, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Seg3 Curvature: {seg3_curv:.3f}", (50, 350), font, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"End Curvature: {end_curv:.3f}", (50, 400), font, 1, (0, 255, 0), 2)
            
            else:
                # Add a row to the dataframe with NaN values
                new_row = {"Video Filename": filename, "Frame": 1, "Servo1 Angle": np.nan,
                        "Servo2 Angle": np.nan, "Servo3 Angle": np.nan,
                        "Joint1 Position": np.nan, "Joint2 Position": np.nan,
                        "Joint3 Position": np.nan, "EndEffector Position": np.nan,
                        "Seg1 Curvature": np.nan, "Seg2 Curvature": np.nan,
                        "Seg3 Curvature": np.nan, "End Curvature": np.nan}
                dataframe = pd.concat([dataframe, pd.Series(new_row)], ignore_index=True)

            # # Write the frame to the output video file
            # # Write the frame to the output video file
            # out_filename = os.path.join(output_dir, filename[:-4] + f"_frame{frame_num}.avi")
            # out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(*"MJPG"), 30.0, (frame.shape[1], frame.shape[0]))
            # out.write(frame)
            # out.release()

            # Write the frame to the output video file
            if frame_num == 0:
                out_filename = os.path.join(output_dir, filename)
                out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(*"MJPG"), 30.0, (frame.shape[1], frame.shape[0]))
            out.write(frame)
            if frame_num == num_frames - 1:
                out.release()

            # Display the frame
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        # Release the video file
        cap.release()

# Save the dataframe to a CSV file
dataframe.to_csv("data.csv", index=False)

# Close all windows
cv2.destroyAllWindows()


