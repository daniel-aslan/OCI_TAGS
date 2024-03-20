#! /usr/bin/env python3
import mysql.connector
import base64, logging
from check_tags import get_oci_compute_info as go

# Replace these values with your database information
host = '1.1.1.1'
user = 'someuser'
encoded_password = b'XXXXXXXXXXXXXXXXXXXXXXXX'
password = (base64.b64decode(encoded_password)).decode("ascii")
database = 'somedb'
port = 3276  # Replace with your non-standard port
logging.basicConfig(filename='database.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

##############################################
# Example query
# query_select = "SELECT * FROM sometable_fftags"
# Execute the query
# cursor1.execute(query_select)
# Fetch all the results
# results = cursor1.fetchall()
# Process the results (print in this example)
# for row in results:
#     print(row)
# print("1st cursor")
##############################################
data_to_insert = (compute_name_id, tag_name, tag_value)

dynamic_dicts = {}
dynamic_lists = []
oci_facts = go()
compute_name_query = "SELECT ID FROM somedb WHERE sometable = %s"  # Adjust the WHERE clause accordingly

for instance in oci_facts:
    dynamic_dicts_name = f"{instance.display_name}.somedomain.com"
    instance_has_keys = instance.freeform_tags
    if instance_has_keys:
        dynamic_dicts[dynamic_dicts_name] = instance.freeform_tags
    else:
        dynamic_lists.append(instance.display_name)


##############################################
# Function to Retrieve Parent ID from somedb Table
def retrieve_parent_id(dicts, query1):
    hosts = []
    name_parent_id = {}
    for key in dicts:
        hosts.append(key)

    cursor = connection.cursor()
    # Retrieve the 'ID' from the 'somedb' table
    # try:
    for name in hosts:
        print(name)
        n = (name,)
        cursor.execute(query1, n)
        # Fetch the 'ID' result
        compute_name_result = cursor.fetchone()
        # If the displayname is not in the db update the db
        if not compute_name_result:
            add_compute_name_query = ("INSERT INTO somedb (sometable) VALUES row(%s);")
            cursor.execute(add_compute_name_query, n)
            cursor.execute(query1, n)
            # Fetch the 'ID' result
            compute_name_result = cursor.fetchone()
            name_parent_id[name] = compute_name_result
        else:
        # Extract the 'ID' value
            name_parent_id[name] = compute_name_result
    # except mysql.connector.Error as e:
        # logging.error(f'Error: {e}')

    # if name_parent_id not:
        # insert_computename
    connection.commit()
    cursor.close()
    return name_parent_id
##############################################
    
##############################################
# Function to insert tags into the sometable_fftags table
def insert_fftags(tag_dict, tag_key, tag_value):   
    insert_query = (
        "INSERT INTO sometable_fftags (parent_id, tag_name, tag_value)"
        "VALUES (%s, %s, %s)")
    data_to_insert = (parent_id, tag_key, tag_value)
    cursor = connection.cursor()
    # Example query to insert data into sometable_fftags table with the foreign key
    # Data to be inserted, including the foreign key from somedb
    
    # Execute the insert query with the data
    cursor.execute(insert_query, data_to_insert)
    cursor.close() 

##############################################

def insert_computename(list_hosts):
    cursor = connection.cursor()
    add_compute_name_query = ("INSERT INTO somedb (sometable) VALUES row(%s);")
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
        # print(add_compute_name_query, add_compute_name_value)




# insert_computename(dynamic_lists)
insert_fftags(retrieve_parent_id(dynamic_dicts, compute_name_query))

# Commit the changes to the database
# connection.commit()

# Close the and connection
# connection.close()
