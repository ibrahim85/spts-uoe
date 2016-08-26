#! /bin/bash

# command params
DIR=$1
SOURCE=$2
URL=$3
FROM=$4
TO=$5
SIZE_THRESHOLD=$6
TMP_FOLDER=$7

# set up file name
DATE_TIME=`date +%Y-%m-%d:%H:%M:%S`
FILE_NAME="$DIR/$SOURCE-$DATE_TIME.json"

# init variables
HTTP_STATUS=0
ATTEMPTS=0
SIZE=0

while [[ $ATTEMPTS < 3 && ($HTTP_STATUS != 200 || $SIZE -lt $SIZE_THRESHOLD) ]]
do
    # sleep for a given amount of a time between retries
    if [[ "$ATTEMPTS" > 0 ]]; then
	sleep 6s
    fi

    # store the status code in a variable and send output to FILE_NAME
    HTTP_STATUS=$(curl -sw "%{http_code}" -o >(cat > $FILE_NAME) $URL) 

    # store the size of the file
    SIZE=$(ls -nl $FILE_NAME | awk '{print $5}')

    ((ATTEMPTS++))
done

# send notification email if service is down
if [[ "$HTTP_STATUS" != 200 ]]; then
    # delete the output file
    rm $FILE_NAME
	
    # get the response headers
    BODY=$(curl -sI $URL)

    # send a notification email and discard output
    aws ses send-email --from $FROM --to $TO --subject "SPTS Error: $HTTP_STATUS $SOURCE" --text "$URL $BODY" >/dev/null

    exit 0
fi

# move file for inspection if size is not valid 
if [[ $SIZE -lt $SIZE_THRESHOLD ]]; then
    mv $FILE_NAME $TMP_FOLDER
fi

