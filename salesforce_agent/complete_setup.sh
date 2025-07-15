#!/bin/bash

# Complete Salesforce Agent Setup Script
# This script handles the entire setup process for the Salesforce agent

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Salesforce Agent Complete Setup${NC}"
echo "===================================="

# Check if we're in the correct environment
if ! command -v orchestrate &> /dev/null; then
    echo -e "${RED}❌ Error: orchestrate command not found. Please make sure you have the ADK installed.${NC}"
    exit 1
fi

# Activate the environment
ENVIRONMENT_NAME=${1:-"challenge"}
echo -e "${YELLOW}Using environment: ${ENVIRONMENT_NAME}${NC}"
orchestrate env activate ${ENVIRONMENT_NAME}

echo -e "${YELLOW}Step 1: Checking environment...${NC}"
# Get the script directory and navigate to it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if we're in the right place
if [ ! -f "connections/salesforce_connection.yaml" ]; then
    echo -e "${RED}❌ Error: Not in the correct directory. Expected to be in salesforce_agent directory.${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 2: Importing agent and tools...${NC}"
./import_agent.sh ${ENVIRONMENT_NAME}

echo -e "${YELLOW}Step 3: Setting up connection...${NC}"
echo "Do you want to set up the Salesforce connection with your credentials? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    ./setup_connection.sh
else
    echo -e "${YELLOW}⚠️  Skipping connection setup. You can run ./setup_connection.sh later${NC}"
fi

echo -e "${YELLOW}Step 4: Testing setup...${NC}"
./test_agent.sh ${ENVIRONMENT_NAME}

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "- ✅ Agent imported: salesforce_agent"
echo "- ✅ Tools imported with connection association"
echo "- ✅ Connection configured (if selected)"
echo ""
echo -e "${BLUE}🎮 Next steps:${NC}"
echo "1. Test the agent: orchestrate playground"
echo "2. Check connection status: ./check_connection.sh"
echo "3. View examples: cat examples.py"
echo ""
echo -e "${YELLOW}Need help? Check the README.md for detailed usage instructions.${NC}"
