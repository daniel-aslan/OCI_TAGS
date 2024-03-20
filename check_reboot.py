#! /usr/bin/python3
# Use this as a template for the script
# https://github.com/oracle/oci-python-sdk/blob/master/examples/tag_resources_in_tenancy/tag_resources_in_tenancy.py

from pprint import pprint as pp
import base64, pymsteams
import oci

### Global Variables
# Auth from instance principal
# signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
# config = {'region': signer.region, 'tenancy': signer.tenancy_id}
# Auth from config file
file = ["~/.oci/config", "DEFAULT"]
config = oci.config.from_file(file_location=file[0], profile_name=file[1])
dynamic_dicts = {}

# EST. connecticity to OCI
identity = oci.identity.IdentityClient(config)
core_client = oci.core.ComputeClient(config)

def get_oci_compute_info():
    all_instance_response = []
    # Get a list of compartments in the tenancy
    list_compartments_response = identity.list_compartments(
        config["tenancy"],
        compartment_id_in_subtree=True,
        access_level="ANY"
        )
    # Create an empty list to store the compartments
    compartments_list = []
    # Put compartment OCID's in empty list
    for compartment in list_compartments_response.data:
        compartments_list.append(compartment.id)
    # Iterate over the compartments to get the list of instances and there tags
    # comp_id = 
    for comp_id in compartments_list:
        list_instances_response = core_client.list_instances(
            compartment_id=comp_id,
            sort_by="TIMECREATED",
            sort_order="DESC",
            lifecycle_state="RUNNING"
            )
        
        if list_instances_response.data:
            for i in list_instances_response.data:
                all_instance_response.append(i)
    return (all_instance_response)

oci_facts = get_oci_compute_info()
# Get the instances that need to be rebooted
for instance in oci_facts:
    # Replace time_maintenance with whatever for future iterations
    if instance.time_maintenance_reboot_due:
        dynamic_dicts_name = f"{instance.display_name}.somedomain.com"
        # Register if instance has a maintence reboot:
        dynamic_dicts[dynamic_dicts_name] = str(instance.time_maintenance_reboot_due)

########## TEAMS Noticications #######################################
## This section is for sending teams notifications ####
dynamic_dicts_to_string = str(dynamic_dicts)
text_to_card = """
      The following hosts need to be rebooted for OCI Maintence purposes and will be rebooted by OCI if not rebooted by ESG:
      {} 
      """.format(dynamic_dicts_to_string)
######################################################################

def teams_notifications(message):
    encoded_teams_url = b'XXXXXXXXXX'
    teams_url = (base64.b64decode(encoded_teams_url)).decode('ascii')
    card = pymsteams.connectorcard(teams_url)
    card.text(message)
    # card.printme()
    card.send()

notify = teams_notifications(text_to_card)
