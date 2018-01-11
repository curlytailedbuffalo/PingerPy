# PingerPy
A python version of the Host Pinger exe 

When looking into the Smartthings HostPinger Smartapp I wanted a way to be able to run it without having to use a windows machine or any fancy programs to run the EXE file from linux or mac.
This is where PingerPy came from - a python version of the Host Pinger EXE.
Once configured this will work with the Host Pinger Smartapp to display the server status of configured hosts.

## Details
The PingerPy application is made up of 2 parts:
1. PingerPy - main module
2. PingerPy - web server
The PingerPy web server allows you to configure the installation without having to manually edit the config file
You will be able to add hosts, and set the configuration through the web server URL

## Installation
Installation should be fairly easy. The only requirement is that the system is running python 2.7
1. Copy the directory to your computer
2. Make runonce.sh executable 'chmod u+x runonce.sh'
3. Execute runonce.sh './runonce.sh'
4. Now you can run the main program with './run.sh'

*Runonce is used to set the permissions values for all the other executable files, once complete run.sh initiates the actual pinger and web server.

