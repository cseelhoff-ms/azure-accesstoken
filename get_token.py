import requests
import time
import logging
import os
import jwt

def get_access_token(device_code:str, secondsBetweenVerificationChecks:int, secondsUntilVerificationExpires:int):
    azure_powershell_clientId = "1950a258-227b-4e31-a9cf-717495945fc2"
    token_uri = f"https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
    grant_type = "urn:ietf:params:oauth:grant-type:device_code"    
    bodyToken : dict[str, str]= {
        "grant_type": grant_type,
        "client_id": azure_powershell_clientId,
        "device_code": device_code,
        "audience": "https://management.core.windows.net/",
        "scope": "https://management.azure.com/user_impersonation"
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
                continue
            logging.error(error_name)
        return None

def get_device_code():
    azure_powershell_clientId = "1950a258-227b-4e31-a9cf-717495945fc2"
    device_code_uri = f"https://login.microsoftonline.com/organizations/oauth2/v2.0/devicecode"
    bodyDeviceCode = {
        "scope": "user_impersonation",
        "client_id": azure_powershell_clientId,
        "audience": "https://management.core.windows.net/",
        "scope": "https://management.azure.com/user_impersonation"
    }
    deviceCodeResponse = requests.get(device_code_uri, data=bodyDeviceCode).json()
    logging.info(deviceCodeResponse['message'])
    secondsUntilVerificationExpires = deviceCodeResponse['expires_in']
    secondsBetweenVerificationChecks = deviceCodeResponse['interval']
    device_code = deviceCodeResponse['device_code']
    return device_code, secondsBetweenVerificationChecks, secondsUntilVerificationExpires

# create main section
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    access_token = None
    if 'AZURE_ACCESS_TOKEN' in os.environ:
        access_token = os.environ['AZURE_ACCESS_TOKEN']
        # decode the jwt accessToken to ensure it is not expired
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        # Check if the token will expire in the next 10 minutes
        if time.time() < decoded_token['exp'] - 10*60:
            print(access_token)
            exit(0)
    device_code, secondsBetweenVerificationChecks, secondsUntilVerificationExpires = get_device_code()
    access_token = get_access_token(device_code, secondsBetweenVerificationChecks, secondsUntilVerificationExpires)
    print(access_token)
    exit(0)
    # export AZURE_ACCESS_TOKEN=$(python get_token.py)
