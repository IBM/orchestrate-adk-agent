#!/usr/bin/env bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Atlassian MCP Server Import Script${NC}"
echo "========================================"

# Get script directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if we're in the correct environment
echo -e "${YELLOW}Checking orchestrate environment...${NC}"
if ! command -v orchestrate &> /dev/null; then
    echo -e "${RED}❌ Error: orchestrate command not found. Please make sure you have the ADK installed.${NC}"
    exit 1
fi

# Check if uvx is available
echo -e "${YELLOW}Checking uvx availability...${NC}"
if ! command -v uvx &> /dev/null; then
    echo -e "${RED}❌ Error: uvx command not found. Please install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    exit 1
fi

# Activate the environment (you can change this to your preferred environment)
ENVIRONMENT_NAME=${1:-"local"}
echo -e "${YELLOW}Activating environment: ${ENVIRONMENT_NAME}${NC}"
orchestrate env activate ${ENVIRONMENT_NAME}

# Jira URL (configure as needed)
JIRA_URL="https://jsw.ibm.com"

# Prompt for Jira username
if [ -z "$JIRA_USERNAME" ]; then
    echo -e "${YELLOW}Enter your Jira username (email):${NC}"
    read JIRA_USER
else
    JIRA_USER=$JIRA_USERNAME
fi

# Prompt for Jira personal token
if [ -z "$JIRA_PERSONAL_TOKEN" ]; then
    echo -e "${YELLOW}Enter your Jira Personal Access Token:${NC}"
    read -s JIRA_TOKEN
    echo ""
else
    JIRA_TOKEN=$JIRA_PERSONAL_TOKEN
fi

# Setup connection for Atlassian credentials
echo -e "${YELLOW}Setting up Atlassian connection...${NC}"

# Add connection (will fail if already exists, that's ok)
orchestrate connections add -a atlassian_creds || echo -e "${YELLOW}Connection 'atlassian_creds' already exists, updating...${NC}"

# Configure for draft environment only (local development only supports draft)
orchestrate connections configure -a atlassian_creds --env draft --type team --kind key_value || true
orchestrate connections set-credentials -a atlassian_creds --env draft -e "JIRA_USERNAME=$JIRA_USER" -e "JIRA_PERSONAL_TOKEN=$JIRA_TOKEN"

# Import the MCP toolkit using CLI command
echo -e "${YELLOW}Importing Atlassian MCP toolkit...${NC}"
orchestrate toolkits add \
    --kind mcp \
    --name atlassian_mcp_server \
    --description "Atlassian MCP Server for Jira integration - query issues, create tickets, manage projects" \
    --command '["uvx", "mcp-atlassian", "--jira-url='"$JIRA_URL"'", "--jira-username=${JIRA_USERNAME}", "--jira-personal-token=${JIRA_PERSONAL_TOKEN}"]' \
    --tools "*" \
    --app-id atlassian_creds

echo -e "${GREEN}✅ Atlassian MCP toolkit imported successfully!${NC}"
echo ""
echo -e "${GREEN}📋 Available commands:${NC}"
echo "  - List toolkits: orchestrate toolkits list"
echo "  - Test in playground: orchestrate playground"
echo ""
echo -e "${YELLOW}Note: The MCP server will be started automatically when tools are invoked.${NC}"
