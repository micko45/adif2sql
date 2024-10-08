import mysql.connector
from mysql.connector import Error

from dblogin import *

def create_database():
    """Create MariaDB database."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port,
            ssl_disabled=True  # Disable SSL if not needed
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        print(f"Database '{db_name}' created successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_qso_table():
    """Create QSO table in the MariaDB database."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            ssl_disabled=True  # Disable SSL if not needed
        )
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS qsos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            adif_ver VARCHAR(10),
            qso_date DATE,
            qso_date_off DATE,
            time_on TIME,
            time_off TIME,
            callsign VARCHAR(20),
            band VARCHAR(10),
            freq DECIMAL(10,6),
            mode VARCHAR(10),
            submode VARCHAR(20),
            rst_sent VARCHAR(5),
            rst_rcvd VARCHAR(5),
            tx_pwr VARCHAR(10),
            operator VARCHAR(20),
            station_callsign VARCHAR(20),
            my_gridsquare VARCHAR(10),
            gridsquare VARCHAR(10),
            qth VARCHAR(100),
            name VARCHAR(100),
            my_country VARCHAR(100),
            my_cnty VARCHAR(100),
            my_state VARCHAR(50),
            my_name VARCHAR(50),
            my_cq_zone INT,
            my_itu_zone INT,
            country VARCHAR(100),
            cnty VARCHAR(100),
            state VARCHAR(50),
            cq_zone INT,
            itu_zone INT,
            contest_id VARCHAR(50),
            srx INT,
            srx_string VARCHAR(50),
            stx INT,
            stx_string VARCHAR(50),
            category VARCHAR(50),
            operator_category VARCHAR(50),
            eqsl_qsl_sent ENUM('Y', 'N', 'Q', 'R'),
            eqsl_qsl_rcvd ENUM('Y', 'N', 'Q', 'R'),
            lotw_qsl_sent ENUM('Y', 'N', 'Q', 'R'),
            lotw_qsl_rcvd ENUM('Y', 'N', 'Q', 'R'),
            qsl_sent ENUM('Y', 'N', 'Q', 'R'),
            qsl_rcvd ENUM('Y', 'N', 'Q', 'R'),
            dxcc INT,
            iota VARCHAR(10),
            sat_mode VARCHAR(20),
            sat_name VARCHAR(50),
            prop_mode VARCHAR(20),
            notes TEXT,
            comment TEXT,
            user_defined TEXT,
            UNIQUE KEY unique_qso (callsign, qso_date, time_on)  -- Place constraint here

        );
        '''
        cursor.execute(create_table_query)
        print("Table 'qsos' created successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    create_database()
    create_qso_table()
