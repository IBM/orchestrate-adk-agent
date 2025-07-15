"""
Salesforce Tools for watsonx Orchestrate Agent
Uses simple-salesforce library for Salesforce operations
"""

import os
import json
from typing import Dict, List, Any, Optional
from simple_salesforce import Salesforce, SalesforceLogin
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.agent_builder.connections import (
    ConnectionType,
    ExpectedCredentials,
)
from ibm_watsonx_orchestrate.run import connections

import datetime
import pytz


def get_salesforce_connection():
    """Create and return a Salesforce connection using credentials from orchestrate connections"""
    try:
        # Get credentials from orchestrate connection (required)
        try:
            conn = connections.key_value("salesforce_creds")
            sf_username = conn.get("SF_USERNAME")
            sf_password = conn.get("SF_PASSWORD")
            sf_security_token = conn.get("SF_SECURITY_TOKEN")
            sf_domain = conn.get("SF_DOMAIN", "login")
            sf_session_id = conn.get("SF_SESSION_ID")
            sf_instance = conn.get("SF_INSTANCE")
            sf_consumer_key = conn.get("SF_CONSUMER_KEY")
            sf_consumer_secret = conn.get("SF_CONSUMER_SECRET")
        except Exception as e:
            raise Exception(
                f"Failed to access Salesforce connection 'salesforce_creds': {str(e)}. Please ensure the connection is properly configured."
            )

        # Validate that we have required credentials
        if not sf_username:
            raise Exception(
                "SF_USERNAME not found in connection 'salesforce_creds'. Please set credentials using setup_connection.sh"
            )

        if not sf_password:
            raise Exception(
                "SF_PASSWORD not found in connection 'salesforce_creds'. Please set credentials using setup_connection.sh"
            )

        # Try different authentication methods based on available credentials
        if sf_session_id and sf_instance:
            # Session ID method
            # Session ID method
            sf = Salesforce(instance=sf_instance, session_id=sf_session_id)
        elif sf_username and sf_password and sf_security_token:
            # Username/Password/Security Token method
            sf = Salesforce(
                username=sf_username,
                password=sf_password,
                security_token=sf_security_token,
                domain=sf_domain,  # 'test' for sandbox, 'login' for production
            )
        elif sf_username and sf_password and sf_consumer_key and sf_consumer_secret:
            # Connected App method
            sf = Salesforce(
                username=sf_username,
                password=sf_password,
                consumer_key=sf_consumer_key,
                consumer_secret=sf_consumer_secret,
                domain=sf_domain,
            )
        else:
            raise ValueError(
                "Missing required Salesforce credentials. Please configure the salesforce_creds connection or set appropriate environment variables."
            )

        return sf
    except Exception as e:
        raise Exception(f"Failed to connect to Salesforce: {str(e)}")


