#!/bin/bash

# Install script for Pi Axera SD Interactive System Service
# Run this as root or with sudo from the project root directory

echo "Installing Pi Axera SD Interactive as a system service..."

# Get the current user (who should own the project)
CURRENT_USER=$(whoami)
if [ "$CURRENT_USER" = "root" ]; then
    echo "Please run this script as the user who owns the project directory, not as root."
    echo "The service will be configured to run as that user."
    exit 1
fi

# Get the absolute path to the project directory
PROJECT_DIR=$(pwd)

echo "Installing for user: $CURRENT_USER"
echo "Project directory: $PROJECT_DIR"

# Create a temporary service file with replaced placeholders
TEMP_SERVICE="/tmp/pi_axera_sd_interactive.service"
cp pi_system_service/pi_axera_sd_interactive.service "$TEMP_SERVICE"
sed -i "s|@USER@|$CURRENT_USER|g" "$TEMP_SERVICE"
sed -i "s|@PROJECT_DIR@|$PROJECT_DIR|g" "$TEMP_SERVICE"

# Copy the service file to systemd
sudo cp "$TEMP_SERVICE" /etc/systemd/system/pi_axera_sd_interactive.service

# Clean up temp file
rm "$TEMP_SERVICE"

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable pi_axera_sd_interactive

# Start the service
sudo systemctl start pi_axera_sd_interactive

echo "Service installed and started."
echo "Check status with: sudo systemctl status pi_axera_sd_interactive"
echo "View logs with: sudo journalctl -u pi_axera_sd_interactive -f"