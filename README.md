
# Name
# OCI Verify Tags and Update as needed

Description
This repo is to create an OCI Python Function that will check all OCI Freeform tags in all instances in a tenancy. ]
Currently it is just a python script that will move to a Function that will run weekly and be triggered by new instance creations.
It will also send notifications to Teams to notify us.

The link to oracle doc for function quickstart
https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartcloudshell.htm#functionsquickstart_cloudshell

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
Download the FN CLI

```bash
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh
```

Make sure you have Docker 
```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
```
If using Docker Desktop on MacOS go into Settings > General and change file sharing from VirtioFS to osxfs(Legacy) as this causes an issue when invoking the function locally 

Start the fn server to develop locally 
This is for Local Usage Only
```bash
fn start
```
Change the runtime to whatever you are comfortable (Go, node, java, etc)
<app-name> is the name you set for the app 
```bash
fn init --runtime python3.9 <app-name>
```

```bash
cd <app-name>
```

This is for Local Usage Only
```bash
fn create app <app-name>
```

This is for Local Usage Only
```bash
fn deploy --app <app-name> --local
```

```bash
fn invoke <app-name> <func-name>
```

To deploy this to OCI once you have the function ready to deploy update the context for use with OCI
List the available contexts
```bash
fn list context
```

Select the appropriate context.  It should match the region that you are working on if not create it.
```bash
fn use context us-phoenix-1
```

Update the context with the compartment ocid where the app lives
```bash
fn up context oracle.compartment-id ocid1.compartment.oc1..aaaaaaaavotqadc73fftvx75ilmevwkpoot7qs7l3q3dzb6gumb2227oerda
```

Add the provider that establishes authetication.  This will use the OCI config file. Please set it up if you do not have it set
```bash
fn update context provider oracle
```

Set the profile of the OCI Config.  It is case sensitive.
```bash
fn update context oracle.profile <profile-name>
```

Set up the Functions server api for oci
```bash
# For PHX
fn update context api-url https://functions.us-phoenix-1.oci.oraclecloud.com

# For ASH
fn update context api-url https://functions.us-ashburn-1.oci.oraclecloud.com

# For localserver
fn update context api-url http://localhost:8080
```

Add the repo of choice.  Currently using: 
phx.ocir.io/axlax3h4t8yj
```bash
fn update context registry <region-key>.ocir.io/<tenancy-namespace>
```

Configure the compartment where the registry is located if not in the root compartment
```bash
fn update context oracle.image-compartment-id <ocid-compartment>
```

Log in to the registry 
```bash
docker login phx.ocir.io
Username:
Password
```

You can now deploy to OCI 
```bash
fn deploy --app <app-name>
```

And Invoke the Function for testing 
```bash
fn invoke <app-name> <func-name>

# to list app names use the following
fn ls app
```
Daniel Aslan