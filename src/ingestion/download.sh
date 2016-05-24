#! /bin/bash

BUCKET=$1
TARGET_DIR=$2

aws s3 cp s3://$BUCKET $TARGET_DIR --recursive
