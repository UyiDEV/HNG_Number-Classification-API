# Steps to Deploy on EC2:

### Launch an EC2 Instance:

1. Choose a Linux AMI.
2. Select an appropriate instance type (t2.micro).
3. Configure security groups to allow inbound HTTP traffic (port 80) and SSH (port 22).
4. Connect to your EC2 Instance: Use SSH to connect to your instance.

### Install Python and Dependencies:

```bash
sudo apt update -y  # Update system packages
sudo apt install python3.12-venv  # Create a virtual environment
```

You can clone your GitHub repository and change into it, then activate virtual environment.

```bash
python3 -m venv venv 
pip install -r requirements.txt # Install dependencies
```

### Create a WSGI file (wsgi.py):
```bash
touch wsgi.py
```
```Python
from app import app  # Replace app with your Flask app's name

if __name__ == "__main__":
    app.run()
```

Run with Gunicorn (Recommended for Production):
```Bash
gunicorn --bind :8000 wsgi:app  # Run Gunicorn on port 8000
```
You could run this in the background using `nohup` or `screen` so it continues to run after you disconnect from SSH.

Configure a Reverse Proxy (Nginx or Apache): `sudo apt install nignx -y`

A reverse proxy is highly recommended for production.  It handles static files, load balancing, and more.  Here's a basic Nginx configuration example:
```Nginx
server {
    listen 80;
    server_name your_ec2_public_ip_or_dns;  # Replace with your EC2 instance's public IP or DNS

    location / {
        proxy_pass http://127.0.0.1:8000;  # Forward requests to Gunicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
Place this configuration in /etc/nginx/conf.d/your_app.conf and restart Nginx: 
```bash
sudo systemctl restart nginx.
```

Get your EC2 Public IP or DNS: You can find this in the EC2 console. Use this to access your API: http://54.235.25.225/api/classify-number?number=371
