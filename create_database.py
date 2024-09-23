import mysql.connector
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
            use_pure=True
        )
        if connection.is_connected():
            print("Connected to the database.")
        return connection
    except Error as e:
        print(f"Error while connecting to database: {e}")
        return None

def create_database():
    """Create the qsos table in the database with a UNIQUE constraint to prevent duplicates."""
    connection = connect_database()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()

        # SQL to create the qsos table with a UNIQUE constraint on (callsign, qso_date, time_on)
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS qsos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            adif_ver VARCHAR(10),
            qso_date DATE NOT NULL,
            time_on TIME NOT NULL,
            time_off TIME,
            callsign VARCHAR(20) NOT NULL,
            band VARCHAR(10),
            freq DECIMAL(10, 6),
            mode VARCHAR(10),
            submode VARCHAR(10),
            rst_sent VARCHAR(5),
            rst_rcvd VARCHAR(5),
            tx_pwr VARCHAR(10),
            operator VARCHAR(50),
            station_callsign VARCHAR(20),
            my_gridsquare VARCHAR(10),
            gridsquare VARCHAR(10),
            qth VARCHAR(100),
            name VARCHAR(50),
            my_country VARCHAR(50),
            my_cnty VARCHAR(50),
            my_state VARCHAR(50),
            my_cq_zone VARCHAR(5),
            my_itu_zone VARCHAR(5),
            country VARCHAR(50),
            cnty VARCHAR(50),
            state VARCHAR(50),
            cq_zone VARCHAR(5),
            itu_zone VARCHAR(5),
            contest_id VARCHAR(50),
            srx VARCHAR(10),
            srx_string VARCHAR(10),
            stx VARCHAR(10),
            stx_string VARCHAR(10),
            category VARCHAR(50),
            operator_category VARCHAR(50),
            eqsl_qsl_sent VARCHAR(5),
            eqsl_qsl_rcvd VARCHAR(5),
            lotw_qsl_sent VARCHAR(5),
            lotw_qsl_rcvd VARCHAR(5),
            qsl_sent VARCHAR(5),
            qsl_rcvd VARCHAR(5),
            dxcc VARCHAR(10),
            iota VARCHAR(10),
            sat_mode VARCHAR(10),
            sat_name VARCHAR(10),
            prop_mode VARCHAR(10),
            notes TEXT,
            comment TEXT,
            user_defined TEXT,
            UNIQUE KEY unique_qso (callsign, qso_date, time_on)  -- Place constraint here
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully or already exists.")
        
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()
