#! /usr/bin/env python3
# Use this as a template for the script
# https://github.com/oracle/oci-python-sdk/blob/master/examples/tag_resources_in_tenancy/tag_resources_in_tenancy.py

from pprint import pprint as pp
import base64, oci
# from pprint import pprint as pp

### Global Variables
file = ["~/.oci/config", "DEFAULT"]
config = oci.config.from_file(file_location=file[0], profile_name=file[1])
dynamic_dicts = {}
dynamic_lists = []

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
# # print the freeform_tags
for instance in oci_facts:
    dynamic_dicts_name = f"{instance.display_name}.oci.fiu.edu"
    dynamic_lists_name = f"{instance.display_name}.oci.fiu.edu"
    instance_has_keys = instance.freeform_tags
    if instance_has_keys:
        dynamic_dicts[dynamic_dicts_name] = instance.freeform_tags
    else:
        dynamic_lists.append(instance.display_name)

# pp(dynamic_dicts)
hosts = []
for key in dynamic_dicts:
    hosts.append(key)

print(hosts)
