# Gadget – Raspberry Pi Zero 2 W Sandbox

This repository serves as a sandbox environment for experimenting with the Raspberry Pi Zero 2 W, focusing on gadget modes, e-paper displays, microphones, and more.

## Setup

The files in this repository are organized to mirror the system's directory structure. To set up, copy each file to its corresponding folder on your Raspberry Pi. Hopefully, this helps align with the provided scripts and notes. 

## Installing Python Packages

Due to restrictions in the Raspberry Pi OS, it's advisable to avoid using `pip` for system-wide installations. Instead, install Python packages using the package manager with:


```bash
sudo apt install python3-[package-name]
```


Replace `[package-name]` with the specific name of the package you wish to install. This method ensures compatibility and proper integration with the system.

## Adding a Cron Job

To ensure the system maintains a Wi-Fi connection, you can add a script to run every minute using cron. Edit the root user's crontab with:


```bash
sudo crontab -e
```


Add the following line to schedule the script to run every minute:


```bash
* * * * * /usr/local/bin/wifi-up.sh
```


Ensure you use `sudo` to edit the root crontab, so the job is added for the root user.

## Adding a Service

To run scripts automatically at system startup, add them as services. This approach is useful for tasks like keeping the display updated. First, create a service file, for example:

```bash
sudo nano /etc/systemd/system/show-time-wifi.service
```

Add the following content to the service file:

```ini
[Unit]
Description=Show Time and WiFi on E-Ink Display
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/usr/local/bin
ExecStart=/bin/bash -c 'python3 show-time-wifi.py'
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then, reload the systemd manager configuration and enable the service to start on boot:

```bash
sudo systemctl daemon-reload
sudo systemctl enable show-time-wifi.service
sudo systemctl start show-time-wifi.service
```

This setup ensures your script runs at startup and restarts automatically if it fails. 
