#!/bin/bash

export DEFAULT_AP="TELLO-9AFD00"
export TARGET_AP="${TARGET_AP:-$DEFAULT_AP}"

while [ "true" == "true" ]; do
    # Rescan for wifi access points
    nmcli dev wifi rescan

    # Sleep for 1 second
    sleep 1

    # List the wireless APs
    nmcli dev wifi list | grep $TARGET_AP

done