#!/bin/bash

# Define progress bar function
progressBar() {
  local duration=${1}
  local columns=$(tput cols)
  local space=$(( columns - 15 ))
  local fill=$(printf "%${space}s" | tr ' ' '#')
  local EMPTY=$(printf "%${space}s" | tr ' ' ' ')

  printf "\n"
  for (( i=0; i<=$duration; i++ )); do
    local percentage=$(( 100 * i / duration ))
    local fillLength=$(( space * i / duration ))
    local emptyLength=$(( space - fillLength ))
    printf "\r[%-${space}s] %d%%" "${fill:0:fillLength}${EMPTY:0:emptyLength}" "${percentage}"
    sleep 1
  done
  printf "\n\n"
}

# Define script stages and their percentage of total progress
STAGE1=20
STAGE2=30
STAGE3=40
STAGE4=10
TOTAL=$(( STAGE1 + STAGE2 + STAGE3 + STAGE4 ))

# Start progress bar for the whole process
progressBar "${TOTAL}" &

# Stage 1: Start Xvfb virtual display server
echo "Starting Xvfb virtual display server..."
Xvfb :99 -screen 0 1024x768x24 &
sleep 2
echo "Xvfb virtual display server started"
((CURRENT += STAGE1))
printf "\n\n"

# Stage 2: Run BitPredictor script
echo "Running BitPredictor script..."
python3 BitPredictor.py &> BitPredictor.log &
sleep 10
if grep -q "BitPredictor started successfully" BitPredictor.log; then
  echo "BitPredictor script started successfully"
else
  echo "BitPredictor script failed to start"
  echo "BitPredictor script failed to start" >> runallscripts.log
  exit 2
fi
((CURRENT += STAGE2))
printf "\n\n"

# Stage 3: Run website script
echo "Running website script..."
python3 website.py &> website.log &
sleep 10
if grep -q "Starting server" website.log; then
  echo "Website script started successfully"
else
  echo "Website script failed to start"
  echo "Website script failed to start" >> runallscripts.log
  exit 3
fi
((CURRENT += STAGE3))
printf "\n\n"

# Stage 4: Run website monitoring script
echo "Running website monitoring script..."
python3 website_monitor.py &> website_monitor.log &
sleep 10
if grep -q "Website is" website_monitor.log; then
  echo "Website monitoring script started successfully"
else
  echo "Website monitoring script failed to start"
  echo "Website monitoring script failed to start" >> runallscripts.log
  exit 1
fi
((CURRENT += STAGE4))
printf "\n\n"

# Finish progress bar
printf "Overall progress: %d%%\n" 100
wait

# Prompt user before exiting
read -p "Press any key to exit"

# End of script

