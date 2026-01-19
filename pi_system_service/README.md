# Pi Axera SD Interactive System Service Setup

This directory contains files to set up the Pi Axera SD Interactive application as a system service on Raspberry Pi.

## Files

- `pi_axera_sd_interactive.service`: Systemd service file template (with placeholders)
- `start_service.sh`: Script to start the application with proper environment
- `install_service.sh`: Installation script that automatically detects paths and user

## Prerequisites

1. The application code is in the current directory (run install from project root)
2. Python virtual environment is set up at `./.venv`
3. All dependencies are installed in the virtual environment
4. Run the install script as the user who owns the project directory

## Installation

1. Navigate to the project root directory
2. Run the install script (as the project owner, not root):

   ```bash
   ./pi_system_service/install_service.sh
   ```

   The script will:
   - Detect the current user and project path
   - Generate the service file with correct paths
   - Install and enable the systemd service

## Service Management

- Start service: `sudo systemctl start pi_axera_sd_interactive`
- Stop service: `sudo systemctl stop pi_axera_sd_interactive`
- Restart service: `sudo systemctl restart pi_axera_sd_interactive`
- Check status: `sudo systemctl status pi_axera_sd_interactive`
- View logs: `sudo journalctl -u pi_axera_sd_interactive -f`
- Enable auto-start: `sudo systemctl enable pi_axera_sd_interactive`
- Disable auto-start: `sudo systemctl disable pi_axera_sd_interactive`

## Notes

- The application will be accessible at `http://raspberry-pi-ip:7860` (default Gradio port)
- The service will automatically restart if it crashes
- Logs can be viewed using journalctl
- The service runs as the user who installed it