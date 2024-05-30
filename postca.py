import os
import requests
import json

if __name__ == "__main__":        
    if 'AZURE_ACCESS_TOKEN' not in os.environ:
        print("run: export AZURE_ACCESS_TOKEN=$(python get_token.py)")
        exit(0)
    accessToken = os.environ['AZURE_ACCESS_TOKEN']
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "Content-type": "application/json"
    }
    #subscriptions_url = "https://management.azure.com/subscriptions?api-version=2020-01-01"
    #subscriptions_response = requests.get(subscriptions_url, headers=headers)
    #subscriptions_data = subscriptions_response.json()
    #if len(subscriptions_data['value']) == 1:
    #    subscriptionId = subscriptions_data['value'][0]['subscriptionId']
    #    print("SubscriptionId: ", subscriptionId)
    #else:
    #    for subscription in subscriptions_data['value']:
    #        print(subscription['displayName'], subscription['subscriptionId'])
    #    subscriptionId = input("Enter subscriptionId: ")

    capolicy_url = "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies"

    payload = {
        "displayName": "Access to EXO requires MFA",
        "state": "enabled",
        "conditions": {
            "clientAppTypes": [
                "mobileAppsAndDesktopClients",
                "browser"
            ],
            "applications": {
                "includeApplications": [
                    "1950a258-227b-4e31-a9cf-717495945fc2"
                ]
            },
            "users": {
                "includeGroups": ["118e7ded-8b0f-4836-ba06-8ff1ecc5c8ba"]
            },
            "locations": {
                "includeLocations": [
                    "All"
                ],
                "excludeLocations": [
                    "AllTrusted"
                ]
            }
        },
        "grantControls": {
            "operator": "OR",
            "builtInControls": [
                "mfa"
            ]
        }
    }

    capolicy_response = requests.post(capolicy_url, headers=headers, data=json.dumps(payload))
    capolicy_data = capolicy_response.json()
    print("capolicy_data: ", capolicy_data['value'])