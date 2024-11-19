#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# -------------------------------
# Configuration Variables
# -------------------------------
DOCKER_COMPOSE_DIR="."
FRONTEND_PORT=9598
BACKEND_PORT=9599
STATIC_IP="192.168.1.100/24"  # <-- Modify as needed
GATEWAY_IP="192.168.1.1"       # <-- Modify as needed
DNS_SERVERS="8.8.8.8,8.8.4.4"   # <-- Modify as needed

# -------------------------------
# Function Definitions
# -------------------------------

# Function to print messages
print_message() {
    echo "============================================================"
    echo "$1"
    echo "============================================================"
}

# Function to install Docker
install_docker() {
    print_message "Installing Docker..."

    sudo apt update
    sudo apt install -y ca-certificates curl gnupg lsb-release

    # Add Docker’s official GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    # Set up the Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker Engine and Docker Compose plugin
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Verify installation
    docker --version
    docker compose version

    print_message "Docker installation completed."
}

# Function to add current user to Docker group
add_user_to_docker_group() {
    print_message "Adding user '$USER' to the 'docker' group..."

    sudo usermod -aG docker $USER

    echo "User '$USER' added to the 'docker' group. Please log out and log back in for the changes to take effect."

    print_message "User group update completed."
}

# Function to configure UFW firewall
configure_firewall() {
    print_message "Configuring UFW firewall..."

    # Install UFW if not installed
    sudo apt install -y ufw

    # Allow SSH if not already allowed to prevent locking out
    sudo ufw allow OpenSSH

    # Allow frontend and backend ports
    sudo ufw allow $FRONTEND_PORT/tcp
    sudo ufw allow $BACKEND_PORT/tcp

    # Enable UFW
    sudo ufw --force enable

    # Reload UFW to apply changes
    sudo ufw reload

    # Display UFW status
    sudo ufw status verbose

    print_message "UFW firewall configuration completed."
}

# Function to set a static IP (Optional)
set_static_ip() {
    read -p "Would you like to configure a static IP address? [y/N]: " response
    response=${response,,} # tolower

    if [[ "$response" =~ ^(yes|y)$ ]]; then
        print_message "Configuring static IP..."

        # Identify active network interface
        INTERFACE=$(ip -o -4 route show default | awk '{print $5}')
        echo "Detected network interface: $INTERFACE"

        CONFIG_FILE="/etc/netplan/02-static-ip.yaml"

        # Backup existing netplan config
        sudo cp /etc/netplan/*.yaml /etc/netplan/backup-before-static-ip.yaml

        # Create a new netplan configuration file
        sudo bash -c "cat > $CONFIG_FILE" <<EOL
network:
  version: 2
  renderer: networkd
  ethernets:
    $INTERFACE:
      dhcp4: no
      addresses:
        - $STATIC_IP
      gateway4: $GATEWAY_IP
      nameservers:
        addresses: [$DNS_SERVERS]
EOL

        # Apply netplan configuration
        sudo netplan apply

        # Verify IP address
        CURRENT_IP=$(ip -o -4 addr show $INTERFACE | awk '{print \$4}' | cut -d/ -f1)
        echo "Static IP configured: $CURRENT_IP"

        print_message "Static IP configuration completed."
    else
        echo "Skipping static IP configuration."
    fi
}

# Function to deploy Docker Compose services
deploy_docker_compose() {
    print_message "Deploying Docker Compose services..."

    if [ ! -f "$DOCKER_COMPOSE_DIR/docker-compose.yml" ]; then
        echo "Error: docker-compose.yml not found in $DOCKER_COMPOSE_DIR"
        exit 1
    fi

    cd "$DOCKER_COMPOSE_DIR"

    # Pull latest images (optional)
    # docker compose pull

    # Build and start containers
    docker compose up -d

    # Display running containers
    docker ps

    print_message "Docker Compose services deployed successfully."
}

# Function to display usage
usage() {
    echo "Usage: sudo bash setup_kratos_docker.sh"
    exit 1
}

# -------------------------------
# Main Script Execution
# -------------------------------

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or use sudo."
    usage
fi

# Check if Docker is already installed
if ! command -v docker &> /dev/null
then
    install_docker
else
    echo "Docker is already installed. Skipping Docker installation."
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null
then
    echo "Docker Compose is not installed."
    install_docker
else
    echo "Docker Compose is already installed. Skipping Docker Compose installation."
fi

# Add user to Docker group (if not already a member)
if groups $SUDO_USER | grep &>/dev/null '\bdocker\b'; then
    echo "User '$SUDO_USER' is already in the 'docker' group."
else
    add_user_to_docker_group
fi

# Configure UFW firewall
configure_firewall

# Optional: Set static IP
set_static_ip

# Deploy Docker Compose services
deploy_docker_compose

print_message "Setup completed successfully!"

echo "================================================================"
echo "You may need to log out and log back in for group changes to take effect."
echo "Access your application at http://<Your_Ubuntu_IP>:$FRONTEND_PORT/"
echo "================================================================"