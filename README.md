# Relution-User-Sync
enable service 

## Installation
Change the `/etc/relution-sync/config/sample-config.json` file to your needs and setup.

Then run the following commands:

`mv /etc/relution-sync/config/sample-config.json /etc/relution-sync/config/config.json`

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