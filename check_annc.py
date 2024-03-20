#! /usr/bin/env ptyhon3

from pprint import pprint as pp
import base64, pymsteams, oci

### Global Variables
# Auth from instance principal
# signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
# config = {'region': signer.region, 'tenancy': signer.tenancy_id}
# Auth from config file
file = ["~/.oci/config", "DEFAULT"]
config = oci.config.from_file(file_location=file[0], profile_name=file[1])

# EST. connecticity to OCI
#identity = oci.identity.IdentityClient(config)
#core_client = oci.core.ComputeClient(config)
announcements_service_client = oci.announcements_service.AnnouncementClient(config)
comp = "ocid1.tenancy.oc1..XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

def get_oci_annc(comp_id):
    list_announcements_response = announcements_service_client.list_announcements(
        compartment_id=comp_id,
        sort_by="timeCreated",
        sort_order="ASC",
        page=100,
        should_show_only_latest_in_chain=True,
        # should_show_only_latest_in_chain=False,
    )
    # for announce in list_announcements_response:
    # pp(list_announcements_response.data.items[0])
    list_annc = list_announcements_response.data.items
    for a in list_annc: 
    # pp(list_annc)
        # list_annc.append(announce)# pp(list_announcements_response.data)
        print(a.summary)
        print(a.announcement_type)
        print(a.services)
        print(a.time_created)
        print(a.affected_regions)
        pp('#' * 40)

get_oci_annc(comp)
