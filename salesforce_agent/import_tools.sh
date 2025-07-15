#!/usr/bin/env bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Salesforce Tools Import Script${NC}"
echo "===================================="

# Get script directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if we're in the correct environment
echo -e "${YELLOW}Checking orchestrate environment...${NC}"
if ! command -v orchestrate &> /dev/null; then
    echo -e "${RED}❌ Error: orchestrate command not found. Please make sure you have the ADK installed.${NC}"
    exit 1
fi

# Activate the environment (you can change this to your preferred environment)
ENVIRONMENT_NAME=${1:-"challenge"}
echo -e "${YELLOW}Activating environment: ${ENVIRONMENT_NAME}${NC}"
orchestrate env activate ${ENVIRONMENT_NAME}

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r "${SCRIPT_DIR}/requirements.txt"

# # Import the connection (if it exists)
# if [ -f "${SCRIPT_DIR}/connections/salesforce_connection.yaml" ]; then
#     echo -e "${YELLOW}Importing Salesforce connection...${NC}"
#     orchestrate connections import --file "${SCRIPT_DIR}/connections/salesforce_connection.yaml"
# fi

# Import the tools with connection association
echo -e "${YELLOW}Importing Salesforce tools...${NC}"
orchestrate tools import -k python -f "${SCRIPT_DIR}/tools/salesforce_tools.py" -r "${SCRIPT_DIR}/requirements.txt" --app-id salesforce_creds

echo -e "${GREEN}✅ Salesforce tools imported successfully!${NC}"
echo ""
echo -e "${GREEN}📋 Next steps:${NC}"
echo "1. Run './setup_connection.sh' to configure your Salesforce credentials"
echo "2. Run './import_agent.sh' to import the agent"
echo "3. Test with: orchestrate playground"
echo ""
echo -e "${YELLOW}Note: If you haven't set up the connection yet, run './setup_connection.sh' first.${NC}"
