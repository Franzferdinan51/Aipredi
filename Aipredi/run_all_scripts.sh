#!/bin/bash

# Define colors for progress bars
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Open terminal with verbose logging
gnome-terminal --tab --title="Script Logging" -- bash -c 'echo "Starting run_all_scripts.sh"; exec bash -i -l -c "set -vx; exec >/tmp/run_all_scripts.log 2>&1"'

# Run AI training script
echo -e "${YELLOW}Running AI training script...${NC}"
gnome-terminal --tab --title="AI Training" -- bash -c 'python3 aipred.py 2>&1 | tee -va aipred.log'
while [ ! -f "aipred.log" ]; do sleep 1; done
if grep -q "Training progress" aipred.log; then
  echo -e "${GREEN}AI Training script started successfully${NC}"
else
  echo -e "${RED}AI Training script failed to start${NC}"
  exit 1
fi

# Run website monitoring script
echo -e "${YELLOW}Running website monitoring script...${NC}"
gnome-terminal --tab --title="Website Monitoring" -- bash -c 'python3 website_monitor.py 2>&1 | tee -va website_monitor.log'
while [ ! -f "website_monitor.log" ]; do sleep 1; done
if grep -q "Website is" website_monitor.log; then
  echo -e "${GREEN}Website Monitoring script started successfully${NC}"
else
  echo -e "${RED}Website Monitoring script failed to start${NC}"
  exit 1
fi

# Run CLI script
echo -e "${YELLOW}Running CLI script...${NC}"
gnome-terminal --tab --title="CLI" -- bash -c 'python3 aipred_cli.py 2>&1 | tee -va aipred_cli.log'
while [ ! -f "aipred_cli.log" ]; do sleep 1; done
if grep -q "AI prediction" aipred_cli.log; then
  echo -e "${GREEN}CLI script started successfully${NC}"
else
  echo -e "${RED}CLI script failed to start${NC}"
  exit 1
fi

# Keep terminal open until user confirmation
echo ""
echo -e "${GREEN}All scripts have started successfully!${NC}"
echo ""
echo -e "${YELLOW}Press Enter to close the terminal${NC}"
read -p ""
