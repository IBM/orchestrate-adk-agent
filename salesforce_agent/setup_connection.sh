#!/bin/bash

# Import and configure Salesforce connection for orchestrate
echo "Importing Salesforce connection..."

# Check if we're already in the salesforce_agent directory
if [ ! -f "connections/salesforce_connection.yaml" ]; then
    echo "Error: connections/salesforce_connection.yaml not found. Make sure you're in the salesforce_agent directory."
    exit 1
fi

# Import the connection configuration
echo "Importing connection configuration..."
orchestrate connections add -a salesforce_creds

# Configure the connection
echo "Configuring Salesforce connection..."
orchestrate connections configure -a salesforce_creds --env draft --kind key_value --type team
orchestrate connections configure -a salesforce_creds --env live --kind key_value --type team

# Set credentials for the connection
echo "Setting connection credentials..."
echo "You will be prompted to enter your Salesforce credentials:"
echo "1. SF_USERNAME - Your Salesforce username"
echo "2. SF_PASSWORD - Your Salesforce password"
echo "3. SF_SECURITY_TOKEN - Your Salesforce security token (get from Setup > My Personal Information > Reset Security Token)"
echo "4. SF_DOMAIN - 'login' for production, 'test' for sandbox (optional, defaults to 'login')"
echo ""

# Prompt for credentials
read -p "Enter your Salesforce username: " username
read -s -p "Enter your Salesforce password: " password
echo ""
read -s -p "Enter your Salesforce security token: " token
echo ""
read -p "Enter your Salesforce domain (login/test) [default: login]: " domain
domain=${domain:-test}

# Set the credentials using orchestrate CLI for draft environment
echo "Setting credentials for draft environment..."
orchestrate connections set-credentials --app-id salesforce_creds --env draft -e SF_USERNAME="$username" -e SF_PASSWORD="$password" -e SF_SECURITY_TOKEN="$token" -e SF_DOMAIN="$domain"  
# orchestrate connections set-credentials create --app-id salesforce_creds --env draft -e SF_PASSWORD="$password"
# orchestrate connections set-credentials create --app-id salesforce_creds --env draft -e SF_SECURITY_TOKEN="$token"
# orchestrate connections set-credentials create --app-id salesforce_creds --env draft -e SF_DOMAIN="$domain"

# Also set credentials for live environment (for production deployment)
echo "Setting credentials for live environment..."
orchestrate connections set-credentials --app-id salesforce_creds --env live -e SF_USERNAME="$username" -e SF_PASSWORD="$password" -e SF_SECURITY_TOKEN="$token" -e SF_DOMAIN="$domain"
# orchestrate connections set-credentials create --app-id salesforce_creds --env live -e SF_PASSWORD="$password"
# orchestrate connections set-credentials create --app-id salesforce_creds --env live -e SF_SECURITY_TOKEN="$token"
# orchestrate connections set-credentials create --app-id salesforce_creds --env live -e SF_DOMAIN="$domain"

echo "Connection credentials set successfully!"
echo "Connection is ready to use with your Salesforce tools."
