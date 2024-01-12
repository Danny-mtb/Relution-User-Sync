#!/usr/bin/python
# Author: Danny Anders
# Version: 1.3.0
import json
import requests
import datetime
import time


try:
    configFile = open('./config/config.json')
    config = json.load(configFile)
    configFile.close()
except FileNotFoundError:
    exit('No config.json found')

accessToken = config['accessToken']
relutionServer = config['protocol'] + '://' + config['hostname'] + ':' + config['port']

headers = {
        'accept': 'application/json',
        'X-User-Access-Token': accessToken,
        'Content-Type': 'application/json',
    }


logDateAndTime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
logFile = open(config["logPath"] + 'relution-sync.log', 'a+')
uuidCacheFile = open(config["cachePath"] + 'changedUUIDs.cache', 'a+')


def getOrganisationNumbersFromConfig():
    return len(config["organisation"])


def systemCheck():
    if accessToken == '':
        logFile.write(logDateAndTime + ' | No access token found in config.json\n')
    if relutionServer == '':
        logFile.write(logDateAndTime + ' |  No relution server found in config.json\n')


def addUserToGroup(uuid, organisationUUID, groupId_1):
    userCount = 0

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


def getGroupUsers(groupId, organisationUUID):
    url = relutionServer + '/api/v1/security/groups/' + groupId + '/members?tenantOrganizationUuid=' + organisationUUID

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


def comparisonGroups(toGroup, fromGroup):
    comparisonGroupsAdd = []
    for i in range(len(fromGroup)):
        if fromGroup[i] not in toGroup:
            comparisonGroupsAdd.append(fromGroup[i])

    return comparisonGroupsAdd


def getGroupId(groupName, organisationUUID):
    url = relutionServer + '/api/v1/security/groups?tenantOrganizationUuid=' + organisationUUID

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        logFile.write(logDateAndTime + ' | Access token is invalid\n')
    if response.status_code == 404:
        logFile.write(logDateAndTime + ' | Organisation UUID is invalid\n')

    groups = response.json()['items']
    for i in range(len(groups)):
        if groups[i]['name'] == groupName:
            return groups[i]['uuid']


def changeManagedAppleId(userID, organisationUUID):
    global managedAppleId, email
    url = relutionServer + '/api/v1/security/users/' + userID + '?tenantOrganizationUuid=' + organisationUUID

    response = requests.get(url, headers=headers)

    if userID in open('./cache/changedUUIDs.cache', 'r').read():
        if config['userInterface'] == 'True' or config['userInterface'] == 'true':
            print('-', end='')
        else:
            pass

    else:
        try:
            email = response.json()['email']
            managedAppleId = response.json()['managedAppleId']
        except KeyError:
            email = ''
            managedAppleId = ''
        finally:
            if managedAppleId == '' or managedAppleId != email:
                url = relutionServer + '/api/v1/security/users/' + userID + '?tenantOrganizationUuid=' + organisationUUID
                payload = {
                    "managedAppleId": email
                }
                requests.put(url, headers=headers, json=payload)

                uuidCacheFile.write(userID + '\n')

                if config['userInterface'] == 'True' or config['userInterface'] == 'true':
                    print("changed Managed AppleID for: " + email)
                else:
                    pass

            elif managedAppleId == email:
                uuidCacheFile.write(userID + '\n')

                if config['userInterface'] == 'True' or config['userInterface'] == 'true':
                    print("Managed AppleID is already correct for: " + email)
                else:
                    pass

            else:
                exit('Something went wrong for user: ' + email)


def mainManagedAppleId():
    organisationUUID = config["managedAppleID"][0]["organisationUUID"]
    groupId = getGroupId(config["managedAppleID"][0]["managedAppleIDGroup"], organisationUUID)
    usersInGroup = getGroupUsers(groupId, organisationUUID)

    for i in range(len(getGroupUsers(groupId, organisationUUID))):
        changeManagedAppleId(usersInGroup[i], organisationUUID)


def main(organisationConfigNumbers):
    for orgIndex in range(organisationConfigNumbers):
        organisationUUID = config["organisation"][orgIndex]["organisationUUID"]
        groupId_1 = getGroupId(config["organisation"][orgIndex]["toGroup"], organisationUUID)
        groupId_2 = getGroupId(config["organisation"][orgIndex]["fromGroup"], organisationUUID)
        addUserToGroup(
            comparisonGroups(getGroupUsers(groupId_1, organisationUUID),
                             getGroupUsers(groupId_2, organisationUUID)),
            organisationUUID, groupId_1)


def timer(configTime):
    while True:
        main(getOrganisationNumbersFromConfig())
        if config['managedAppleID'][0]['enabled'] == 'True' or config['managedAppleID'][0]['enabled'] == 'true':
            mainManagedAppleId()
        if config['userInterface'] == 'True' or config['userInterface'] == 'true':
            print("Waiting " + str(configTime) + " minutes")
        time.sleep(int(configTime * 60))


if __name__ == '__main__':
    systemCheck()
    timer(config['timer'])
