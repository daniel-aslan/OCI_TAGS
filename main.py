#! /usr/bin/env python3
from check_tags import check_tags
from oci_facts import get_compute_tags_info as gt
from connect_db import call_all
from check_reboot import check_reboots

def main():
    check_reboots()
    check_tags()
    call_all()

if __name__ == "__main__":
    main()
