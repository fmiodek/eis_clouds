#!/bin/bash
sleep 20
./connect.py &
./frontend_comm.py &
./frontend_server.py &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --kiosk "http://localhost:8000/scores.html" &

