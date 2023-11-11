# Relution-User-Sync

## Installation && Configuration
Copy the `relution-sync.deb` file from `Linux/deb-config` to your server and run the following command:

`apt install ./relution-sync.deb` - This installs the package and all dependencies.
After the installation you can find the config file under `/etc/relution-sync/config/sample-config.json`.

Change the `sample-config.json` file to your needs and setup.

Then run the following commands:

`mv /etc/relution-sync/config/sample-config.json /etc/relution-sync/config/config.json`


You can also copy only the `relution-sync.py` and `sample-config.json` file to your server and run the script manuel.

---

```
{
  "protocol": "http/https",
  "hostname": "domain.tld",
  "port": "80/443/...",
  "accessToken": "Your created Accestoken",

  "organisation": [
    {
      "id": 1,
      "groupId_1": "To Group",
      "groupId_2": "From Group",
      "organisationUUID": "Organisation ID"
    },
    {
      "id": 2,
      "groupId_1": "To Group",
      "groupId_2": "From Group",
      "organisationUUID": "Organisation ID"
    },
    .
    .
    .
    .
  ]
}
```