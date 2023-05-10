#!/bin/bash

# Define colors for progress bars
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Open headless terminal with verbose logging
xvfb-run --server-args="-screen 0 1024x768x24" terminator -T "Script Logging" -e 'echo "Starting run_all_scripts.sh"; exec bash -i -l -c "set -vx; exec >/tmp/run_all_scripts.log 2>&1"'

# Run website monitoring script
echo -e "${YELLOW}Running website monitoring script...${NC}"
xvfb-run --server-args="-screen 0 1024x768x24" terminator -T "Website Monitoring" -e 'python3 website_monitor.py &> website_monitor.log' &
while [ ! -f "website_monitor.log" ]; do sleep 1; done
while read -r line; do echo "$line"; done < <(tail -f website_monitor.log | sed -u -e 's/^/[website_monitor] /')
if grep -q "Website is" website_monitor.log; then
  echo -e "${GREEN}Website Monitoring script started successfully${NC}"
else
  echo -e "${RED}Website Monitoring script failed to start${NC}"
  exit 1
fi

# Run CLI script
echo -e "${YELLOW}Running CLI script...${NC}"
xvfb-run --server-args="-screen 0 1024x768x24" terminator -T "CLI" -e 'python3 aipred_cli.py &> aipred_cli.log' &
while [ ! -f "aipred_cli.log" ]; do sleep 1; done
while read -r line; do echo "$line"; done < <(tail -f aipred_cli.log | sed -u -e 's/^/[aipred_cli] /')
if grep -q "AI prediction" aipred_cli.log; then
  echo -e "${GREEN}CLI script started successfully${NC}"
else
  echo -e "${RED}CLI script failed to start${NC}"
  exit 2
fi

# Wait for a few seconds before starting AI training script
echo -e "${YELLOW}Waiting for 10 seconds before starting AI training script...${NC}"
sleep 10

# Run AI training script
echo -e "${YELLOW}Running AI training script...${NC}"
xvfb-run --server-args="-screen 0 1024x768x24" terminator -T "AI Training" -e 'python3 aipred.py &> aipred.log' &
while [ ! -f "aipred.log" ]; do sleep 1; done
while read -r line; do echo "$line"; done < <(tail -f aipred.log | sed -u -e 's/^/[aipred] /')
if grep -q "Training progress" aipred.log; then
  echo -e "${GREEN}AI Training script started successfully${NC}"
else
  echo -e "${RED}AI Training script failed to start${NC}"
  exit 3
fi

# Keep terminal open until user confirmation
echo ""
echo -e "${GREEN}All scripts have started successfully!${NC}"
echo ""
echo -

