import mysql.connector
from mysql.connector import Error
import sys

# Database configuration (update these according to your setup)
db_host = 'localhost'
db_user = 'root'
db_password = 'your_password'
db_name = 'adif_log'

def connect_database():
    """Connect to MariaDB."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        sys.exit(1)

def fetch_qsos(connection):
    """Fetch all QSOs from the database."""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM qsos;")
        qsos = cursor.fetchall()
        return qsos
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()

def adif_format(qso):
    """Convert a single QSO to ADIF format."""
    adif_entry = ""
    
    for key, value in qso.items():
        if value is not None:
            if isinstance(value, (str, int, float)):
                value_str = str(value)
                adif_entry += f"<{key.upper()}:{len(value_str)}>{value_str} "
    
    adif_entry += "<eor>\n"
    return adif_entry

def export_to_adif(qsos, output_file):
    """Export QSO data to an ADIF file."""
    with open(output_file, 'w') as file:
        file.write("<ADIF_VER:5>3.1.0\n")
        file.write("<EOH>\n\n")  # End of header
        
        for qso in qsos:
            file.write(adif_format(qso))

def export_adif(output_file):
    """Main function to export QSOs to an ADIF file."""
    connection = connect_database()
    qsos = fetch_qsos(connection)
    
    if qsos:
        export_to_adif(qsos, output_file)
        print(f"Exported {len(qsos)} QSOs to {output_file}.")
    else:
        print("No QSOs found to export.")
    
    if connection.is_connected():
        connection.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python export_adif.py output-file.adif")
        sys.exit(1)
    
    output_file = sys.argv[1]
    export_adif(output_file)

