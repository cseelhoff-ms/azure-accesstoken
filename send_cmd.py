import requests
import os
import time
def create_live_response_session(machine_id:str, access_token:str):
    # Define the API endpoint
    url = f"https://api.securitycenter.microsoft.com/API/machines/{machine_id}/runliveresponse"

    # Define the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "Commands":[
            {
                "type":"PutFile",
                "params":[
                    {
                    "key":"FileName",
                    "value":"sigma.zip"
                    }
                ]
            },
            {
                "type":"RunScript",
                "params":[
                    {
                        "key":"ScriptName",
                        "value":"test.ps1"
                    },
                    {
                        "key":"Args",
                        "value":"none"
                    }

                ]
            },
            {
                "type":"GetFile",
                "params":[
                    {
                    "key":"Path",
                    "value":"C:\\Windows\\notepad.exe"
                    }
                ]
            },
        ],
    "Comment":"Testing Live Response API"
    }
    # Send the POST request
    response = requests.post(url, headers=headers, json=body)

    # Check the response
    if response.status_code == 200 or response.status_code == 201:
        print("Live response session created successfully.")
        machine_session_id = response.json()['id']
        command_index = len(body['Commands']) - 1  # Assuming the command index is the index of the last command in the Commands list
        return machine_session_id, command_index
    else:
        print(f"Failed to create live response session. Status code: {response.status_code}. Message: {response.text}")
        return None, None

def send_command(machine_id:str, session_id:str, access_token:str):
    # Define the API endpoint
    url = f"https://api.securitycenter.microsoft.com/API/machines/{machine_id}/liveResponse/{session_id}/commands"

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

def get_live_response_result(machine_action_id:str, command_index:str, access_token:str):
    # Define the API endpoint
    url = f"https://api.securitycenter.microsoft.com/api/machineactions/{machine_action_id}/GetLiveResponseResultDownloadLink(index={command_index})"

    # Define the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Send the GET request
    response = requests.get(url, headers=headers)
    
    while response.status_code == 400:
        print(response.json()['error']['message'])
        time.sleep(3)
        response = requests.get(url, headers=headers)
    # Check the response
    if response.status_code == 200:
        print("Live response result retrieved successfully.")
        return response.json()['value']
    else:
        print(f"Failed to retrieve live response result. Status code: {response.status_code}. Message: {response.text}")
        return None

if __name__ == "__main__":  
    if 'AZURE_ACCESS_TOKEN' not in os.environ:
        print("run: export AZURE_ACCESS_TOKEN=$(python get_token.py)")
        exit(0)
    access_token:str = os.environ['AZURE_ACCESS_TOKEN']
    # Get the access token, machine ID, and session ID
    machine_id:str = "a374bb647d8c94d90070abe9e6530dad23798b3e"
    
    machine_action_id:str = ""
    command_index:int = -1
    machine_action_id, command_index = create_live_response_session(machine_id, access_token)

    print('Machine action id: ', machine_action_id)
    result_download_url = get_live_response_result(machine_action_id, str(command_index), access_token)
    print(result_download_url)

    # Send the command
    #send_command(machine_id, session_id, access_token)