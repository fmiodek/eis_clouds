#!/bin/bash
sleep 20
python3 connect.py &
python3 frontend_comm.py &
python3 frontend_server.py &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --kiosk "http://localhost:8000/scores.html" &

