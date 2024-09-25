import mysql.connector
import logging
import sys
from dblogin import *  # Import database login info (db_host, db_user, db_password, db_name, db_port)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_help():
    """Prints the help message with usage information."""
    help_message = """
    Usage: python export_adif.py [output_file.adi]

    Export QSOs from the database to an ADIF file.

    Arguments:
        output_file.adi   The path to the output ADIF file where the QSOs will be saved.
    
    Example:
        python export_adif.py /path/to/output.adif
    """
    print(help_message)
    logging.info("Displayed help message.")

def connect_database():
    """Connect to MariaDB with ssl_disabled."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            ssl_disabled=True  # Disable SSL if not needed
        )
        if connection.is_connected():
            logging.info("Connected to the database.")
        return connection
    except mysql.connector.Error as e:
        logging.error(f"Error while connecting to the database: {e}")
        return None

def fetch_qsos(connection):
    """Fetch all QSOs from the database."""
    try:
        cursor = connection.cursor(dictionary=True)
        fetch_query = "SELECT * FROM qsos"
        cursor.execute(fetch_query)
        qsos = cursor.fetchall()
        logging.info(f"Fetched {len(qsos)} QSOs from the database.")
        return qsos
    except mysql.connector.Error as e:
        logging.error(f"Error fetching QSOs: {e}")
        return []
    finally:
        cursor.close()

def format_adif(qsos):
    """Format QSOs into ADIF format."""
    adif_lines = []
    
    # Add ADIF header
    adif_lines.append("<ADIF_VER:5>3.1.0")
    adif_lines.append("<EOH>\n")
    
    # Helper function to format and add a field only if it's not empty or None
    def add_field(tag, value, data_type=None):
        nonlocal adif_line
        if value:
            value_str = str(value).strip()
            # Format date and time values
            if data_type == 'D':
                # Convert date to YYYYMMDD
                value_str = format_date(value_str)
            elif data_type == 'T':
                # Convert time to HHMMSS
                value_str = format_time(value_str)
            length = len(value_str)
            # Include data type if provided
            if data_type:
                adif_line += f"<{tag}:{length}:{data_type}>{value_str}"
            else:
                adif_line += f"<{tag}:{length}>{value_str}"
    
    # Functions to format date and time strings
    def format_date(value):
        # Assume value is in 'YYYY-MM-DD' or similar format
        return ''.join(filter(str.isdigit, value))[:8]
    
    def format_time(value):
        # Assume value is in 'HH:MM:SS' or similar format
        return ''.join(filter(str.isdigit, value))[:6]
    
    # Convert each QSO into ADIF format
    for qso in qsos:
        adif_line = ""
        
        # Add fields only if they contain values, include data types where appropriate
        add_field("QSO_DATE", qso.get('qso_date'), data_type='D')
        add_field("QSO_DATE_OFF", qso.get('qso_date_off'), data_type='D')
        add_field("TIME_ON", qso.get('time_on'), data_type='T')
        add_field("TIME_OFF", qso.get('time_off'), data_type='T')
        add_field("CALL", qso.get('callsign'))
        add_field("BAND", qso.get('band'))
        add_field("FREQ", qso.get('freq'), data_type='N')
        add_field("MODE", qso.get('mode'))
        add_field("SUBMODE", qso.get('submode'))
        add_field("RST_SENT", qso.get('rst_sent'))
        add_field("RST_RCVD", qso.get('rst_rcvd'))
        add_field("TX_PWR", qso.get('tx_pwr'))
        add_field("OPERATOR", qso.get('operator'))
        add_field("STATION_CALLSIGN", qso.get('station_callsign'))
        add_field("MY_GRIDSQUARE", qso.get('my_gridsquare'))
        add_field("GRIDSQUARE", qso.get('gridsquare'))
        add_field("QTH", qso.get('qth'))
        add_field("NAME", qso.get('name'))
        add_field("MY_COUNTRY", qso.get('my_country'))
        add_field("MY_CNTY", qso.get('my_cnty'))
        add_field("MY_STATE", qso.get('my_state'))
        add_field("MY_NAME", qso.get('my_name'))
        add_field("MY_CQ_ZONE", qso.get('my_cq_zone'))
        add_field("MY_ITU_ZONE", qso.get('my_itu_zone'))
        add_field("COUNTRY", qso.get('country'))
        add_field("CNTY", qso.get('cnty'))
        add_field("STATE", qso.get('state'))
        add_field("CQ_ZONE", qso.get('cq_zone'))
        add_field("ITU_ZONE", qso.get('itu_zone'))
        add_field("CONTEST_ID", qso.get('contest_id'))
        add_field("SRX", qso.get('srx'))
        add_field("STX", qso.get('stx'))
        add_field("CATEGORY", qso.get('category'))
        add_field("OPERATOR_CATEGORY", qso.get('operator_category'))
        add_field("EQSL_QSL_SENT", qso.get('eqsl_qsl_sent'))
        add_field("EQSL_QSL_RCVD", qso.get('eqsl_qsl_rcvd'))
        add_field("LOTW_QSL_SENT", qso.get('lotw_qsl_sent'))
        add_field("LOTW_QSL_RCVD", qso.get('lotw_qsl_rcvd'))
        add_field("DXCC", qso.get('dxcc'))
        add_field("IOTA", qso.get('iota'))
        add_field("SAT_MODE", qso.get('sat_mode'))
        add_field("SAT_NAME", qso.get('sat_name'))
        add_field("PROP_MODE", qso.get('prop_mode'))
        add_field("NOTES", qso.get('notes'))
        add_field("COMMENT", qso.get('comment'))
        add_field("USER_DEFINED", qso.get('user_defined'))
    
        # Only add the line if it has content
        if adif_line.strip():
            adif_line += "<EOR>\n"  # End of record
            adif_lines.append(adif_line)
            logging.debug(f"Formatted QSO for {qso.get('callsign', 'UNKNOWN')}: {adif_line.strip()}")
    
    return adif_lines

def export_adif(adif_file_path):
    """Export all QSOs from the database to an ADIF file."""
    connection = connect_database()
    if connection is None:
        logging.error("Failed to connect to the database. Exiting.")
        return
    
    qsos = fetch_qsos(connection)
    if not qsos:
        logging.warning("No QSOs found in the database. Exiting.")
        return
    
    adif_lines = format_adif(qsos)
    
    # Write to ADIF file
    try:
        with open(adif_file_path, 'w') as file:
            file.writelines(adif_lines)
        logging.info(f"Exported {len(qsos)} QSOs to {adif_file_path}")
    except IOError as e:
        logging.error(f"Error writing to ADIF file: {e}")
    
    if connection.is_connected():
        connection.close()

if __name__ == '__main__':
    # Check if no arguments or incorrect arguments are provided
    if len(sys.argv) != 2:
        logging.error("No output file specified or too many arguments.")
        print_help()
        sys.exit(1)

    adif_file_path = sys.argv[1]

    # Check if the file has a .adif extension
    if not adif_file_path.lower().endswith('.adi'):
        logging.error("Invalid file extension. ADIF files should have the .adi extension.")
        print_help()
        sys.exit(1)

    export_adif(adif_file_path)
