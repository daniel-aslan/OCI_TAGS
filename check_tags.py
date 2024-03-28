#! /usr/bin/env ptyhon3

from oci_facts import get_compute_tags_info as gt
from oci_facts import get_oci_compute_info as go
from teams_notification import teams_notifications as tn

def check_tags():
    tag_dictionary, notag_list = gt(go())

    # ## This section is for sending teams notifications ####
    dynamic_dicts_to_string = str(tag_dictionary)
    dynamic_list_to_strings = ','.join(str(compute) for compute in notag_list)
    text_to_card = """
        The following hosts have freeform tags:
        {}
        The following hosts have no freeform tags:
        {}
        """.format(dynamic_dicts_to_string, dynamic_list_to_strings)

    tn(text_to_card)

def main():
    check_tags()

if __name__ == '__main__':
    main()
