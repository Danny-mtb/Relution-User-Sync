# Relution-User-Sync

This program is designed to add users from one group to another group. This is necessary if, for example, you want to move users from a certain AzureAD group to a relution group in order to enable a sync to an Apple ASM.

## Installation
Copy the `relution-sync.deb` file from `Linux/deb-config` to your server and run the following command:

This installs the package and all dependencies: `apt install ./relution-sync.deb`

After the installation you can find the config file under `/etc/relution-sync/config/sample-config.json`.

Change the `sample-config.json` file to your needs and setup.

<br>

Then run the following commands:

Rename the config file: `mv /etc/relution-sync/config/sample-config.json /etc/relution-sync/config/config.json`

Enable and start the service: `systemctl enable relution-sync.service && systemctl start relution-sync.service`

<br>

You can also copy only the `relution-sync.py` and `sample-config.json` file to your server and run the script manuel.

<br>

## Configuration Description

```
{
  "protocol": "", // http or https
  "hostname": "", // like 'sub.domain.tld'
  "port": "", // 80, 443, ...
  "accessToken": "", // generated token from 'my Profile'
  "timer": 1, // in minutes

  "organisation": [
    {
      "id": 1,
      "toGroup": "", // Group name in Relution
      "fromGroup": "", // Group name in Relution
      "organisationUUID": "" // Organisation ID in Relution from the URL
    },
    {
      "id": 2,
      "toGroup": "",
      "fromGroup": "",
      "organisationUUID": ""
    },
    .
    .
    .
    .
  ]
}
```
