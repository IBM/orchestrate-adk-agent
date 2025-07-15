#!/usr/bin/env python3
"""
Test script to debug Salesforce connection access
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test import
    from ibm_watsonx_orchestrate.run import connections

    print("✅ Successfully imported connections module")

    # Test connection access
    try:
        conn = connections.key_value("salesforce_creds")
        print("✅ Successfully accessed salesforce_creds connection")
        print(f"Connection type: {type(conn)}")
        print(f"Connection data: {conn}")

        # Test individual key access
        username = conn.get("SF_USERNAME")
        print(f"SF_USERNAME: {username}")

        password = conn.get("SF_PASSWORD")
        print(f"SF_PASSWORD: {'*' * len(password) if password else 'None'}")

        token = conn.get("SF_SECURITY_TOKEN")
        print(f"SF_SECURITY_TOKEN: {'*' * len(token) if token else 'None'}")

        domain = conn.get("SF_DOMAIN")
        print(f"SF_DOMAIN: {domain}")

    except Exception as e:
        print(f"❌ Error accessing connection: {e}")
        print(f"Error type: {type(e)}")
        import traceback

        traceback.print_exc()

except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback

    traceback.print_exc()
