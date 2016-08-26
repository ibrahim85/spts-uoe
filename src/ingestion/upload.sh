#! /bin/bash

# command params
SOURCE_DIR=$1
TAG=$2
BUCKET=$3

# set up file name
DATE_TIME=`date +%Y-%m-%d:%H:%M:%S`
COMPRESSED_FILE="$TAG-$DATE_TIME.zip"

# compress all the json filed in the given folder
zip -qrmjT $COMPRESSED_FILE $SOURCE_DIR 
ZIP_STATUS=$?

# upload the zip file to s3
if [[ "$ZIP_STATUS" == 0 ]]; then
    aws s3 mv --quiet $COMPRESSED_FILE s3://$BUCKET/$COMPRESSED_FILE
fi

