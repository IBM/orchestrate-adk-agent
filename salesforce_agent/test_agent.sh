#!/usr/bin/env bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Salesforce Agent Test Script${NC}"
echo "=================================="

# Check if we're in the correct environment
if ! command -v orchestrate &> /dev/null; then
    echo -e "${RED}❌ Error: orchestrate command not found. Please make sure you have the ADK installed.${NC}"
    exit 1
fi

# Activate the environment
ENVIRONMENT_NAME=${1:-"challenge"}
echo -e "${YELLOW}Using environment: ${ENVIRONMENT_NAME}${NC}"
orchestrate env activate ${ENVIRONMENT_NAME}

echo -e "${YELLOW}Checking if agent exists...${NC}"
if orchestrate agents list | grep -q "salesforce_agent"; then
    echo -e "${GREEN}✅ Salesforce agent found${NC}"
else
    echo -e "${RED}❌ Salesforce agent not found. Please run ./import_agent.sh first${NC}"
    exit 1
fi

echo -e "${YELLOW}Checking connection status...${NC}"
if orchestrate connections list | grep -q "salesforce_creds"; then
    echo -e "${GREEN}✅ Salesforce connection found${NC}"
    
    # Test if connection has credentials
    if orchestrate connections describe --app-id salesforce_creds | grep -q "SF_USERNAME"; then
        echo -e "${GREEN}✅ Connection has credentials configured${NC}"
    else
        echo -e "${YELLOW}⚠️  Connection exists but credentials may not be set${NC}"
        echo -e "${YELLOW}   Run ./setup_connection.sh to configure credentials${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Connection not found - tools will use environment variables${NC}"
    echo -e "${YELLOW}   Run ./setup_connection.sh to create orchestrate connection${NC}"
fi

echo -e "${YELLOW}Checking if tools exist...${NC}"
TOOLS=(
    "salesforce_query"
    "salesforce_search"
    "salesforce_create_record"
    "salesforce_update_record"
    "salesforce_delete_record"
    "salesforce_get_record"
    "salesforce_describe_object"
    "salesforce_list_objects"
    "salesforce_upsert_record"
    "salesforce_bulk_create"
    "salesforce_get_recent_records"
    "salesforce_get_user_info"
    "salesforce_get_record_count"
)

TOOLS_FOUND=0
for tool in "${TOOLS[@]}"; do
    if orchestrate tools list | grep -q "$tool"; then
        echo -e "${GREEN}✅ $tool${NC}"
        ((TOOLS_FOUND++))
    else
        echo -e "${RED}❌ $tool${NC}"
    fi
done

echo ""
echo -e "${BLUE}📊 Test Results:${NC}"
echo -e "${GREEN}✅ Tools found: $TOOLS_FOUND/${#TOOLS[@]}${NC}"

if [ $TOOLS_FOUND -eq ${#TOOLS[@]} ]; then
    echo -e "${GREEN}🎉 All tools are properly installed!${NC}"
else
    echo -e "${RED}⚠️  Some tools are missing. Please check the import process.${NC}"
fi

echo ""
echo -e "${BLUE}🔧 Manual Testing Suggestions:${NC}"
echo "1. Test basic query: 'Show me all users in the org'"
echo "2. Test object description: 'Describe the Account object'"
echo "3. Test record count: 'How many accounts are there?'"
echo "4. Test user info: 'What is my user information?'"
echo ""
echo -e "${YELLOW}💡 Note: Make sure your Salesforce credentials are configured before testing!${NC}"
