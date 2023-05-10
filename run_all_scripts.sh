#!/bin/bash

# Define timestamp function
timestamp() {
  date +"%Y-%m-%d %T"
}

# Check if programs related to this script are running, and kill them
echo "$(timestamp) - Checking for running programs..."
if pgrep -f "Xvfb :99" >/dev/null; then
  echo "$(timestamp) - Killing Xvfb virtual display server..."
  pkill -f "Xvfb :99"
  sleep 2
fi
if pgrep -f "website_monitor.py" >/dev/null; then
  echo "$(timestamp) - Killing website monitoring script..."
  pkill -f "website_monitor.py"
  sleep 2
fi
if pgrep -f "BitPredictor.py" >/dev/null; then
  echo "$(timestamp) - Killing BitPredictor script..."
  pkill -f "BitPredictor.py"
  sleep 2
fi
if pgrep -f "webserver.py" >/dev/null; then
  echo "$(timestamp) - Killing website script..."
  pkill -f "webserver.py"
  sleep 2
fi
if pgrep -f "PriceUpdater.py" >/dev/null; then
  echo "$(timestamp) - Killing PriceUpdater script..."
  pkill -f "PriceUpdater.py"
  sleep 2
fi
echo "$(timestamp) - All related programs killed"
echo

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
STAGE3=20
STAGE4=20
STAGE5=10
TOTAL=$(( STAGE1 + STAGE2 + STAGE3 + STAGE4 + STAGE5 ))

# Start progress bar for the whole process
progressBar "${TOTAL}" &

# Stage 1: Start Xvfb virtual display server
echo "$(timestamp) - Starting Xvfb virtual display server..."
Xvfb :99 -screen 0 1024x768x24 &
sleep 2
if ! pgrep -f "Xvfb :99" >/dev/null; then
  ERROR="$(timestamp) - Failed to start Xvfb virtual display server"
  echo "${ERROR}"
  echo "${ERROR}" >> runallscripts.log
  exit 1
fi
echo "$(timestamp) - Xvfb virtual display server started"
((CURRENT += STAGE1))
printf "\n\n"

# Stage 2: Run BitPredictor script
echo "$(timestamp) - Running BitPredictor script..."
python3 BitPredictor.py &> BitPredictor.log &
sleep 10
if ! grep -q "BitPredictor started successfully" BitPredictor.log; then
  ERROR="$(timestamp) - BitPredictor script failed to start"
  echo "${ERROR}"
  echo "${ERROR}" >> runallscripts.log
  exit 2
fi
echo "$(timestamp) - BitPredictor script started successfully"
((CURRENT += STAGE2))
printf "\n\n"

# Stage 3: Run PriceUpdater script
echo "$(timestamp) - Running PriceUpdater script..."
python3 PriceUpdater.py &> PriceUpdater.log &
sleep 10
if ! grep -q "PriceUpdater started successfully" PriceUpdater.log; then
  ERROR="$(timestamp) - PriceUpdater script failed to start"
  echo "${ERROR}"
  echo "${ERROR}" >> runallscripts.log
  exit 3
fi
echo "$(timestamp) - PriceUpdater script started successfully"
((CURRENT += STAGE3))
printf "\n\n"

# Stage 4: Run website monitoring script
echo "$(timestamp) - Running website monitoring script..."
python3 website_monitor.py &> website_monitor.log &
sleep 10
if grep -q "Website monitoring started successfully" website_monitor.log; then
  echo "$(timestamp) - Website monitoring script started successfully"
else
  ERROR="$(timestamp) - Website monitoring script failed to start"
  echo "${ERROR}"
  echo "${ERROR}" >> runallscripts.log
  exit 4
fi
((CURRENT += STAGE4))
printf "\n\n"

echo "$(timestamp) - All scripts started successfully"
