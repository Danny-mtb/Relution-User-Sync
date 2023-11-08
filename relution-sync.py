import json
import requests
import datetime

try:
    configFile = open('config.json')
    config = json.load(configFile)
    configFile.close()
except FileNotFoundError:
    exit('No config.json found')

accessToken = config['accessToken']
relutionServer = config['protocol'] + '://' + config['hostname'] + ':' + config['port']
azureGroupId = config['azureGroupId']
relutionGroupId = config['relutionGroupId']
organisationUUID = config['organisationUUID']

logDateAndTime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

logFile = open('/opt/relution-sync/log/error.log', 'a')


def systemCheck():
    if accessToken == '':
        logFile.write(logDateAndTime + ' | No access token found in config.json\n')
    if relutionServer == '':
        logFile.write(logDateAndTime + ' |  No relution server found in config.json\n')
    if azureGroupId == '':
        logFile.write(logDateAndTime + ' | No azure group id found in config.json\n')
    if relutionGroupId == '':
        logFile.write(logDateAndTime + ' | No relution group id found in config.json\n')
    if organisationUUID == '':
        logFile.write(logDateAndTime + ' | No organisation UUID found in config.json\n')


def getGroupUUID(groupName):
    exit()


def addUserToGroup(uuid):
    userCount = 0

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
        logFile.write(logDateAndTime + ' | No users to add\n')

    elif len(uuid) == 1:
        userId = str(uuid)
        response = requests.put(
            relutionServer + '/api/v1/security/users/' + userId + '/groups',
            params=params,
            headers=headers,
            json=json_data,
        )

        if response.status_code == 200:
            userCount += 1

    else:
        for i in range(len(uuid)):
            response = requests.put(
                relutionServer + '/api/v1/security/users/' + uuid[i] + '/groups',
                params=params,
                headers=headers,
                json=json_data,
            )

            if response.status_code == 200:
                userCount += 1

    logFile.write(logDateAndTime + ' | Successfully added ' + str(userCount) + ' users to group\n')


def getAzureUsersByGroup(groupId_2):
    headers = {'X-User-Access-Token': accessToken}
    url = relutionServer + '/api/v1/security/groups/' + groupId_2 + '/members?tenantOrganizationUuid=' + organisationUUID

    import requests
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        logFile.write(logDateAndTime + ' | Access token is invalid\n')
    if response.status_code == 404:
        logFile.write(logDateAndTime + ' | Organisation UUID is invalid\n')
    if response.status_code == 200:
        logFile.write(logDateAndTime + ' | Successfully got Azure users from relution server\n')

    usersInGroup = []
    users = response.json()['items']
    for i in range(len(users)):
        if users[i]['type'] == 'USER':
            usersInGroup.append(users[i]['uuid'])

    return usersInGroup


# Check User is in Relution Group or not, if not add user to array
def getGroupUsers(groupId_1):
    headers = {'X-User-Access-Token': accessToken}
    url = relutionServer + '/api/v1/security/groups/' + groupId_1 + '/members?tenantOrganizationUuid=' + organisationUUID

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        logFile.write(logDateAndTime + ' | Access token is invalid\n')
    if response.status_code == 404:
        logFile.write(logDateAndTime + ' | Organisation UUID is invalid\n')
    if response.status_code == 200:
        logFile.write(logDateAndTime + ' | Successfully got users from relution server\n')

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
    addUserToGroup(comparisonGroups(getGroupUsers(relutionGroupId), getAzureUsersByGroup(azureGroupId)))


if __name__ == '__main__':
    main()
