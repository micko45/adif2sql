import mysql.connector
import sys
import logging
from mysql.connector import Error
from dblogin import *

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_database():
    """Connect to MariaDB."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            ssl_disabled=True  # Disable SSL if not needed

        )
        logging.info("Connected to the database.")
        return connection
    except Error as e:
        logging.error(f"Error connecting to the database: {e}")
        sys.exit(1)

def parse_adif(adif_file_path):
    """Parse ADIF file and return a list of QSO dictionaries."""
    qsos = []
    qso_data = {}
    
    with open(adif_file_path, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        line = line.strip()  # Remove any leading/trailing whitespace
        
        # Logging: log each line as it's being processed
        logging.debug(f"Processing line {i + 1}: {line}")
        
        if not line:  # Skip empty lines
            logging.debug(f"Skipping empty line {i + 1}")
            continue
        
        if line.upper() == "<EOH>":  # Skip the end of header marker
            logging.debug(f"Skipping EOH at line {i + 1}")
            continue
        
        # Split the line by spaces, each part should be a valid ADIF field or <eor>
        fields = line.split()

        for field in fields:
            if field.upper() == "<EOR>":  # End of QSO record
                if qso_data:  # Only append if there's valid data
                    qsos.append(qso_data)
                    logging.debug(f"QSO added: {qso_data}")
                qso_data = {}  # Reset for next QSO
                continue
            
            # Process ADIF fields like <CALL:6>EI9ABC
            if '<' in field and '>' in field:
                field_start = field.find('<')
                field_end = field.find('>')
                
                tag_content = field[field_start + 1:field_end]
                if ':' not in tag_content:
                    logging.warning(f"Invalid tag structure: {tag_content}, skipping line {i + 1}")
                    continue
                
                field_info = tag_content.split(':')
                field_name = field_info[0].lower()

                # Ensure the field has a length part and is an integer
                try:
                    field_length = int(field_info[1])
                except (IndexError, ValueError):
                    logging.error(f"Error parsing field length for {field_name} at line {i + 1}, skipping...")
                    continue

                field_value = field[field_end + 1:field_end + 1 + field_length].strip()
                
                # Map 'call' to 'callsign'
                if field_name == 'call':
                    field_name = 'callsign'
                    
                qso_data[field_name] = field_value.strip()
    
    logging.info(f"Total QSOs parsed: {len(qsos)}")
    return qsos

def insert_qso(connection, qso):
    """Insert a single QSO into the MariaDB database."""
    try:
        cursor = connection.cursor()

        # Insert only the necessary fields to avoid errors with missing fields
        insert_query = '''
        INSERT INTO qsos (
            qso_date, time_on, callsign, band, freq, mode, rst_sent, rst_rcvd, name, qth, gridsquare, tx_pwr
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        logging.debug(f"Inserting QSO: {qso}")

        # Ensure all the required fields are present, use None for missing fields
        cursor.execute(insert_query, (
            qso.get('qso_date', None),
            qso.get('time_on', None),
            qso.get('callsign', None),  # Ensure 'callsign' is not missing
            qso.get('band', None),
            qso.get('freq', None),
            qso.get('mode', None),
            qso.get('rst_sent', None),
            qso.get('rst_rcvd', None),
            qso.get('name', None),
            qso.get('qth', None),
            qso.get('gridsquare', None),
            qso.get('tx_pwr', None)
        ))
        
        # Commit the transaction
        connection.commit()
        logging.info(f"QSO successfully inserted into the database.")
        
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            # Handle duplicate entry
            logging.warning(f"Duplicate entry detected for QSO: {qso}. Skipping insertion.")
        else:
            logging.error(f"Error inserting QSO: {e}")
            connection.rollback()  # Rollback in case of failure
    finally:
        cursor.close()

def import_adif(adif_file_path):
    """Main function to import ADIF file into the MariaDB database."""
    connection = connect_database()
    qsos = parse_adif(adif_file_path)
    
    # Insert each QSO into the database
    for qso in qsos:
        if 'callsign' not in qso or not qso['callsign']:
            logging.warning("Skipping invalid QSO with missing callsign")
            continue
        insert_qso(connection, qso)  # Insert each parsed QSO into the DB
    
    logging.info(f"Imported {len(qsos)} QSOs successfully.")
    
    if connection.is_connected():
        connection.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.error("Usage: python import_adif.py path/to/adif-file.adif")
        sys.exit(1)
    
    adif_file_path = sys.argv[1]
    import_adif(adif_file_path)
