mkdir -p /home/pi/frame/photos
sudo apt-get update
sudo apt-get install rsync
sudo apt-get install feh
sudo apt-get install unclutter


#!/bin/sh
#
# Script to run Digital Picture Frame using Feh
# drware@thewares.net
#

# Change number below to the duration, in seconds
# for each photo to be displayed
DELAY="60"

# hide the cursor after 15 seconds
/usr/bin/unclutter -idle 15 &

# Start slide show
/usr/bin/feh --quiet --recursive --randomize --full-screen \ --slideshow-delay $
DELAY /home/pi/frame/photos/ &

# Phone home and sync
/home/pi/frame/rsync.sh

exit 0

#!/bin/sh
#
# Script to run Digital Picture Frame using Feh
# drware@thewares.net
#

# Change number below to the duration, in seconds
# for each photo to be displayed
DELAY="60"

# Set display so that the script will effect
# the screen on the frame
export DISPLAY=:0

# Stop the currently running Slide show
/home/pi/frame/kill.sh feh

sleep 10s

# Start slide show
feh --quiet --recursive --randomize --full-screen --slideshow-delay $DELAY /home
/pi/frame/photos/ &

exit 0


#!/bin/sh
#
# Script to copy and remove photos on the DPF
# Script requires that a rsync server on a machine
# separate from the DPF be running and configured
#
# drware@thewares.net
#

PATH=/sbin:/usr/sbin:/usr/bin:/usr/local/bin

INTERNAL="192.168.1.87"

#When frame is inside your network and will connect
#via an intranet
rsync -v -rlt -z --chmod=a=rw,Da+x --delete --bwlimit=2048 $INTERNAL::Frame /home/pi/frame/photos/
