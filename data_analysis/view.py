import argparse
import os
import cv2

# Create a window to display the video
cv2.namedWindow('Video')

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

def play_videos_from_directory(directory_path):
    # Loop through all files in the directory
    fileorder = sort_by_file_order(os.listdir(directory_path))
    for filename in fileorder:
        # Check if the file is a video (based on file extension)
        if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
            # Open the video file using OpenCV
            video = cv2.VideoCapture(os.path.join(directory_path, filename))

            # Check if the video file was opened successfully
            if not video.isOpened():
                print(f"Could not open video file: {filename}")
                continue

            # Loop through all frames in the video and display them
            while True:
                # Read the next frame from the video
                ret, frame = video.read()

                # Check if the frame was read successfully
                if not ret:
                    break

                # Display the current frame in a window
                cv2.imshow(filename, frame)

                # Wait for a short period of time (in milliseconds)
                cv2.waitKey(25)

            # Release the video object and destroy the window
            video.release()
            cv2.destroyAllWindows()

def play_single_video_on_loop(video_file_path):
    # Load the video file
    cap = cv2.VideoCapture(video_file_path)


    def mouse_callback(event, x, y, flags, param):
        # Check if the left mouse button was clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            # Get the color of the pixel at the current cursor position
            b, g, r = frame[y, x]
            print(f"Pixel value at ({x}, {y}): R={r}, G={g}, B={b}")
    
    # Set the mouse callback function for the window
    cv2.setMouseCallback('Video', mouse_callback)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Read and display each frame of the video
    while True:
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Release the video file and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Play videos using OpenCV")
    parser.add_argument("path", type=str, help="Path to a directory or a video file to play")
    parser.add_argument("--mode", type=str, default="dir", choices=["dir", "single"], help="Choose whether to play all videos in a directory or a single video on loop")
    args = parser.parse_args()

    # Call the appropriate function based on the chosen mode
    if args.mode == "dir":
        play_videos_from_directory(args.path)
    elif args.mode == "single":
        play_single_video_on_loop(args.path)
