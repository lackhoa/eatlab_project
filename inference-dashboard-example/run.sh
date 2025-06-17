#
#!/bin/bash

# Check if a path argument is provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <VIDEO_DIR> <VIDEO_FILE>"
    exit 1
fi

VIDEO_DIR=$1
VIDEO_FILE=$2

# Print results
echo "Directory: $VIDEO_DIR"
echo "Filename: $VIDEO_FILE"

docker run --net=host --entrypoint /bin/sh --volume "${VIDEO_DIR}":/videos eatlab_project-client -c "python /code/main.py --video_path=/videos/${VIDEO_FILE}"
#