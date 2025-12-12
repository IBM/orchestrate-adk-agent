#!/usr/bin/env bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Salesforce Agent Import Script${NC}"
echo "======================================"

# Get script directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if we're in the correct environment
echo -e "${YELLOW}Checking orchestrate environment...${NC}"
if ! command -v orchestrate &> /dev/null; then
    echo -e "${RED}❌ Error: orchestrate command not found. Please make sure you have the ADK installed.${NC}"
    exit 1
fi

# Activate the environment (you can change this to your preferred environment)
ENVIRONMENT_NAME=${1:-"local"}
echo -e "${YELLOW}Activating environment: ${ENVIRONMENT_NAME}${NC}"
orchestrate env activate ${ENVIRONMENT_NAME}

# Check if .env file exists in root directory
ROOT_DIR="${SCRIPT_DIR}/.."
if [ ! -f "${ROOT_DIR}/.env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found in root directory. Please create one from .env.template with your Salesforce credentials.${NC}"
    echo -e "${YELLOW}   You can use orchestrate connections for credential management as an alternative.${NC}"
fi

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r "${SCRIPT_DIR}/requirements.txt"

# # Import the connection (if it exists)
# if [ -f "${SCRIPT_DIR}/connections/salesforce_connection.yaml" ]; then
#     echo -e "${YELLOW}Importing Salesforce connection...${NC}"
#     orchestrate connections import --file "${SCRIPT_DIR}/connections/salesforce_connection.yaml"
# fi

# # Import the tools with connection association
# echo -e "${YELLOW}Importing Salesforce tools...${NC}"
# orchestrate tools import -k python -f "${SCRIPT_DIR}/tools/salesforce_tools.py" -r "${SCRIPT_DIR}/requirements.txt" --app-id salesforce_creds

# Import the agent
echo -e "${YELLOW}Importing Salesforce agent...${NC}"
orchestrate agents import -f "${SCRIPT_DIR}/agents/salesforce_agent.yaml"

echo -e "${GREEN}✅ Salesforce agent imported successfully!${NC}"
echo ""
echo -e "${GREEN}📋 Next steps:${NC}"
echo "1. Run './setup_connection.sh' to configure your Salesforce credentials in orchestrate"
echo "2. Test the agent with: orchestrate playground"
echo "3. Or run automated tests with: './test_agent.sh'"
echo ""
echo -e "${YELLOW}Note: If you haven't set up the connection yet, the tools will fallback to environment variables.${NC}"
echo -e "${YELLOW}For production use, it's recommended to use orchestrate connections for credential management.${NC}"
echo "2. Test the agent with: orchestrate agents test salesforce_agent"
echo "3. Use the agent in your watsonx Orchestrate environment"
echo ""
echo -e "${GREEN}🔧 Available tools:${NC}"
echo "- salesforce_query: Execute SOQL queries"
echo "- salesforce_search: Execute SOSL searches"
echo "- salesforce_create_record: Create new records"
echo "- salesforce_update_record: Update existing records"
echo "- salesforce_delete_record: Delete records"
echo "- salesforce_get_record: Get specific records by ID"
echo "- salesforce_describe_object: Get object metadata"
echo "- salesforce_list_objects: List all objects in org"
echo "- salesforce_upsert_record: Upsert records using external ID"
echo "- salesforce_bulk_create: Bulk create multiple records"
echo "- salesforce_get_recent_records: Get recently created records"
echo "- salesforce_get_user_info: Get current user information"
echo "- salesforce_get_record_count: Get record counts with filters"
echo ""
echo -e "${GREEN}💡 Example usage:${NC}"
echo "- 'Show me all accounts created today'"
echo "- 'Create a new contact with name John Doe and email john@example.com'"
echo "- 'Find all opportunities with amount greater than 100000'"
echo "- 'Update account A001 with new phone number'"
echo "- 'Describe the Lead object fields'"
