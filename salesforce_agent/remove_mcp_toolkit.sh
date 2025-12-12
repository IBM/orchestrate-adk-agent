#!/usr/bin/env bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🗑️  Tavily MCP Toolkit Removal Script${NC}"
echo "========================================"

# Get script directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if we're in the correct environment
echo -e "${YELLOW}Checking orchestrate environment...${NC}"
if ! command -v orchestrate &> /dev/null; then
    echo -e "${RED}❌ Error: orchestrate command not found. Please make sure you have the ADK installed.${NC}"
    exit 1
fi

# Activate the environment
ENVIRONMENT_NAME=${1:-"local"}
echo -e "${YELLOW}Activating environment: ${ENVIRONMENT_NAME}${NC}"
orchestrate env activate ${ENVIRONMENT_NAME}

# Remove the MCP toolkit
echo -e "${YELLOW}Removing Tavily MCP toolkit...${NC}"
orchestrate toolkits remove --name tavily_mcp_server

# Optionally remove the connection
echo -e "${YELLOW}Removing Tavily connection...${NC}"
orchestrate connections remove -a tavily_creds || true

echo -e "${GREEN}✅ Tavily MCP toolkit removed successfully!${NC}"
