"""
Example usage and configuration for the Salesforce Agent
This file demonstrates how to use the Salesforce agent tools
"""

# Example environment configuration
EXAMPLE_ENV_CONFIG = {
    "production": {
        "SF_USERNAME": "integration.user@company.com",
        "SF_PASSWORD": "your_secure_password",
        "SF_SECURITY_TOKEN": "your_security_token",
        "SF_DOMAIN": "login",
    },
    "sandbox": {
        "SF_USERNAME": "integration.user@company.com.sandbox",
        "SF_PASSWORD": "your_secure_password",
        "SF_SECURITY_TOKEN": "your_security_token",
        "SF_DOMAIN": "test",
    },
    "connected_app": {
        "SF_USERNAME": "integration.user@company.com",
        "SF_PASSWORD": "your_secure_password",
        "SF_CONSUMER_KEY": "your_consumer_key",
        "SF_CONSUMER_SECRET": "your_consumer_secret",
        "SF_DOMAIN": "login",
    },
}

# Example queries for common use cases
EXAMPLE_QUERIES = {
    "accounts": {
        "all_accounts": "SELECT Id, Name, Type, Industry FROM Account LIMIT 100",
        "high_value_accounts": "SELECT Id, Name, AnnualRevenue FROM Account WHERE AnnualRevenue > 1000000",
        "recent_accounts": "SELECT Id, Name, CreatedDate FROM Account WHERE CreatedDate = TODAY",
    },
    "contacts": {
        "all_contacts": "SELECT Id, Name, Email, Account.Name FROM Contact LIMIT 100",
        "contacts_by_account": "SELECT Id, Name, Email FROM Contact WHERE AccountId = '001XXXXXXXXXXXXXXX'",
        "recent_contacts": "SELECT Id, Name, Email, CreatedDate FROM Contact WHERE CreatedDate >= YESTERDAY",
    },
    "opportunities": {
        "open_opportunities": "SELECT Id, Name, Amount, CloseDate, StageName FROM Opportunity WHERE IsClosed = false",
        "closing_soon": "SELECT Id, Name, Amount, CloseDate FROM Opportunity WHERE CloseDate <= NEXT_MONTH AND IsClosed = false",
        "big_deals": "SELECT Id, Name, Amount, Account.Name FROM Opportunity WHERE Amount > 100000",
    },
    "leads": {
        "new_leads": "SELECT Id, Name, Email, Status, Company FROM Lead WHERE CreatedDate = TODAY",
        "qualified_leads": "SELECT Id, Name, Email, Status FROM Lead WHERE Status = 'Qualified'",
        "leads_by_source": "SELECT Id, Name, LeadSource FROM Lead WHERE LeadSource != null",
    },
}

# Example record creation templates
EXAMPLE_RECORD_TEMPLATES = {
    "account": {
        "Name": "Acme Corporation",
        "Type": "Customer",
        "Industry": "Technology",
        "Phone": "+1-555-123-4567",
        "Website": "https://acme.com",
        "BillingStreet": "123 Main Street",
        "BillingCity": "San Francisco",
        "BillingState": "CA",
        "BillingPostalCode": "94105",
        "BillingCountry": "USA",
    },
    "contact": {
        "FirstName": "John",
        "LastName": "Doe",
        "Email": "john.doe@acme.com",
        "Phone": "+1-555-987-6543",
        "Title": "VP of Sales",
        "Department": "Sales",
    },
    "lead": {
        "FirstName": "Jane",
        "LastName": "Smith",
        "Email": "jane.smith@prospect.com",
        "Company": "Prospect Company",
        "Phone": "+1-555-456-7890",
        "Title": "IT Director",
        "Status": "Open - Not Contacted",
        "LeadSource": "Website",
    },
    "opportunity": {
        "Name": "Acme - New Implementation",
        "Amount": 50000,
        "CloseDate": "2024-03-31",
        "StageName": "Prospecting",
        "Probability": 25,
        "Type": "New Customer",
    },
}

# Example bulk operations
EXAMPLE_BULK_OPERATIONS = {
    "bulk_contacts": [
        {
            "FirstName": "Alice",
            "LastName": "Johnson",
            "Email": "alice.johnson@example.com",
            "Phone": "+1-555-111-2222",
        },
        {
            "FirstName": "Bob",
            "LastName": "Williams",
            "Email": "bob.williams@example.com",
            "Phone": "+1-555-333-4444",
        },
        {
            "FirstName": "Carol",
            "LastName": "Brown",
            "Email": "carol.brown@example.com",
            "Phone": "+1-555-555-6666",
        },
    ]
}

# Example search queries
EXAMPLE_SEARCH_QUERIES = {
    "find_company": "FIND {Acme} IN ALL FIELDS RETURNING Account(Id, Name), Contact(Id, Name, Email), Lead(Id, Name, Email, Company)",
    "find_email": "FIND {john@example.com} IN EMAIL FIELDS RETURNING Contact(Id, Name, Email), Lead(Id, Name, Email)",
    "find_phone": "FIND {555-123-4567} IN PHONE FIELDS RETURNING Contact(Id, Name, Phone), Lead(Id, Name, Phone)",
}

