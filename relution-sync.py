#!/usr/bin/python
# Author: Danny Anders
# Version: 1.1
import json
import requests
import datetime

try:
    configFile = open('./config/config.json')
    config = json.load(configFile)
    configFile.close()
except FileNotFoundError:
    exit('No config.json found')

accessToken = config['accessToken']
relutionServer = config['protocol'] + '://' + config['hostname'] + ':' + config['port']

logDateAndTime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
logFile = open('/var/log/relution-sync.log', 'a')


def getOrganisationNumbersFromConfig():
    return len(config["organisation"])


def systemCheck():
    if accessToken == '':
        logFile.write(logDateAndTime + ' | No access token found in config.json\n')
    if relutionServer == '':
        logFile.write(logDateAndTime + ' |  No relution server found in config.json\n')


def addUserToGroup(uuid, organisationUUID, groupId_1):
    userCount = 0

    headers = {
        'accept': 'application/json',
        'X-User-Access-Token': accessToken,
        'Content-Type': 'application/json',
    }
    params = {
        'tenantOrganizationUuid': organisationUUID
    }
    json_data = [
        groupId_1,
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

    logFile.write(logDateAndTime + '| ' + groupId_1 + ' | Successfully added ' + str(userCount) + ' users to group\n')


def getAzureUsersByGroup(groupId_2, organisationUUID):
    headers = {'X-User-Access-Token': accessToken}
    url = relutionServer + '/api/v1/security/groups/' + groupId_2 + '/members?tenantOrganizationUuid=' + organisationUUID

    import requests
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        logFile.write(logDateAndTime + ' | Access token is invalid\n')
    if response.status_code == 404:
        logFile.write(logDateAndTime + ' | Organisation UUID is invalid\n')

    usersInGroup = []
    users = response.json()['items']
    for i in range(len(users)):
        if users[i]['type'] == 'USER':
            usersInGroup.append(users[i]['uuid'])

    return usersInGroup


def getGroupUsers(groupId_1, organisationUUID):
    headers = {'X-User-Access-Token': accessToken}
    url = relutionServer + '/api/v1/security/groups/' + groupId_1 + '/members?tenantOrganizationUuid=' + organisationUUID

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        logFile.write(logDateAndTime + ' | Access token is invalid\n')
    if response.status_code == 404:
        logFile.write(logDateAndTime + ' | Organisation UUID is invalid\n')

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


def main(organisationConfigNumbers):
    for orgIndex in range(organisationConfigNumbers):
        organisationUUID = config["organisation"][orgIndex]["organisationUUID"]
        groupId_1 = config["organisation"][orgIndex]["groupId_1"]
        groupId_2 = config["organisation"][orgIndex]["groupId_2"]
        addUserToGroup(comparisonGroups(getGroupUsers(groupId_1, organisationUUID), getAzureUsersByGroup(groupId_2, organisationUUID)), organisationUUID, groupId_1)


if __name__ == '__main__':
    systemCheck()
    main(getOrganisationNumbersFromConfig())
