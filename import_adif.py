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
            ssl_disabled=True  # Disable SSL explicitly

        )
        print("Connected to the database.")
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
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
            print(f"QSO parsed: {qso_data}")  # Print the parsed QSO for visibility
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
    
    print(f"Total QSOs parsed: {len(qsos)}")  # Print the total number of parsed QSOs
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
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        # Print what is being inserted for visibility
        print(f"Inserting QSO: {qso}")
        
        cursor.execute(insert_query, (
            qso.get('adif_ver'),
            qso.get('qso_date'),
            qso.get('time_on'),
            qso.get('time_off'),
            qso.get('call'),
            qso.get('band'),
            qso.get('freq'),
            qso.get('mode'),
            qso.get('submode'),
            qso.get('rst_sent'),
            qso.get('rst_rcvd'),
            qso.get('tx_pwr'),
            qso.get('operator'),
            qso.get('station_callsign'),
            qso.get('my_gridsquare'),
            qso.get('gridsquare'),
            qso.get('qth'),
            qso.get('name'),
            qso.get('my_country'),
            qso.get('my_cnty'),
            qso.get('my_state'),
            qso.get('my_cq_zone'),
            qso.get('my_itu_zone'),
            qso.get('country'),
            qso.get('cnty'),
            qso.get('state'),
            qso.get('cq_zone'),
            qso.get('itu_zone'),
            qso.get('contest_id'),
            qso.get('srx'),
            qso.get('srx_string'),
            qso.get('stx'),
            qso.get('stx_string'),
            qso.get('category'),
            qso.get('operator_category'),
            qso.get('eqsl_qsl_sent'),
            qso.get('eqsl_qsl_rcvd'),
            qso.get('lotw_qsl_sent'),
            qso.get('lotw_qsl_rcvd'),
            qso.get('qsl_sent'),
            qso.get('qsl_rcvd'),
            qso.get('dxcc'),
            qso.get('iota'),
            qso.get('sat_mode'),
            qso.get('sat_name'),
            qso.get('prop_mode'),
            qso.get('notes'),
            qso.get('comment'),
            qso.get('user_defined')
        ))
        connection.commit()  # Commit after every insert for visibility
        print("QSO inserted successfully.")
        
    except Error as e:
        print(f"Error inserting QSO: {e}")
        connection.rollback()  # Rollback in case of failure
    finally:
        cursor.close()

def import_adif(adif_file_path):
    """Main function to import ADIF file into the MariaDB database."""
    connection = connect_database()
    qsos = parse_adif(adif_file_path)
    
    for qso in qsos:
        # Ensure data validation before inserting
        if 'call' not in qso or not qso['call']:
            print("Skipping invalid QSO with missing call sign")
            continue
        insert_qso(connection, qso)
    
    print(f"Imported {len(qsos)} QSOs successfully.")
    
    if connection.is_connected():
        connection.commit()  # Commit all changes at once if successful
        connection.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python import_adif.py path/to/adif-file.adif")
        sys.exit(1)
    
    adif_file_path = sys.argv[1]
    import_adif(adif_file_path)
