# MIG Info Webapp

This project provides a simple Flask-based web application that displays metadata and Managed Instance Group (MIG) information from a Google Cloud VM instance. It is intended to be deployed on a VM that is part of a MIG in Google Cloud Platform.

## Features

- Retrieves and displays:
  - Private IP address of the instance
  - Hostname
  - Current target size of the associated MIG
- Uses Google Cloud Metadata server for instance-specific data
- Uses the Compute API to query MIG size
- Simple NGINX reverse proxy configuration
- Systemd service for process management

## Requirements

- Python 3
- Flask
- google-api-python-client
- google-auth
- NGINX
- Systemd
- Running inside a GCP Compute Engine instance with appropriate permissions (default service account with Compute Viewer role)

## File Overview

- `webapp.py`: Main Flask application
- `webapp.conf`: NGINX configuration for reverse proxy
- `webapp.service`: Systemd service file for managing the app

## Setup

1. Place the files in `/opt/webapp` (or another directory, adjust `WorkingDirectory` accordingly).
2. Install required Python packages:
   ```
   pip install flask google-api-python-client google-auth
   ```
3. Set up the systemd service:
   ```
   cp webapp.service /etc/systemd/system/
   systemctl daemon-reexec
   systemctl enable webapp
   systemctl start webapp
   ```
4. Deploy the NGINX configuration:
   ```
   cp webapp.conf /etc/nginx/sites-available/webapp
   ln -s /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/
   nginx -t
   systemctl reload nginx
   ```
5. Ensure the VM has access to the GCP metadata server and the necessary IAM permissions.

## Security Notes

- The application restricts access to `.git` paths via NGINX.
- No authentication is implemented; access should be limited by firewall or IAM controls if necessary.

## License

MIT License
