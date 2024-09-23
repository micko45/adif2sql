import mysql.connector
import sys
from mysql.connector import Error
from dblogin import *

def connect_database():
    """Connect to MariaDB."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            use_pure=True  # Use pure Python MySQL connector
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        sys.exit(1)

def parse_adif(adif_file_path):
    """Parse ADIF file and return a list of QSO dictionaries."""
    qsos = []
    qso_data = {}
    
    with open(adif_file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if line.strip() == "<eor>":  # End of record
            qsos.append(qso_data)
            qso_data = {}
            continue
        
        while '<' in line and '>' in line:
            field_start = line.find('<')
            field_end = line.find('>')
            field_info = line[field_start + 1:field_end].split(':')
            field_name = field_info[0].lower()
            field_length = int(field_info[1])
            field_value = line[field_end + 1:field_end + 1 + field_length]
            qso_data[field_name] = field_value.strip()
            line = line[field_end + 1 + field_length:]
    
    return qsos

def insert_qso(connection, qso):
    """Insert a single QSO into the MariaDB database."""
    try:
        cursor = connection.cursor()
        insert_query = '''
        INSERT INTO qsos (
            adif_ver, qso_date, time_on, time_off, `call`, band, freq, mode, submode, 
            rst_sent, rst_rcvd, tx_pwr, operator, station_callsign, my_gridsquare, 
            gridsquare, qth, name, my_country, my_cnty, my_state, my_cq_zone, my_itu_zone,
            country, cnty, state, cq_zone, itu_zone, contest_id, srx, srx_string, stx,
            stx_string, category, operator_category, eqsl_qsl_sent, eqsl_qsl_rcvd,
            lotw_qsl_sent, lotw_qsl_rcvd, qsl_sent, qsl_rcvd, dxcc, iota, sat_mode, 
            sat_name, prop_mode, notes, comment, user_defined
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
