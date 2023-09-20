#!/bin/bash

export DEFAULT_AP="TELLO-9AFD00"
export TARGET_AP="${TARGET_AP:-$DEFAULT_AP}"

while [ "true" == "true" ]; do
    # Rescan for wifi access points
    nmcli dev wifi rescan

    # Sleep for 1 second
    sleep 1

    # List the wireless APs
    RESULTING_APS=$(nmcli dev wifi list | grep $TARGET_AP)
    RESULTING_APS_LEN=$(nmcli dev wifi list | grep $TARGET_AP | wc -l)
    CONNECTED_AP=$(nmcli dev wifi list | grep '*' | grep $TARGET_AP | wc -l)

    # Connect to the AP if there is a match and it is not already connected
    if [ $RESULTING_APS_LEN -eq 1 ]; then
        if [ $CONNECTED_AP -eq 0 ]; then
            nmcli dev wifi connect $TARGET_AP
        fi
    fi

done