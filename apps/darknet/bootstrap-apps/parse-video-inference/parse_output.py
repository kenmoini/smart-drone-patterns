# Description: This script parses the output of the video inference text blob into JSON
# python3 parse_output.py -i <input file> -o <output file>
# python3 parse_output.py -i output-test.txt -o output-test.json
import json, argparse, os, sys

# Define and parse the input arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--input", help="input text stream")
argParser.add_argument("-o", "--output", help="output JSON file")
args = argParser.parse_args()

# Check to see if the input image exists
if not os.path.isfile(args.input):
    print("The input file does not exist")
    sys.exit(1)

inputTextFile = open(args.input, "r")

lines = inputTextFile.readlines()

video_data = {}
frames = []
frame = {}
frameCount = 1
fileNameDetected = False
fileInfoDetected = False
frameBlockFound = False

for line in lines:

    # Detect video info
    if fileNameDetected == False:
        if "video file:" in line:
            video_file = line.split(" ")[2].strip()
            video_data["video_file"] = video_file
            fileNameDetected = True
            continue
    if fileInfoDetected == False:
        if "Video stream:" in line:
            video_width = line.split(" ")[2]
            video_height = line.split(" ")[4]
            video_data["video_size"] = video_width + "x" + video_height
            fileInfoDetected = True
            continue

    # Detect when frame processing starts
    if "Objects:" in line:
        frameBlockFound = True
        frame["frame_number"] = frameCount
        frame["objects"] = []
        continue

    # Detect when frame processing ends
    if "FPS:" in line:
        frameBlockFound = False
        frames.append(frame)
        frame = {}
        # Increase the count
        frameCount += 1
        continue

    # Detect when stream processing ends
    if "input video stream closed" in line:
        video_data["frame_count"] = frameCount
        break

    # Parse frame data
    if frameBlockFound:
        # If there is a detected object with an accuracy level
        if "%" in line:
            object = {}
            # Occasionally there are multiple class objects on a single line delimited by a comma if it thinks it could be one of multiple objects

            classOb = line.split(":")[0].strip()
            if classOb != "":
                object["class"] = classOb
                object["confidence"] = line.split(":")[1].strip().split("%")[0] + "%"
                
                coord = line.split("(")[1].strip().split(")")[0].split()
                coordinates = {}
                # Loop through the coordinate object
                for i in range(len(coord)):
                    c = coord[i].replace(":","").strip()
                    if c == "left_x":
                        coordinates["left_x"] = coord[i+1]
                    elif c == "top_y":
                        coordinates["top_y"] = coord[i+1]
                    elif c == "width":
                        coordinates["width"] = coord[i+1]
                    elif c == "height":
                        coordinates["height"] = coord[i+1]
                object["coordinates"] = coordinates
                frame["objects"].append(object)

# Add frames to video data
video_data["frames"] = frames

# Close the input file
inputTextFile.close()

# Determine the output file name
if args.output is None:
    output_file = ".".join(video_data['video_file'].split(".")[:-1]) + "_output.json"
else:
    output_file = args.output

# Write the output to a file
with open(output_file, 'w') as outfile:
    json.dump(video_data, outfile)
