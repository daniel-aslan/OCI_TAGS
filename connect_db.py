#! /usr/bin/env python3
import mysql.connector
import base64, logging
from oci_facts import get_compute_tags_info as gt
from check_tags import get_oci_compute_info as go
from pprint import pprint as pp

logging.basicConfig(filename='database.log', level=logging.INFO, format='%(asctime)s - %(levelna    me)s - %(message)s')

# Replace these values with your database information
host = '1.1.1.1'
user = 'someuser'
encoded_password = b'XXXXXXXXXXXXXXXXXXXXXXXX'
password = (base64.b64decode(encoded_password)).decode("ascii")
database = 'somedb'
port = 3276  # Replace with your non-standard port
dynamic_dicts = {}
dynamic_lists = []
compute_name_query = "SELECT ID FROM ComputeName WHERE DisplayName = %s"  # Adjust the WHERE clause accordingly

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

# Call the get__compute_tag_info module to get a list and dictionary
tag_dictionary, notag_list = gt(go())

##############################################
# Function to Retrieve Parent ID from ComputeName Table
def retrieve_parent_id(dicts: dict, query1):
    hosts = []
    name_parent_id = {}
    for key in dicts:
        hosts.append(key)

    cursor = connection.cursor()
    # Retrieve the 'ID' from the 'ComputeName' table
    # try:
    for name in hosts:
        n = (name,)
        cursor.execute(query1, n)
        # Fetch the 'ID' result
        compute_name_result = cursor.fetchone()
        # If the displayname is not in the db update the db
        if not compute_name_result:
            add_compute_name_query = ("INSERT INTO ComputeName (DisplayName) VALUES row(%s);")
            cursor.execute(add_compute_name_query, n)
            cursor.execute(query1, n)
            # Fetch the 'ID' result
            compute_name_result = cursor.fetchone()
            name_parent_id[name] = compute_name_result
        else:
        # Extract the 'ID' value
            name_parent_id[name] = compute_name_result

    connection.commit()
    cursor.close()
    return name_parent_id

##############################################

for instance in oci_facts:
    dynamic_dicts_name = f"{instance.display_name}.somedomain.com"
    instance_has_keys = instance.freeform_tags
    if instance_has_keys:
        dynamic_dicts[dynamic_dicts_name] = instance.freeform_tags
    else:
        dynamic_lists.append(instance.display_name)


##############################################

# Function to insert tags into the FFTags table
def insert_fftags(id_dict: dict, tag_dict: dict):
    successful_inserts = []
    cursor = connection.cursor()
    # Example query to insert data into FFTags table with the foreign key
    insert_query = (
        "INSERT INTO FFTags (parent_id, tag_name, tag_value)"
        "VALUES (%s, %s, %s)")
    # Data to be inserted, including the foreign key from ComputeName
    for host_id, pid in id_dict.items():
        if host_id not in tag_dict:
            logging.warning(f"No tags found for: {host_id} ")

        host_tag_values = tag_dict[host_id]
        successful_inserts.append(host_id)

        for ff_tag_name, ff_tag_value in host_tag_values.items():
            parentid = pid[0]
            data_to_insert = (parentid, ff_tag_name, ff_tag_value)
            try:
                cursor.execute(insert_query, data_to_insert)
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    logging.warning(f"Skipped duplicate host: {host_id} ")
                else:
                    raise

    cursor.close()
    connection.commit()

    print(""" The Following instances have been added to the DB:
              {}
          """.format(successful_inserts) )
    return successful_inserts
    
##############################################

def insert_computename(list_hosts: list):
    cursor = connection.cursor()
    add_compute_name_query = ("INSERT INTO ComputeName (DisplayName) VALUES row(%s);")
    try:
        for v in list_hosts:
            val = (v,)
            try:
                cursor.execute(add_compute_name_query, val)
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    logging.warning(f"Skipped duplicate host: {host} ")
                else:
                    raise
        #     print(e)
        #     pass
    except Exception as e:
        logging.error(f'Error: {e}')

    cursor.close()
    connection.commit()

##############################################

def call_all():
    insert_computename(notag_list)
    insert_fftags(retrieve_parent_id(tag_dictionary, compute_name_query),tag_dictionary)
    # Close the and connection
    connection.close()

def main():
    call_all()
    # insert_fftags(retrieve_parent_id(tag_dictionary, compute_name_query),tag_dictionary)

if __name__ == '__main__':
    main()
