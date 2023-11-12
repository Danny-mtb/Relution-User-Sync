# Relution-User-Sync

## Installation && Configuration
Copy the `relution-sync.deb` file from `Linux/deb-config` to your server and run the following command:

`apt install ./relution-sync.deb` - This installs the package and all dependencies.
After the installation you can find the config file under `/etc/relution-sync/config/sample-config.json`.

Change the `sample-config.json` file to your needs and setup.

Then run the following commands:

Rename the config file: `mv /etc/relution-sync/config/sample-config.json /etc/relution-sync/config/config.json`
Enable and start the service: `systemctl enable relution-sync.service && systemctl start relution-sync.service`


You can also copy only the `relution-sync.py` and `sample-config.json` file to your server and run the script manuel.

---

```
{
  "protocol": "",
  "hostname": "",
  "port": "",
  "accessToken": "",
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