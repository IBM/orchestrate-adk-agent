# Salesforce Agent for watsonx Orchestrate

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/salesforce-agent/ci.yml?branch=main)](https://github.com/your-org/salesforce-agent/actions)
[![Version](https://img.shields.io/github/v/release/your-org/salesforce-agent)](https://github.com/your-org/salesforce-agent/releases)

A comprehensive Salesforce agent built for IBM watsonx Orchestrate ADK that provides powerful tools to interact with your Salesforce org using the simple-salesforce Python library.

### NOTE: This is just a example implementation to help you get started with orchestrate adk and create agents/tools/connections. The salesforce tools added here are NOT meant for deployment purpose. Please take this only as example implementation

## Getting Started

### Prerequisites

- Python 3.8+
- IBM watsonx Orchestrate ADK
- Salesforce account with API access

### Installation

```bash
git clone https://github.com/your-org/salesforce-agent.git
cd salesforce-agent
pip install -r requirements.txt
cp .env.template .env
# Fill in your Salesforce credentials in .env
```

> **Note:** Make scripts executable if needed:
>
> ```bash
> chmod +x import_agent.sh setup_connection.sh check_connection.sh test_agent.sh
> ```

## Repository Structure

- `agents/`: Agent configuration files
- `tools/`: Python tools for Salesforce operations
- `connections/`: Connection configuration files
- `requirements.txt`: Python dependencies
- `.env.template`: Environment variable template
- `import_agent.sh`, `setup_connection.sh`, `check_connection.sh`, `test_agent.sh`: Shell scripts for quick setup and testing

## Shell Scripts

- `import_agent.sh`: Imports the agent into Orchestrate.
  ```bash
  ./import_agent.sh
  ```
- `setup_connection.sh`: Sets up Salesforce connection.
  ```bash
  ./setup_connection.sh
  ```
- `check_connection.sh`: Checks connection status.
  ```bash
  ./check_connection.sh
  ```
- `test_agent.sh`: Runs agent tests.
  ```bash
  ./test_agent.sh
  ```

Each script prints helpful messages and checks for required environment variables. If you encounter errors, ensure your `.env` file is configured and the scripts have execute permissions.

## Features

### Core Capabilities

- **SOQL Queries**: Execute complex Salesforce Object Query Language queries
- **SOSL Searches**: Search across multiple Salesforce objects
- **CRUD Operations**: Create, Read, Update, Delete records
- **Bulk Operations**: Handle multiple records efficiently
- **Metadata Access**: Describe objects, fields, and org structure
- **User Information**: Get current user and org details

### Supported Operations

- Query records with filtering, sorting, and relationships
- Search across multiple objects simultaneously
- Create new records with validation
- Update existing records with change tracking
- Delete records with confirmation
- Upsert records using external IDs
- Bulk create multiple records
- Get record counts with filtering
- Retrieve recent records
- Access object metadata and field definitions

## Installation

1. **Clone or create the agent directory structure**:

```bash
salesforce_agent/
├── agents/
│   └── salesforce_agent.yaml
├── tools/
│   └── salesforce_tools.py
├── connections/
│   └── salesforce_connection.yaml
├── requirements.txt
├── .env.template
├── import_agent.sh
├── setup_connection.sh
├── check_connection.sh
└── README.md
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Configure credentials** (choose one method):

### Method 1: Orchestrate Connections (Recommended)

Use the built-in script to set up the connection:

```bash
./setup_connection.sh
```

This will:

- Import the connection configuration
- Prompt you for your Salesforce credentials
- Store them securely in orchestrate
- Associate the connection with your tools

### Method 2: Environment Variables (.env file)

Copy `.env.template` to `.env` and configure:

```bash
# For production org
SF_USERNAME=your_username@company.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
SF_DOMAIN=login

# For sandbox org
SF_USERNAME=your_username@company.com.sandbox
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
SF_DOMAIN=test
```

## Quick Start

1. **Import the agent and tools**:

```bash
./import_agent.sh
```

2. **Set up your Salesforce connection**:

```bash
./setup_connection.sh
```

3. **Check connection status**:

```bash
./check_connection.sh
```

4. **Test the agent**:

```bash
./test_agent.sh
```

## Connection Management

### Using Orchestrate Connections (Recommended)

The agent uses orchestrate's connection management system to securely store and access credentials:

- **Connection ID**: `salesforce_creds`
- **Connection Type**: `key_value`
- **Required Keys**:
  - `SF_USERNAME`: Your Salesforce username
  - `SF_PASSWORD`: Your Salesforce password
  - `SF_SECURITY_TOKEN`: Your security token
  - `SF_DOMAIN`: `login` for production, `test` for sandbox

### Credential Hierarchy

The tools check for credentials in this order:

1. Orchestrate connections (`salesforce_creds`)
2. Environment variables (`.env` file)
3. System environment variables

## Tools Reference

### Query and Search Tools

#### `salesforce_query`

Execute SOQL queries against Salesforce.

```python
# Example: Get all accounts with more than 100 employees
query = "SELECT Id, Name, NumberOfEmployees FROM Account WHERE NumberOfEmployees > 100"
```

#### `salesforce_search`

Execute SOSL searches across multiple objects.

```python
# Example: Search for "Acme" across all searchable objects
search_term = "Acme"
```

### Record Management Tools

#### `salesforce_create_record`

Create new records in Salesforce.

```python
# Example: Create a new contact
object_type = "Contact"
record_data = '{"LastName": "Doe", "FirstName": "John", "Email": "john.doe@example.com"}'
```

#### `salesforce_update_record`

Update existing records.

```python
# Example: Update account phone number
object_type = "Account"
record_id = "001XXXXXXXXXXXXXXX"
record_data = '{"Phone": "+1-555-123-4567"}'
```

#### `salesforce_delete_record`

Delete records from Salesforce.

```python
# Example: Delete a lead
object_type = "Lead"
record_id = "00QXXXXXXXXXXXXXXX"
```

#### `salesforce_get_record`

Retrieve specific records by ID.

```python
# Example: Get account details
object_type = "Account"
record_id = "001XXXXXXXXXXXXXXX"
```

### Bulk Operations

#### `salesforce_bulk_create`

Create multiple records using Bulk API.

```python
# Example: Create multiple contacts
object_type = "Contact"
records_data = '[
    {"LastName": "Smith", "Email": "smith@example.com"},
    {"LastName": "Jones", "Email": "jones@example.com"}
]'
```

#### `salesforce_upsert_record`

Insert or update records using external IDs.

```python
# Example: Upsert contact using custom external ID
object_type = "Contact"
external_id_field = "External_ID__c"
external_id_value = "EXT-001"
record_data = '{"LastName": "Wilson", "Email": "wilson@example.com"}'
```

### Metadata and Information Tools

#### `salesforce_describe_object`

Get metadata for Salesforce objects.

```python
# Example: Describe the Account object
object_type = "Account"
```

#### `salesforce_list_objects`

List all available objects in the org.

#### `salesforce_get_user_info`

Get current user information.

#### `salesforce_get_record_count`

Get record counts with optional filtering.

```python
# Example: Count accounts created today
object_type = "Account"
where_clause = "CreatedDate = TODAY"
```

#### `salesforce_get_recent_records`

Get recently created records.

```python
# Example: Get 10 most recent opportunities
object_type = "Opportunity"
limit = 10
```

## Agent Usage Examples

### Basic Queries

- "Show me all accounts with more than 100 employees"
- "Find all opportunities closing this month"
- "Get all contacts from Acme Corp"

### Record Management

- "Create a new contact named John Doe with email john@example.com"
- "Update account A001 with phone number 555-123-4567"
- "Delete lead L001 (with confirmation)"

### Bulk Operations

- "Create 100 new contacts from this data"
- "Update all accounts in California with new tax rate"

### Metadata Queries

- "Describe the Lead object and its fields"
- "Show me all custom objects in the org"
- "What are the required fields for creating an Account?"

### Analytics

- "How many opportunities were created today?"
- "Show me the 10 most recent cases"
- "Count all contacts by account"

## Error Handling

The agent includes comprehensive error handling:

- **Connection errors**: Clear messages about authentication issues
- **API errors**: Detailed Salesforce API error responses
- **Validation errors**: Field validation and required field checks
- **Permission errors**: Clear messages about insufficient permissions

## Security Best Practices

1. **Credential Management**: Use environment variables or orchestrate connections
2. **Least Privilege**: Use dedicated integration users with minimal permissions
3. **Audit Trail**: All operations are logged in Salesforce
4. **Data Privacy**: Agent respects field-level security and sharing rules
5. **Rate Limiting**: Built-in respect for Salesforce API limits

## Authentication Methods

### Username/Password/Security Token

Most common method for server-to-server integration.

### Session ID

For existing authenticated sessions.

### Connected App (OAuth)

For more secure, token-based authentication.

### IP Whitelisting

For orgs with IP restrictions.

## Troubleshooting

### Common Issues

1. **Authentication Failed**: Check credentials and security token
2. **Insufficient Permissions**: Verify user has required object permissions
3. **API Limits**: Monitor API usage in Salesforce Setup
4. **Network Issues**: Check firewall and proxy settings

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export SF_DEBUG=true
```

## How to Contribute

We welcome contributions from the community! To contribute:

1. Fork this repository and create your feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit your changes:
   ```bash
   git commit -am "Add your feature or fix"
   ```
3. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a Pull Request on GitHub and describe your changes.

Please ensure your code is well-tested and documented. For major changes, open an issue first to discuss your proposal.

## Reporting Issues & Support

- For bugs, feature requests, or questions, please use [GitHub Issues](https://github.com/your-org/salesforce-agent/issues).
- For general discussion, join GitHub Discussions or contact the maintainers listed in the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Maintainers & Community

- Maintainers: [Add your GitHub usernames here]
- Community: Join GitHub Discussions for Q&A and collaboration
