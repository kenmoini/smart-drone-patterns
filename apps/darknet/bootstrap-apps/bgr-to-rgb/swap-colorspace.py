# python3 -m pip install Pillow matplotlib --user
import sys, os
import argparse
import matplotlib.pyplot as plt

# Define and parse the input arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--input", help="input image")
argParser.add_argument("-o", "--output", help="output image")
args = argParser.parse_args()

# Check to see if the input image exists
if not os.path.isfile(args.input):
    print("The input file does not exist")
    sys.exit(1)

# Check to see if the output is specified
if args.output is None:
    targetFile = args.input
else:
    targetFile = args.output

# Load the image
plt.ion()
img = plt.imread(args.input)

# Rotate and save the image
plt.imsave(fname=targetFile, arr=img[:,:,[2,1,0]])