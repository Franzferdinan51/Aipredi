#!/bin/bash

# Log file for the script
LOG_FILE="run_all_scripts.log"
exec > >(tee -i "$LOG_FILE")
exec 2>&1

# Open terminal window
gnome-terminal --tab --title="Run All Scripts" -- bash -c "
echo 'Starting run_all_scripts.sh'
echo '-----------------------------------'

# Run AI training script
echo 'Starting AI training script'
gnome-terminal --tab --title='AI Training' --command='python3 aipred.py | tee aipred.log'

# Wait for AI training script to start
while [ ! -f 'aipred.log' ]
do
  sleep 1
done

# Check if AI training script started properly
if grep -q 'Training progress' aipred.log; then
  echo 'AI Training script started successfully'
else
  echo 'AI Training script failed to start'
  exit 1
fi

# Run website monitoring script
echo 'Starting website monitoring script'
gnome-terminal --tab --title='Website Monitoring' --command='python3 website_monitor.py | tee website_monitor.log'

# Wait for website monitoring script to start
while [ ! -f 'website_monitor.log' ]
do
  sleep 1
done

# Check if website monitoring script started properly
if grep -q 'Website is' website_monitor.log; then
  echo 'Website Monitoring script started successfully'
else
  echo 'Website Monitoring script failed to start'
  exit 1
fi

# Run CLI script
echo 'Starting CLI script'
gnome-terminal --tab --title='CLI' --command='python3 aipred_cli.py | tee aipred_cli.log'

# Wait for CLI script to start
while [ ! -f 'aipred_cli.log' ]
do
  sleep 1
done

# Check if CLI script started properly
if grep -q 'AI prediction' aipred_cli.log; then
  echo 'CLI script started successfully'
else
  echo 'CLI script failed to start'
  exit 1
fi

# Keep terminal open until user confirmation
echo 'Press Enter to close the terminal'
read
"

