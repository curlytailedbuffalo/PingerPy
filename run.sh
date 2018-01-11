#!/bin/bash

echo "Starting PingerPy watchdog and webserver..."
cd main
python PingerPy &
cd ..
cd server
python PingerPy_web_server &
echo "Done!"
