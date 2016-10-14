#!/bin/sh

# Download URL (CHANGE THIS!)
URL=http://foo.bar/not-a-real-url

# Directory Name
DIR=data-`date +"%m-%d-%y"`

# If directory doesn't exist, create it
if [ ! -d $DIR ]; then
  mkdir $DIR
fi

cd $DIR

wget -r -nH -nd -np -R index.html* $URL

# Note on the flags I used:
# -r: recursive (to crawl through all the subdirectories)
# -nH: ignore host directories
# -nd: ignore directory hierarchy (wanted them all in one directory)
# -np: don't go to parent directory
# -R: reject index.html files
