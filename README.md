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
  - [Creating the Database](#creating-the-database)
  - [Importing ADIF Data](#importing-adif-data)
  - [Exporting ADIF Data](#exporting-adif-data)
- [Contributing](#contributing)
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
Copy code
python create_database.py
