#!/usr/bin/env bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🗑️  Salesforce Agent Removal Script${NC}"
echo "======================================="

# Activate the environment (you can change this to your preferred environment)
ENVIRONMENT_NAME=${1:-"challenge"}
echo -e "${YELLOW}Using environment: ${ENVIRONMENT_NAME}${NC}"
orchestrate env activate ${ENVIRONMENT_NAME}

# Function to safely remove items
safe_remove() {
    local item_type=$1
    local item_name=$2
    echo -e "${YELLOW}Removing ${item_type}: ${item_name}${NC}"
    
    if [[ "$item_type" == "agent" ]]; then
        orchestrate agents remove --name "$item_name" 2>/dev/null || echo -e "${RED}  ❌ Failed to remove or doesn't exist${NC}"
    elif [[ "$item_type" == "tool" ]]; then
        orchestrate tools remove --name "$item_name" 2>/dev/null || echo -e "${RED}  ❌ Failed to remove or doesn't exist${NC}"
    elif [[ "$item_type" == "connection" ]]; then
        orchestrate connections remove --app-id "$item_name" 2>/dev/null || echo -e "${RED}  ❌ Failed to remove or doesn't exist${NC}"
    fi
}

# Remove the agent
safe_remove "agent" "salesforce_agent"

# Remove the tools (each tool individually)
echo -e "${YELLOW}Removing Salesforce tools...${NC}"
safe_remove "tool" "salesforce_query"
safe_remove "tool" "salesforce_search"
safe_remove "tool" "salesforce_create_record"
safe_remove "tool" "salesforce_update_record"
safe_remove "tool" "salesforce_delete_record"
safe_remove "tool" "salesforce_get_record"
safe_remove "tool" "salesforce_describe_object"
safe_remove "tool" "salesforce_list_objects"
safe_remove "tool" "salesforce_upsert_record"
safe_remove "tool" "salesforce_bulk_create"
safe_remove "tool" "salesforce_get_recent_records"
safe_remove "tool" "salesforce_get_user_info"
safe_remove "tool" "salesforce_get_record_count"

# Remove the connection (optional - ask user)
echo -e "${YELLOW}Do you want to remove the Salesforce connection as well? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    safe_remove "connection" "salesforce_creds"
    echo -e "${GREEN}✅ Connection removal attempted${NC}"
else
    echo -e "${YELLOW}⚠️  Connection kept - you can remove it later with: orchestrate connections remove --app-id salesforce_creds${NC}"
fi

echo -e "${GREEN}✅ Salesforce agent cleanup completed!${NC}"
echo ""
echo -e "${YELLOW}💡 Note: This script does not remove Python dependencies or credential files.${NC}"
echo -e "${YELLOW}   You may want to manually clean up .env files and Python packages if no longer needed.${NC}"
