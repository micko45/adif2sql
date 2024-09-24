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
    
    # Convert each QSO into ADIF format
    for qso in qsos:
        adif_line = (
            f"<QSO_DATE:{len(str(qso['qso_date']))}>{qso['qso_date']}"
            f" <TIME_ON:{len(str(qso['time_on']))}>{qso['time_on']}"
            f" <TIME_OFF:{len(str(qso['time_off'])) if qso['time_off'] else '0'}>{qso['time_off'] if qso['time_off'] else ''}"
            f" <CALL:{len(qso['callsign'])}>{qso['callsign']}"
            f" <BAND:{len(qso['band']) if qso['band'] else '0'}>{qso['band'] if qso['band'] else ''}"
            f" <FREQ:{len(str(qso['freq'])) if qso['freq'] else '0'}>{qso['freq'] if qso['freq'] else ''}"
            f" <MODE:{len(qso['mode']) if qso['mode'] else '0'}>{qso['mode'] if qso['mode'] else ''}"
            f" <SUBMODE:{len(qso['submode']) if qso['submode'] else '0'}>{qso['submode'] if qso['submode'] else ''}"
            f" <RST_SENT:{len(qso['rst_sent']) if qso['rst_sent'] else '0'}>{qso['rst_sent'] if qso['rst_sent'] else ''}"
            f" <RST_RCVD:{len(qso['rst_rcvd']) if qso['rst_rcvd'] else '0'}>{qso['rst_rcvd'] if qso['rst_rcvd'] else ''}"
            f" <TX_PWR:{len(str(qso['tx_pwr'])) if qso['tx_pwr'] else '0'}>{qso['tx_pwr'] if qso['tx_pwr'] else ''}"
            f" <OPERATOR:{len(qso['operator']) if qso['operator'] else '0'}>{qso['operator'] if qso['operator'] else ''}"
            f" <STATION_CALLSIGN:{len(qso['station_callsign']) if qso['station_callsign'] else '0'}>{qso['station_callsign'] if qso['station_callsign'] else ''}"
            f" <MY_GRIDSQUARE:{len(qso['my_gridsquare']) if qso['my_gridsquare'] else '0'}>{qso['my_gridsquare'] if qso['my_gridsquare'] else ''}"
            f" <GRIDSQUARE:{len(qso['gridsquare']) if qso['gridsquare'] else '0'}>{qso['gridsquare'] if qso['gridsquare'] else ''}"
            f" <QTH:{len(qso['qth']) if qso['qth'] else '0'}>{qso['qth'] if qso['qth'] else ''}"
            f" <NAME:{len(qso['name']) if qso['name'] else '0'}>{qso['name'] if qso['name'] else ''}"
            f" <MY_COUNTRY:{len(qso['my_country']) if qso['my_country'] else '0'}>{qso['my_country'] if qso['my_country'] else ''}"
            f" <MY_CNTY:{len(qso['my_cnty']) if qso['my_cnty'] else '0'}>{qso['my_cnty'] if qso['my_cnty'] else ''}"
            f" <MY_STATE:{len(qso['my_state']) if qso['my_state'] else '0'}>{qso['my_state'] if qso['my_state'] else ''}"
            f" <MY_CQ_ZONE:{len(str(qso['my_cq_zone'])) if qso['my_cq_zone'] else '0'}>{qso['my_cq_zone'] if qso['my_cq_zone'] else ''}"  # Convert to string
            f" <MY_ITU_ZONE:{len(str(qso['my_itu_zone'])) if qso['my_itu_zone'] else '0'}>{qso['my_itu_zone'] if qso['my_itu_zone'] else ''}"  # Convert to string
            f" <COUNTRY:{len(qso['country']) if qso['country'] else '0'}>{qso['country'] if qso['country'] else ''}"
            f" <CNTY:{len(qso['cnty']) if qso['cnty'] else '0'}>{qso['cnty'] if qso['cnty'] else ''}"
            f" <STATE:{len(qso['state']) if qso['state'] else '0'}>{qso['state'] if qso['state'] else ''}"
            f" <CQ_ZONE:{len(str(qso['cq_zone'])) if qso['cq_zone'] else '0'}>{qso['cq_zone'] if qso['cq_zone'] else ''}"  # Convert to string
            f" <ITU_ZONE:{len(str(qso['itu_zone'])) if qso['itu_zone'] else '0'}>{qso['itu_zone'] if qso['itu_zone'] else ''}"  # Convert to string
            f" <CONTEST_ID:{len(qso['contest_id']) if qso['contest_id'] else '0'}>{qso['contest_id'] if qso['contest_id'] else ''}"
            f" <SRX:{len(qso['srx']) if qso['srx'] else '0'}>{qso['srx'] if qso['srx'] else ''}"
            f" <STX:{len(qso['stx']) if qso['stx'] else '0'}>{qso['stx'] if qso['stx'] else ''}"
            f" <CATEGORY:{len(qso['category']) if qso['category'] else '0'}>{qso['category'] if qso['category'] else ''}"
            f" <OPERATOR_CATEGORY:{len(qso['operator_category']) if qso['operator_category'] else '0'}>{qso['operator_category'] if qso['operator_category'] else ''}"
            f" <EQSL_QSL_SENT:{len(qso['eqsl_qsl_sent']) if qso['eqsl_qsl_sent'] else '0'}>{qso['eqsl_qsl_sent'] if qso['eqsl_qsl_sent'] else ''}"
            f" <EQSL_QSL_RCVD:{len(qso['eqsl_qsl_rcvd']) if qso['eqsl_qsl_rcvd'] else '0'}>{qso['eqsl_qsl_rcvd'] if qso['eqsl_qsl_rcvd'] else ''}"
            f" <LOTW_QSL_SENT:{len(qso['lotw_qsl_sent']) if qso['lotw_qsl_sent'] else '0'}>{qso['lotw_qsl_sent'] if qso['lotw_qsl_sent'] else ''}"
            f" <LOTW_QSL_RCVD:{len(qso['lotw_qsl_rcvd']) if qso['lotw_qsl_rcvd'] else '0'}>{qso['lotw_qsl_rcvd'] if qso['lotw_qsl_rcvd'] else ''}"
            f" <DXCC:{len(str(qso['dxcc'])) if qso['dxcc'] else '0'}>{qso['dxcc'] if qso['dxcc'] else ''}"  # Convert to string
            f" <IOTA:{len(qso['iota']) if qso['iota'] else '0'}>{qso['iota'] if qso['iota'] else ''}"
            f" <SAT_MODE:{len(qso['sat_mode']) if qso['sat_mode'] else '0'}>{qso['sat_mode'] if qso['sat_mode'] else ''}"
            f" <SAT_NAME:{len(qso['sat_name']) if qso['sat_name'] else '0'}>{qso['sat_name'] if qso['sat_name'] else ''}"
            f" <PROP_MODE:{len(qso['prop_mode']) if qso['prop_mode'] else '0'}>{qso['prop_mode'] if qso['prop_mode'] else ''}"
            f" <NOTES:{len(qso['notes']) if qso['notes'] else '0'}>{qso['notes'] if qso['notes'] else ''}"
            f" <COMMENT:{len(qso['comment']) if qso['comment'] else '0'}>{qso['comment'] if qso['comment'] else ''}"
            f" <USER_DEFINED:{len(qso['user_defined']) if qso['user_defined'] else '0'}>{qso['user_defined'] if qso['user_defined'] else ''}"
            " <eor>\n"
        )
        adif_lines.append(adif_line)
        logging.debug(f"Formatted QSO for {qso['callsign']}: {adif_line.strip()}")
    
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
