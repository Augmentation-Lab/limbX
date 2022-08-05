#!/bin/bash

echo " "

echo "$(date): Beginning take_photo.sh script..." >> camera_log.txt

echo "$(date '+%Y-%m-%d_%T'): Taking photo..." >> camera_log.txt
raspistill -o /home/admin/Desktop/limbX/data/$(date '+%s').jpg
echo "Photo name: $(date '+%Y-%m-%d_%T').jpg" >> camera_log.txt
echo "$(date '+%Y-%m-%d_%T'): Finished taking photo." >> camera_log.txt