@tool(
    name="salesforce_query",
    description="Execute SOQL queries against Salesforce to retrieve records",
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_query(query: str) -> str:
    """
    Execute a SOQL query against Salesforce and return results.

    Args:
        query: SOQL query string (e.g., "SELECT Id, Name FROM Account LIMIT 10")

    Returns:
        JSON string containing query results
    """
    try:
        sf = get_salesforce_connection()

        # Fix common SOQL syntax issues
        # Replace double quotes with single quotes for string literals in WHERE clauses
        import re

        # Pattern to find WHERE clauses with double-quoted values
        fixed_query = re.sub(r'(\s*=\s*)"([^"]+)"', r"\1'\2'", query)

        result = sf.query(fixed_query)

        # Format the response for better readability
        response = {
            "totalSize": result.get("totalSize", 0),
            "done": result.get("done", True),
            "records": result.get("records", []),
        }

        return json.dumps(response, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_search",
    description="Execute SOSL searches across multiple Salesforce objects",
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_search(search_term: str) -> str:
    """
    Execute a SOSL search against Salesforce.

    Args:
        search_term: Search term to find across Salesforce objects

    Returns:
        JSON string containing search results
    """
    try:
        sf = get_salesforce_connection()
        result = sf.search(f"FIND {{{search_term}}}")

        if result is None:
            return json.dumps({"message": "No results found"}, indent=2)

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_create_record",
    description="Create new records in Salesforce",
    permission=ToolPermission.READ_WRITE,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_create_record(object_type: str, record_data: str) -> str:
    """
    Create a new record in Salesforce.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')
        record_data: JSON string containing field values for the new record

    Returns:
        JSON string with creation result including new record ID
    """
    try:
        sf = get_salesforce_connection()

        # Parse the record data
        data = json.loads(record_data)

        # Get the object and create the record
        sobject = getattr(sf, object_type)
        result = sobject.create(data)

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_update_record",
    description="Update existing records in Salesforce",
    permission=ToolPermission.READ_WRITE,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_update_record(object_type: str, record_id: str, record_data: str) -> str:
    """
    Update an existing record in Salesforce.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')
        record_id: Salesforce record ID to update
        record_data: JSON string containing field values to update

    Returns:
        JSON string with update result
    """
    try:
        sf = get_salesforce_connection()

        # Parse the record data
        data = json.loads(record_data)

        # Get the object and update the record
        sobject = getattr(sf, object_type)
        result = sobject.update(record_id, data)

        return json.dumps({"success": True, "status_code": result}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_delete_record",
    description="Delete records from Salesforce",
    permission=ToolPermission.READ_WRITE,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_delete_record(object_type: str, record_id: str) -> str:
    """
    Delete a record from Salesforce.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')
        record_id: Salesforce record ID to delete

    Returns:
        JSON string with deletion result
    """
    try:
        sf = get_salesforce_connection()

        # Get the object and delete the record
        sobject = getattr(sf, object_type)
        result = sobject.delete(record_id)

        return json.dumps({"success": True, "status_code": result}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_get_record",
    description="Retrieve specific records from Salesforce by ID",
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_get_record(object_type: str, record_id: str) -> str:
    """
    Retrieve a specific record from Salesforce by ID.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')
        record_id: Salesforce record ID to retrieve

    Returns:
        JSON string containing the record data
    """
    try:
        sf = get_salesforce_connection()

        # Get the object and retrieve the record
        sobject = getattr(sf, object_type)
        result = sobject.get(record_id)

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_describe_object",
    description="Get metadata and field information for Salesforce objects",
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_describe_object(object_type: str) -> str:
    """
    Get metadata description for a Salesforce object.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')

    Returns:
        JSON string containing object metadata including fields and their properties
    """
    try:
        sf = get_salesforce_connection()

        # Get the object and describe it
        sobject = getattr(sf, object_type)
        result = sobject.describe()

        # Extract key information for better readability
        description = {
            "name": result.get("name"),
            "label": result.get("label"),
            "labelPlural": result.get("labelPlural"),
            "keyPrefix": result.get("keyPrefix"),
            "createable": result.get("createable"),
            "updateable": result.get("updateable"),
            "deletable": result.get("deletable"),
            "queryable": result.get("queryable"),
            "searchable": result.get("searchable"),
            "fields": [
                {
                    "name": field.get("name"),
                    "label": field.get("label"),
                    "type": field.get("type"),
                    "required": field.get("nillable") == False,
                    "createable": field.get("createable"),
                    "updateable": field.get("updateable"),
                    "length": field.get("length"),
                    "picklistValues": field.get("picklistValues", []),
                }
                for field in result.get("fields", [])
            ],
        }

        return json.dumps(description, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_list_objects",
    description="List all available Salesforce objects in the org",
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_list_objects() -> str:
    """
    List all available Salesforce objects in the org.

    Returns:
        JSON string containing list of Salesforce objects with their labels
    """
    try:
        sf = get_salesforce_connection()

        # Get org description
        result = sf.describe()

        # Extract object information
        objects = [
            {
                "name": obj.get("name"),
                "label": obj.get("label"),
                "labelPlural": obj.get("labelPlural"),
                "keyPrefix": obj.get("keyPrefix"),
                "createable": obj.get("createable"),
                "updateable": obj.get("updateable"),
                "deletable": obj.get("deletable"),
                "queryable": obj.get("queryable"),
                "searchable": obj.get("searchable"),
                "custom": obj.get("custom", False),
            }
            for obj in result.get("sobjects", [])
        ]

        return json.dumps({"objects": objects}, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_upsert_record",
    description="Insert or update records in Salesforce using external IDs",
    permission=ToolPermission.READ_WRITE,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_upsert_record(
    object_type: str, external_id_field: str, external_id_value: str, record_data: str
) -> str:
    """
    Upsert (insert or update) a record in Salesforce using an external ID.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')
        external_id_field: Name of the external ID field
        external_id_value: Value of the external ID
        record_data: JSON string containing field values for the record

    Returns:
        JSON string with upsert result
    """
    try:
        sf = get_salesforce_connection()

        # Parse the record data
        data = json.loads(record_data)

        # Get the object and upsert the record
        sobject = getattr(sf, object_type)
        result = sobject.upsert(f"{external_id_field}/{external_id_value}", data)

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_bulk_create",
    description="Create multiple records in Salesforce using Bulk API",
    permission=ToolPermission.READ_WRITE,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_bulk_create(
    object_type: str, records_data: str, batch_size: int = 10000
) -> str:
    """
    Create multiple records in Salesforce using Bulk API.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')
        records_data: JSON string containing array of record data
        batch_size: Number of records per batch (default: 10000)

    Returns:
        JSON string with bulk creation results
    """
    try:
        sf = get_salesforce_connection()

        # Parse the records data
        data = json.loads(records_data)

        # Get the object and bulk create
        sobject = getattr(sf.bulk, object_type)
        result = sobject.insert(data, batch_size=batch_size)

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_get_recent_records",
    description="Get recently created records for a specific object type",
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_get_recent_records(object_type: str, limit: int = 10) -> str:
    """
    Get recently created records for a specific object type.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')
        limit: Number of records to retrieve (default: 10)

    Returns:
        JSON string containing recent records
    """
    try:
        sf = get_salesforce_connection()

        # Query for recent records
        query = f"SELECT Id, Name, CreatedDate FROM {object_type} ORDER BY CreatedDate DESC LIMIT {limit}"
        result = sf.query(query)

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_get_user_info",
    description="Get information about the current Salesforce user",
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_get_user_info() -> str:
    """
    Get information about the current Salesforce user.

    Returns:
        JSON string containing current user information
    """
    try:
        sf = get_salesforce_connection()

        # Query for current user info
        query = "SELECT Id, Name, Email, Username, Profile.Name, UserRole.Name FROM User WHERE Id = :userId"
        # Since we can't use bind variables directly, we'll get the user ID from the session
        user_query = f"SELECT Id, Name, Email, Username, Profile.Name, UserRole.Name FROM User WHERE Username = '{sf.session_id}' OR Id = '{sf.session_id}'"

        # Alternative approach - get current user info
        result = sf.query(
            "SELECT Id, Name, Email, Username, Profile.Name, UserRole.Name FROM User WHERE Id = UserInfo.getUserId()"
        )

        if result["totalSize"] == 0:
            # Fallback to getting any user info we can
            result = sf.query(
                "SELECT Id, Name, Email, Username, Profile.Name, UserRole.Name FROM User LIMIT 1"
            )

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@tool(
    name="salesforce_get_record_count",
    description="Get count of records for a specific object type with optional filtering",
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(app_id="salesforce_creds", type=ConnectionType.KEY_VALUE)
    ],
)
def salesforce_get_record_count(object_type: str, where_clause: str = "") -> str:
    """
    Get the count of records for a specific object type with optional filtering.

    Args:
        object_type: Salesforce object type (e.g., 'Account', 'Contact', 'Lead')
        where_clause: Optional WHERE clause for filtering (e.g., "CreatedDate = TODAY")

    Returns:
        JSON string containing record count
    """
    try:
        sf = get_salesforce_connection()

        # Build the query
        query = f"SELECT COUNT() FROM {object_type}"
        if where_clause:
            query += f" WHERE {where_clause}"

        result = sf.query(query)

        return json.dumps(
            {
                "object_type": object_type,
                "count": result.get("totalSize", 0),
                "where_clause": where_clause or "None",
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