# Example agent interactions
EXAMPLE_AGENT_INTERACTIONS = [
    {
        "user_input": "Show me all accounts created today",
        "expected_tool": "salesforce_query",
        "expected_query": "SELECT Id, Name, CreatedDate FROM Account WHERE CreatedDate = TODAY",
    },
    {
        "user_input": "Create a new contact named John Doe with email john@example.com",
        "expected_tool": "salesforce_create_record",
        "expected_object": "Contact",
        "expected_data": {
            "FirstName": "John",
            "LastName": "Doe",
            "Email": "john@example.com",
        },
    },
    {
        "user_input": "Find all opportunities with amount greater than 100000",
        "expected_tool": "salesforce_query",
        "expected_query": "SELECT Id, Name, Amount FROM Opportunity WHERE Amount > 100000",
    },
    {
        "user_input": "Describe the Lead object",
        "expected_tool": "salesforce_describe_object",
        "expected_object": "Lead",
    },
    {
        "user_input": "How many contacts are there?",
        "expected_tool": "salesforce_get_record_count",
        "expected_object": "Contact",
    },
]

# Common SOQL patterns
SOQL_PATTERNS = {
    "basic_select": "SELECT {fields} FROM {object}",
    "with_where": "SELECT {fields} FROM {object} WHERE {condition}",
    "with_limit": "SELECT {fields} FROM {object} LIMIT {limit}",
    "with_order": "SELECT {fields} FROM {object} ORDER BY {field} {direction}",
    "with_relationship": "SELECT {fields}, {parent}.{parent_field} FROM {object}",
    "date_filter": "SELECT {fields} FROM {object} WHERE {date_field} = {date_literal}",
    "aggregate": "SELECT COUNT({field}) FROM {object} GROUP BY {group_field}",
}

# Date literals for SOQL
DATE_LITERALS = [
    "TODAY",
    "YESTERDAY",
    "TOMORROW",
    "LAST_WEEK",
    "THIS_WEEK",
    "NEXT_WEEK",
    "LAST_MONTH",
    "THIS_MONTH",
    "NEXT_MONTH",
    "LAST_QUARTER",
    "THIS_QUARTER",
    "NEXT_QUARTER",
    "LAST_YEAR",
    "THIS_YEAR",
    "NEXT_YEAR",
]

# Common field names by object
COMMON_FIELDS = {
    "Account": [
        "Id",
        "Name",
        "Type",
        "Industry",
        "Phone",
        "Website",
        "BillingCity",
        "BillingState",
        "BillingCountry",
        "AnnualRevenue",
        "NumberOfEmployees",
    ],
    "Contact": [
        "Id",
        "Name",
        "FirstName",
        "LastName",
        "Email",
        "Phone",
        "Title",
        "Department",
        "AccountId",
        "Account.Name",
    ],
    "Lead": [
        "Id",
        "Name",
        "FirstName",
        "LastName",
        "Email",
        "Phone",
        "Company",
        "Title",
        "Status",
        "LeadSource",
        "City",
        "State",
        "Country",
    ],
    "Opportunity": [
        "Id",
        "Name",
        "Amount",
        "CloseDate",
        "StageName",
        "Probability",
        "Type",
        "AccountId",
        "Account.Name",
        "OwnerId",
        "Owner.Name",
    ],
    "Case": [
        "Id",
        "CaseNumber",
        "Subject",
        "Status",
        "Priority",
        "Origin",
        "AccountId",
        "Account.Name",
        "ContactId",
        "Contact.Name",
    ],
    "Task": [
        "Id",
        "Subject",
        "Status",
        "Priority",
        "ActivityDate",
        "Description",
        "WhoId",
        "WhatId",
        "OwnerId",
        "Owner.Name",
    ],
    "User": [
        "Id",
        "Name",
        "FirstName",
        "LastName",
        "Email",
        "Username",
        "Profile.Name",
        "UserRole.Name",
        "IsActive",
    ],
}

# Error handling examples
ERROR_EXAMPLES = {
    "invalid_field": "SELECT InvalidField FROM Account",
    "invalid_object": "SELECT Id FROM InvalidObject",
    "malformed_query": "SELECT Id Name FROM Account",
    "permission_error": "SELECT Id FROM Setup_Object__c",
    "limit_exceeded": "SELECT Id FROM Account LIMIT 50001",
}

if __name__ == "__main__":
    print("This file contains examples and configurations for the Salesforce Agent.")
    print("Use these examples to understand how to interact with the agent.")
    print("\nExample queries:")
    for category, queries in EXAMPLE_QUERIES.items():
        print(f"\n{category.upper()}:")
        for name, query in queries.items():
            print(f"  {name}: {query}")
