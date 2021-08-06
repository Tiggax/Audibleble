#!/bin/bash
AUTHCODE="<INSERT_YOUR_AUTH-CODE>"
OUT_DIR="<YOUR/WANTED/OUTPUT/DIRECTORY>"
AAX_PATH="<INSERT/PATH/TO/YOUR/FOLDER/CALLED/AAXtoMP3>"
#----------------------------------------------------------------------------------------------
PATH=$AAX_PATH:$PATH
echo "Checking Correct setup..."
if [ $AUTHCODE == "<INSERT_YOUR_AUTH-CODE>" ]
then
    echo "ERROR: First setup your system by editing this file, and setting the top parameters!"
    exit
fi
if [ $OUT_DIR == "<YOUR/WANTED/OUTPUT/DIRECTORY>" ]
then
    echo "ERROR: First setup your system by editing this file, and setting the top parameters!"
    exit
fi
if [ $AAX_PATH == "<INSERT/PATH/TO/YOUR/FOLDER/CALLED/AAXtoMP3>" ]
then
    echo "ERROR: First setup your system by editing this file, and setting the top parameters!"
    exit
fi


if [ -e "login" ]
then
    echo "Syncing Library..."
    python Sync.py
    if [ $? -eq 1 ]
    then
        echo "Sync successful"
        echo "Converting files..."
        AAXtoMP3 
    fi
else
echo "Use Create_Account.py to create your login file"
fi
