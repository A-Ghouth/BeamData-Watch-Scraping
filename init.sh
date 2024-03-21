
# Install Docker
sudo apt-get update
sudo apt-get upgrade
sudo apt-get remove docker docker-engine docker.io

sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Install/update aws CLI 
sudo snap install aws-cli --classic

# Change permissions on the Docker socket file
# Note: can be changed to be more restrictive
sudo chmod 777 /var/run/docker.sock

# Source the .env file to load environment variables
source "$(dirname "$0")/.env"

# Configure AWS S3 information
aws configure set aws_access_key_id "$ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$SECRET_KEY" 
aws configure set region "$LOCATION" 
aws configure set output "json"