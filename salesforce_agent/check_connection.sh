#!/bin/bash

# Check Salesforce connection status
echo "Checking Salesforce connection status..."

# Activate virtual environment
if [ -f "orchestrate/bin/activate" ]; then
    source orchestrate/bin/activate
    echo "Virtual environment activated"
else
    echo "Virtual environment not found at orchestrate/bin/activate"
    exit 1
fi

# Navigate to salesforce_agent directory
cd salesforce_agent

# Check if connection exists
echo "Checking if connection exists..."
if orchestrate connections list | grep -q "salesforce_creds"; then
    echo "✅ Connection 'salesforce_creds' exists"
    
    # Check connection details
    echo "Connection details:"
    orchestrate connections describe --app-id salesforce_creds
    
    # Test connection by trying to import a simple tool
    echo ""
    echo "Testing connection access..."
    python3 -c "
try:
    from ibm_watsonx_orchestrate.ext.connections import connections
    conn = connections.key_value('salesforce_creds')
    username = conn.get('SF_USERNAME')
    if username:
        print('✅ Connection working - found username:', username)
    else:
        print('❌ Connection found but no SF_USERNAME set')
except Exception as e:
    print('❌ Error accessing connection:', str(e))
"
else
    echo "❌ Connection 'salesforce_creds' not found"
    echo "Run './setup_connection.sh' to create and configure the connection"
fi
