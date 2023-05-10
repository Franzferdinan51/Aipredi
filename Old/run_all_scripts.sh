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
xvfb-run --server-args="-screen 0 1024x768x24" terminator -T "Website Monitoring" -e 'python3 website_monitor.py 2>&1 | tee -va website_monitor.log'
while [ ! -f "website_monitor.log" ]; do sleep 1; done
if grep -q "Website is" website_monitor.log; then
  echo -e "${GREEN}Website Monitoring script started successfully${NC}"
else
  echo -e "${RED}Website Monitoring script failed to start${NC}"
  exit 1
fi

# Run CLI script
echo -e "${YELLOW}Running CLI script...${NC}"
xvfb-run --server-args="-screen 0 1024x768x24" terminator -T "CLI" -e 'python3 aipred_cli.py 2>&1 | tee -va aipred_cli.log'
while [ ! -f "aipred_cli.log" ]; do sleep 1; done
if grep -q "AI prediction" aipred_cli.log; then
  echo -e "${GREEN}CLI script started successfully${NC}"
else
  echo -e "${RED}CLI script failed to start${NC}"
  exit 1
fi

# Wait for a few seconds before starting AI training script
echo -e "${YELLOW}Waiting for 10 seconds before starting AI training script...${NC}"
sleep 10

# Run AI training script
echo -e "${YELLOW}Running AI training script...${NC}"
xvfb-run --server-args="-screen 0 1024x768x24" terminator -T "AI Training" -e 'python3 aipred.py 2>&1 | tee -va aipred.log'
while [ ! -f "aipred.log" ]; do sleep 1; done
if grep -q "Training progress" aipred.log; then
  echo -e "${GREEN}AI Training script started successfully${NC}"
else
  echo -e "${RED}AI Training script failed to start${NC}"
  exit 1
fi

# Keep terminal open until user confirmation
echo ""
echo -e "${GREEN}All scripts have started successfully!${NC}"
echo ""
echo -e "${YELLOW}Press Enter to close the terminal${NC}"
read -p ""


#!/bin/bash

# Define error codes and definitions
declare -A ERROR_CODES=(
  [1]="Website Monitoring script failed to start"
  [2]="CLI script failed to start"
  [3]="AI Training script failed to start"
)

# Create error code file
echo "Error Codes:" > error_codes.txt
for code in "${!ERROR_CODES[@]}"; do
  echo -e "${code}\t${ERROR_CODES[$code]}" >> error_codes.txt
done

# Check for errors and create error files
if grep -q "ERROR" website_monitor.log; then
  echo -e "Website Monitoring script failed with error: $(grep -m1 'ERROR' website_monitor.log | cut -d ':' -f 2)" >&2
  exit 1
fi

if grep -q "ERROR" aipred_cli.log; then
  echo -e "CLI script failed with error: $(grep -m1 'ERROR' aipred_cli.log | cut -d ':' -f 2)" >&2
  exit 2
fi

if grep -q "ERROR" aipred.log; then
  echo -e "AI Training script failed with error: $(grep -m1 'ERROR' aipred.log | cut -d ':' -f 2)" >&2
  exit 3
fi

exit 0
