#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <new_uid>"
    exit 1
fi

new_uid=$1

files=$(ls ../dashboards/*)

echo $files


for file_path in $files; do
    sed -i "s/\"uid\": \"Your prometheus data source uid\"/\"uid\": \"$new_uid\"/g" "$file_path"
done

echo "UID successfully updated to $new_uid in $file_path"
