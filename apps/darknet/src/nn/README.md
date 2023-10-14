# Neural Networks

- https://github.com/hank-ai/darknet
- This directory should be mounted to `/opt/nn`

- Take a dataset, split into training/validation/test:

```bash=
# in the dataset src dir

# Get counts
#TEST_COUNT=$(echo $(($IMG_COUNT * .10)) | awk '{print int($1+0.5)}')

IMG_COUNT=$(find . -not -name "*.txt" | wc -l)
TEST_COUNT=0
VALIDATION_COUNT=$(echo $(($IMG_COUNT * .25)) | awk '{print int($1+0.5)}')
TRAIN_COUNT=$(($IMG_COUNT - $TEST_COUNT - $VALIDATION_COUNT))

echo "Image Count: $IMG_COUNT"
echo "Test Count: $TEST_COUNT"
echo "Validation Count: $VALIDATION_COUNT"
echo "Train Count: $TRAIN_COUNT"

# Get file list randomly shuffle
#IMAGE_LIST=$(find . -not -name "*.txt"  -printf "%f\n" | grep ".*\.jpg$" | shuf)

IMAGE_LIST=$(find . -not -name "*.txt" -not -type d -printf "%f\n" | shuf)

# Move the test images out
TEST_IMAGES=$(echo $IMAGE_LIST | head -n $TEST_COUNT)
for img in $(echo ${TEST_IMAGES}); do TXT_F_NO_EXT=${img%.*}; TXT_F="${TXT_F_NO_EXT}.txt"; mv -v $img ../test/; mv -v $TXT_F ../test/; done;

# Get the file list again
IMAGE_LIST=$(find . -not -name "*.txt" -not -type d -printf "%f\n" | shuf)

VALIDATION_IMAGES=$(echo $IMAGE_LIST | head -n $VALIDATION_COUNT)
for img in $(echo ${VALIDATION_IMAGES}); do TXT_F_NO_EXT=${img%.*}; TXT_F="${TXT_F_NO_EXT}.txt"; mv -v $img ../valid/; mv -v $TXT_F ../valid/; done;

# Remaining images are training set images

cd ..

# Create image lists
cd test
TEST_IMAGE_LIST=$(find . -not -name "*.txt" -not -type d -printf "%f\n")

cd ../valid
VALIDATION_IMAGE_LIST=$(find . -not -name "*.txt" -not -type d -printf "%f\n")

cd ../train
TRAIN_IMAGE_LIST=$(find . -not -name "*.txt" -not -type d -printf "%f\n")

cd ../..
rm hats_train.txt
rm hats_valid.txt
touch hats_train.txt
touch hats_valid.txt
for img in $(echo $VALIDATION_IMAGE_LIST); do echo "./dataset/valid/$img" >> hats_valid.txt; done
for img in $(echo $TRAIN_IMAGE_LIST); do echo "./dataset/train/$img" >> hats_train.txt; done
```

## Training the Model with Podman

```bash=
# Test
podman run --rm -it --device nvidia.com/gpu=all --security-opt=label=disable quay.io/kenmoini/darkness:darknet-ubnt22 nvidia-smi
podman run --rm -it --device nvidia.com/gpu=all --security-opt=label=disable quay.io/kenmoini/darkness:darknet-ubnt22 darknet version

# Training
podman run --rm -it -v ./apps/darknet/src/nn:/opt/nn --device nvidia.com/gpu=all --security-opt=label=disable quay.io/kenmoini/darkness:darknet-ubnt22 /bin/bash

$ cd /opt/nn/hats
$ darknet detector -map -dont_show train hats.data hats.cfg
$ darknet detector -dont_show train hats.data hats.cfg # cuDNN bug?

$ cd /opt/nn/railways
$ darknet detector -map -dont_show train railways.data railways.cfg

# Image Inference, with JSON data
darknet detector test -dont_show hats.data hats.cfg hats_best.weights dataset/test/005321_jpg.rf.b5f0e98c15af5be7f4e08b30d977da11.jpg -out hat_prediction.json

# Image Inference, with JSON data, with a minimum threshold of 50%
darknet detector test -dont_show hats.data hats.cfg hats_best.weights -out hat_prediction.json -thresh 0.5 dataset/test/005321_jpg.rf.b5f0e98c15af5be7f4e08b30d977da11.jpg

darknet detector test -dont_show railways.data railways.cfg railways_best.weights dataset/pexels-krivec-ales-552779.jpg -out railways_prediction.json
darknet detector test -dont_show railways.data railways.cfg railways_best.weights dataset/pexels-pixabay-258421.jpg -out railways_prediction.json

# Video Inference, display detected object locations and store output in a text file
darknet detector demo -dont_show hats.data hats.cfg ./cudnn-model/hats_final.weights GOPRO_1697242189.MP4 -out_filename prediction.mkv -ext_output > prediction.txt
darknet detector demo -dont_show hats.data hats-test.cfg hats_best.weights GOPRO_1697242189.MP4 -out_filename prediction.mkv -ext_output > prediction.txt
# then use the parse-video-inference/parse_output.py file to convert to JSON blob

# JSON + Media Server Output from Video
darknet detector demo -dont_show hats.data hats.cfg hats_best.weights GOPRO_1697242189.MP4 -json_port 8070 -mjpeg_port 8090 -ext_output

```

## Building Multi-arch Model Containers

The easiest way to distribute models is via a slimline container that you can copy models over from via an initContainer.

```bash=
# Run this on an x86_64 and aarch64 system
./hack/build-and-push-models.sh

# Run this on one system
./hack/build-and-push-model-manifest.sh
```