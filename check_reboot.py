#! /usr/bin/python3
from oci_facts import get_oci_compute_info as go
from teams_notification import teams_notifications as tn

def check_reboots():
    oci_instances = go()
    dynamic_dicts = {}
    for instance in oci_instances:
        # Replace time_maintenance with whatever for future iterations
        if instance.time_maintenance_reboot_due:
            dynamic_dicts_name = f"{instance.display_name}.somedomain.local"
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
    
    tn(text_to_card)

def main():
    check_reboots()

if __name__ == "__main__":
    main()
