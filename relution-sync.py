# Description: This script is to sync the users with the 'schueler' group to the 'relution-students' group

# get settings from config file
import json
import requests

configFile = open('config.json')
config = json.load(configFile)
configFile.close()

accessToken = config['accessToken']
relutionServer = config['protocol'] + '://' + config['hostname'] + ':' + config['port']

print('Relution Server: ' + relutionServer)


def systemCheck():
    if accessToken == '':
        print('No access token found in config.json')
        exit()
    if relutionServer == '':
        print('No relution server found in config.json')
        exit()


def getGroupUUID(groupName):
    exit()


def addUserToGroup(uuid):

    headers = {
        'accept': 'application/json',
        'X-User-Access-Token': config['accessToken'],
        'Content-Type': 'application/json',
    }
    params = {
        'tenantOrganizationUuid': config['organisationUUID']
    }
    json_data = [
        config['relutionGroupId'],
    ]

    if len(uuid) == 0:
        print('No users to add')

    elif len(uuid) == 1:
        userId = str(uuid)
        response = requests.put(
            relutionServer + '/api/v1/security/users/' + userId + '/groups',
            params=params,
            headers=headers,
            json=json_data,
        )

        if response.status_code == 200:
            print(uuid + 'added successfully to group')

    else:
        for i in range(len(uuid)):
            response = requests.put(
                relutionServer + '/api/v1/security/users/' + uuid[i] + '/groups',
                params=params,
                headers=headers,
                json=json_data,
            )

            if response.status_code == 200:
                print(uuid[i] + ' added successfully to group')


def getAzureUsersByGroup(azureGroupId):
    organisationUUID = config['organisationUUID']
    headers = {'X-User-Access-Token': accessToken}
    url = relutionServer + '/api/v1/security/groups/' + azureGroupId + '/members?tenantOrganizationUuid=' + organisationUUID

    import requests
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print('Access token is invalid')
        exit()
    if response.status_code == 404:
        print('Organisation UUID is invalid')
        exit()
    if response.status_code == 200:
        print('Successfully got Azure users from relution server')

    usersInGroup = []
    users = response.json()['items']
    for i in range(len(users)):
        if users[i]['type'] == 'USER':
            usersInGroup.append(users[i]['uuid'])

    return usersInGroup


# Check User is in Relution Group
def getGroupUsers(relutionGroupId):
    organisationUUID = config['organisationUUID']
    headers = {'X-User-Access-Token': accessToken}
    url = relutionServer + '/api/v1/security/groups/' + relutionGroupId + '/members?tenantOrganizationUuid=' + organisationUUID

    import requests
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print('Access token is invalid')
        exit()
    if response.status_code == 404:
        print('Organisation UUID is invalid')
        exit()
    if response.status_code == 200:
        print('Successfully got users from relution server')

    usersInGroup = []
    users = response.json()['items']
    for i in range(len(users)):
        if users[i]['type'] == 'USER':
            usersInGroup.append(users[i]['uuid'])

    return usersInGroup


def comparisonGroups(relutionGroup, azureGroup):
    comparisonGroupsAdd = []
    for i in range(len(azureGroup)):
        if azureGroup[i] not in relutionGroup:
            comparisonGroupsAdd.append(azureGroup[i])

    return comparisonGroupsAdd


def main():
    systemCheck()
    addUserToGroup(comparisonGroups(getGroupUsers(config['relutionGroupId']), getAzureUsersByGroup(config['azureGroupId'])))


if __name__ == '__main__':
    main()
