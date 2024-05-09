import os
import requests

if __name__ == "__main__":        
    if 'AZURE_ACCESS_TOKEN' not in os.environ:
        exit(0)
    accessToken = os.environ['AZURE_ACCESS_TOKEN']
    headers = {"Authorization": f"Bearer {accessToken}"}
    subscriptions_url = "https://management.azure.com/subscriptions?api-version=2020-01-01"
    subscriptions_response = requests.get(subscriptions_url, headers=headers)
    subscriptions_data = subscriptions_response.json()
    if len(subscriptions_data['value']) == 1:
        subscriptionId = subscriptions_data['value'][0]['subscriptionId']
        print("SubscriptionId: ", subscriptionId)
    else:
        for subscription in subscriptions_data['value']:
            print(subscription['displayName'], subscription['subscriptionId'])
        subscriptionId = input("Enter subscriptionId: ")

    resourceGroups_url = f"https://management.azure.com/subscriptions/{subscriptionId}/resourcegroups?api-version=2020-01-01"
    resourceGroups_response = requests.get(resourceGroups_url, headers=headers)
    resourceGroups_data = resourceGroups_response.json()
    print("ResourceGroups: ", resourceGroups_data['value'])
