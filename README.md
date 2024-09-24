This repository provides a set of scripts to manage a MariaDB database for logging Amateur Radio QSOs using the ADIF (Amateur Data Interchange Format) standard. It includes functionality for creating the database schema, importing ADIF files into the database, and exporting QSOs from the database back into ADIF format.

## Features

- **Create Database Schema**: A script that sets up a MariaDB database with appropriate fields to store ADIF QSO data.
- **ADIF Import Script**: A script to import ADIF files into the database, parsing each QSO and storing it in the relevant table.
- **ADIF Export Script**: A script that exports all QSOs stored in the database back into ADIF format, making it compatible with logging programs and online QSL services.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Database Authentication](#Authentication)
  - [Creating the Database](#creating-the-database)
  - [Importing ADIF Data](#importing-adif-data)
  - [Exporting ADIF Data](#exporting-adif-data)
- [License](#license)

## Requirements

- **MariaDB or MySQL**: Ensure MariaDB or MySQL is installed and running on your system.
- **Python 3.x**: The scripts are written in Python.
- **Python Libraries**: Required libraries can be installed via `pip`:

  ```bash
  pip install mysql-connector-python

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/adif-database-importer.git
   cd adif-database-importer
   
2. Set up your MariaDB database:

- **Update the connection details in the provided scripts (e.g., db_host, db_user, db_password).

3. Run the database setup script to create the required tables:

```bash
  python create_database.py
```
## Usage

### Authentication
To Authenticate agains the correct database fill in the file dblogin.py
```
# Database configuration (change these according to your setup)
db_host = 'localhost'
db_user = 'root'
db_password = 'letmein'
db_name = 'qso_log'
db_port = '3306'
```

### Creating the Database

The `create_database.py` script sets up the MariaDB database schema to support ADIF fields.

```bash
python create_database.py
```

This script creates a qsos table with fields for commonly used ADIF data, such as call signs, bands, frequencies, modes, and other details relevant to a QSO.

Importing ADIF Data
To import ADIF data into the database, use the import_adif.py script:

```bash
python import_adif.py path/to/adif-file.adif
```
This script will read the ADIF file, parse the QSO entries, and insert them into the qsos table in the database.

Exporting ADIF Data
To export the QSOs from the database back into ADIF format, use the export_adif.py script:

```bash
python export_adif.py output-file.adif
```
This script will query the database for all stored QSOs and write them to an ADIF file, ready for use in logging software or QSL services.

## License

This project is licensed under the GNU General Public License (GPLv3). You are free to copy, modify, and distribute this software under the terms of the GNU GPLv3. See the [LICENSE](LICENSE) file for complete details.

For more information about the GNU GPLv3 license, visit:  
[https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html)
