#! /usr/bin/env python3
import oci
from pprint import pprint as pp

### Global Variables
# Auth from instance principal
# signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
# config = {'region': signer.region, 'tenancy': signer.tenancy_id}
# Auth from config file
file = ["~/.oci/config", "DEFAULT"]
config = oci.config.from_file(file_location=file[0], profile_name=file[1])

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

def get_compute_tags_info(oci_list: list):
    dynamic_lists = []
    dynamic_dicts = {}
    for instance in oci_list:
         # Add the somedomain.local to the displayname from oci sdk
         fqdn_name = f"{instance.display_name}.somedomain.local"
         # IF there are tags add it to the dynamic dictionary for adding the tags to the db later
         if instance.freeform_tags:
             dynamic_dicts[fqdn_name] = instance.freeform_tags
         # Else make a list so we know what instances still need tags
         else:
             dynamic_lists.append(fqdn_name)
    return dynamic_dicts, dynamic_lists

def main():
    pp(get_oci_compute_info())


if __name__ == "__main__":
    main()
