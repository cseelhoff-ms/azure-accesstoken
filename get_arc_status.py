import os
import requests

def create_live_response_session(machine_id:str, access_token:str):
    # Define the API endpoint
    url = f"https://api.securitycenter.windows.com/api/machineactions"

    # Define the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Define the payload
    payload = {
        "Type": "LiveResponse",
        "MachineId": machine_id,
        "Comment": "Initiating live response session"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check the response
    if response.status_code == 200:
        print("Live response session created successfully.")
        return response.json()['id']
    else:
        print(f"Failed to create live response session. Status code: {response.status_code}. Message: {response.text}")
        return None


# Create a new live response session
if __name__ == "__main__":        
    if 'AZURE_ACCESS_TOKEN' not in os.environ:
        print("run: export AZURE_ACCESS_TOKEN=$(python get_mde_token.py)")
        exit(0)
    access_token = os.environ['AZURE_ACCESS_TOKEN']

    
    # Get the machine ID
    machine_id = "<your-machine-id>"

    # Define the API endpoint
    url = f"https://api.securitycenter.windows.com/api/machines/{machine_id}/liveResponse/{session_id}/commands"

    # Define the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Define the payload
    payload = {
        "Command": "powershell",
        "Parameters": "Restart-Computer -Force"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check the response
    if response.status_code == 200:
        print("Command sent successfully.")
    else:
        print(f"Failed to send command. Status code: {response.status_code}. Message: {response.text}")

    # Get the access token, machine ID, and session ID
    access_token = os.getenv("AZURE_ACCESS_TOKEN")
    machine_id = "<your-machine-id>"
    session_id = "<your-session-id>"

    session_id = create_live_response_session(machine_id, access_token)

    # Get the Azure Arc resource connection status
    resourceGroupName = "default-rg"
    machineName = "rsyslog"
    arc_resource_url = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{machineName}?api-version=2019-12-12"
    arc_resource_response = requests.get(arc_resource_url, headers=headers)
    arc_resource_data = arc_resource_response.json()
    connection_status = arc_resource_data['properties']['status']
    print("Connection status: ", connection_status)
