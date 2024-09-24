import mysql.connector
import logging
import sys
from dblogin import *  # Import database login info (db_host, db_user, db_password, db_name, db_port)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_help():
    """Prints the help message with usage information."""
    help_message = """
    Usage: python export_adif.py [output_file.adif]

    Export QSOs from the database to an ADIF file.

    Arguments:
        output_file.adif   The path to the output ADIF file where the QSOs will be saved.
    
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
            f" <CALL:{len(qso['callsign'])}>{qso['callsign']}"
            f" <BAND:{len(qso['band'])}>{qso['band']}"
            f" <FREQ:{len(str(qso['freq']))}>{qso['freq']}"
            f" <MODE:{len(qso['mode'])}>{qso['mode']}"
            f" <RST_SENT:{len(qso['rst_sent'])}>{qso['rst_sent']}"
            f" <RST_RCVD:{len(qso['rst_rcvd'])}>{qso['rst_rcvd']}"
            f" <NAME:{len(qso['name'])}>{qso['name']}"
            f" <QTH:{len(qso['qth'])}>{qso['qth']}"
            f" <GRIDSQUARE:{len(qso['gridsquare'])}>{qso['gridsquare']}"
            f" <TX_PWR:{len(str(qso['tx_pwr']))}>{qso['tx_pwr']}"
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
    if not adif_file_path.lower().endswith('.adif'):
        logging.error("Invalid file extension. ADIF files should have the .adif extension.")
        print_help()
        sys.exit(1)

    export_adif(adif_file_path)
