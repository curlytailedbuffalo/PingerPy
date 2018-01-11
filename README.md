# PingerPy
A python version of the locally run EXE that is part of the Smartthings Host Pinger Smartapp.
Host Pinger - https://github.com/craigktreasure/STHostPinger

When looking into the Smartthings HostPinger Smartapp I wanted a way to be able to run it without having to use a windows machine or any fancy programs to run the EXE file from linux or mac.
This is where PingerPy came from - a python version of the Host Pinger EXE with a web page for configuration.
Once configured this will work with the Host Pinger Smartapp to display the server status of configured hosts.

## Details
The PingerPy application is made up of 2 parts:
1. PingerPy - main module
2. PingerPy - web server

The PingerPy web server allows you to configure the installation without having to manually edit the config file
You will be able to add hosts, and set the configuration through the web server URL

## Installation

### General Install
Installation should be fairly easy. The only requirement is that the system is running python 2.7
1. Copy the directory to your computer

```
git clone https://github.com/curlytailedbuffalo/PingerPy.git /pingerpy
```

2. Make runonce.sh executable 

```
chmod u+x runonce.sh
```

3. Execute runonce.sh 

```
./runonce.sh
```

4. Now you can run the main program with 

```
./run.sh
```

Runonce is used to set the permissions values for all the other executable files, once complete run.sh initiates the actual main PingerPy and PingerPy web server.

The main PingerPy app will run even if the configuration file is not set. It will sleep for 5 minutes and then check again for the configuration file, if it is found it will run as normal pinging all the configured hosts and sending the status to Smartthings

### Configuration
Configuration is set in the settings/config.json file.
You can set the configuration manually or you can use the web server page to set the configuration.
* Web server access: 'localhost:9092' - home page, add hosts
* Web server access: 'localhost:9092/setup' - initial configuration page

### Running
These scripts can be run in a couple ways. The easiest way is from the root folder

```
./run.sh
```
This will run both the server and the main app. To run one or the other you can use

```
./PingerPy
./PingerPy_webserver
```

#### Startup Scripts
Startup scripts that can be used with Debian have been provided in the startup-scripts folder.
There is a script for each PingerPy and PingerPy_webserver. The web server is not required for PingerPy to work.

## Reminder
* You will need to install the Host Pinger smartapp and device handlers for this to work.

