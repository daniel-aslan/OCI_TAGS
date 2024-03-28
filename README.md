
# Name
# OCI Verify Tags and Update as needed

Description
This repo is to create an OCI Python Function that will check all OCI Freeform tags in all instances in a tenancy. ]
Currently it is just a python script that will move to a Function that will run weekly and be triggered by new instance creations.
It will also send notifications to Teams to notify us.

The link to oracle doc for function quickstart
https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartcloudshell.htm#functionsquickstart_cloudshell

When running the below command it will send a teams message to the channel that is configured with 
the hostnames of the instances that do and do not have freeform tags.

It will also notify the teams channel if any instances are scheduled for reboots due to hardware isues.  

It will also update a db so that we can do verification in future iterations.

## Dependencies
For local development 
- OCI Config Credentials (or Instance Principal)
- Oracle Container Registry Repo Credentials
- Oracle Container Registry info
- Oracle Function OCID
- Oracle Compartment OCID (compartment that will own the app)
- FN client or OCI CLI
    https://github.com/fnproject

## Installation / Usage
To run the script currently from the root directory use the following command:

```python
python3 main.py
```


Daniel Aslan  
daniel-aslan (github)
