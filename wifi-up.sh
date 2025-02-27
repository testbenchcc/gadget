#!/bin/bash

# Define the server to ping (Google Public DNS)
SERVER=8.8.8.8

# Ping the server twice, discarding the output
ping -c2 ${SERVER} > /dev/null

# Check the exit status of the ping command.
# If the ping fails (non-zero exit status), then proceed to reset the WiFi.
if [ $? != 0 ]; then
    # Bring down the WiFi interface (wlan0)
    sudo ip link set wlan0 down
    # Wait for 1 second to allow the change to take effect
    sleep 1
    # Bring the WiFi interface back up
    sudo ip link set wlan0 up
fi
