### Install python packages

Due to a restriction in the RP OS, `pip` is not recommended. 
Use `sudo apt install python3-package` instead.

### Add cron job 

To make sure the system connects to wifi, we add a script to a `1 min` cron job using `sudo crontab -e`. You must use sudo so the job is added to the root user.

### Add service

Add whichever scripts as a service so that it will run when the system starts.

I am using this to keep the screen updated.

```bash
sudo systemctl daemon-reload
sudo systemctl enable myscript.service
sudo systemctl start myscript.service
```
