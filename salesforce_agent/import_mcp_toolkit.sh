#!/usr/bin/env bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Tavily MCP Server Import Script${NC}"
echo "====================================="

# Get script directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if we're in the correct environment
echo -e "${YELLOW}Checking orchestrate environment...${NC}"
if ! command -v orchestrate &> /dev/null; then
    echo -e "${RED}❌ Error: orchestrate command not found. Please make sure you have the ADK installed.${NC}"
    exit 1
fi

# Check if npx is available
echo -e "${YELLOW}Checking npx availability...${NC}"
if ! command -v npx &> /dev/null; then
    echo -e "${RED}❌ Error: npx command not found. Please install Node.js first.${NC}"
    exit 1
fi

# Activate the environment (you can change this to your preferred environment)
ENVIRONMENT_NAME=${1:-"local"}
echo -e "${YELLOW}Activating environment: ${ENVIRONMENT_NAME}${NC}"
orchestrate env activate ${ENVIRONMENT_NAME}

# Setup connection for Tavily API key
echo -e "${YELLOW}Setting up Tavily connection...${NC}"

# Add connection (will fail if already exists, that's ok)
orchestrate connections add -a tavily_creds || echo -e "${YELLOW}Connection 'tavily_creds' already exists, updating...${NC}"

# Configure for draft environment only (local development only supports draft)
orchestrate connections configure -a tavily_creds --env draft --type team --kind key_value || true
orchestrate connections set-credentials -a tavily_creds --env draft -e <your-api-key-here>

# Import the MCP toolkit using CLI command
echo -e "${YELLOW}Importing Tavily MCP toolkit...${NC}"
orchestrate toolkits add \
    --kind mcp \
    --name tavily_mcp_server \
    --description "Tavily MCP Server for AI-powered web search and research capabilities" \
    --command '["npx", "-y", "tavily-mcp@latest"]' \
    --tools "*" \
    --app-id tavily_creds

echo -e "${GREEN}✅ Tavily MCP toolkit imported successfully!${NC}"
echo ""
echo -e "${GREEN}📋 Available commands:${NC}"
echo "  - List toolkits: orchestrate toolkits list"
echo "  - Test in playground: orchestrate playground"
echo ""
echo -e "${YELLOW}Note: The MCP server will be started automatically when tools are invoked.${NC}"
