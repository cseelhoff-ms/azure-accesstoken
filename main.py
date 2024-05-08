import requests
import time

def get_access_token(clientId:str, device_code:str, secondsBetweenVerificationChecks:int, secondsUntilVerificationExpires:int):
    token_uri = f"https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
    grant_type = "urn:ietf:params:oauth:grant-type:device_code"    
    bodyToken : dict[str, str]= {
        "grant_type": grant_type,
        "client_id": clientId,
        "device_code": device_code
    }
    while secondsUntilVerificationExpires > 0:
        time.sleep(secondsBetweenVerificationChecks)
        secondsUntilVerificationExpires -= secondsBetweenVerificationChecks
        token_response = requests.post(token_uri, data=bodyToken).json()
        if 'access_token' in token_response:
            return token_response['access_token']
        if 'error' in token_response:
            error_name = token_response['error']
            if error_name == "authorization_pending":
                print("authorization_pending")
                continue
            print(error_name)
        return None

# Set clientId to PowerShell - https://learn.microsoft.com/en-us/troubleshoot/azure/entra/entra-id/governance/verify-first-party-apps-sign-in#application-ids-of-commonly-used-microsoft-applications
clientId = "1950a258-227b-4e31-a9cf-717495945fc2"
bodyDeviceCode = {
    "scope": "openid offline_access",
    "client_id": clientId
}
device_code_uri = f"https://login.microsoftonline.com/organizations/oauth2/v2.0/devicecode"
deviceCodeResponse = requests.get(device_code_uri, data=bodyDeviceCode).json()
print(deviceCodeResponse['message'])
secondsUntilVerificationExpires = deviceCodeResponse['expires_in']
secondsBetweenVerificationChecks = deviceCodeResponse['interval']
device_code = deviceCodeResponse['device_code']
accessToken = get_access_token(clientId, device_code, secondsBetweenVerificationChecks, secondsUntilVerificationExpires)
if accessToken is None:
    print("Access token is None")
    exit()
print("Access token: ", accessToken)
headers = {"Authorization": f"Bearer {accessToken}"}
