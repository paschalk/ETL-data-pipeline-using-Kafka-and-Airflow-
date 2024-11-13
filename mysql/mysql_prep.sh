#!/bin/bash

function start_mysql {
    # Start server
    echo "Starting MySQL server..."
    sudo service mysql start
    if [ $? -ne 0 ]; then
        echo "Failed to start MySQL Server"
        exit 1
    fi
}

start_mysql

# Connect to MySQL server and execute SQL commands
mysql --host=127.0.0.1 --port=3306 --user=root --password="${MYSQL_PASSWORD}" << EOF

-- Create database tolldata
system echo 'Creating database tolldata';
CREATE DATABASE IF NOT EXISTS tolldata;

-- Create table livetolldata to store data generated by traffic simulator
system echo 'Creating table livetolldata'
USE tolldata;
CREATE TABLE IF NOT EXISTS livetolldata(
    timestamp DATETIME,
    vehicle_id INT,
    vehicle_type CHAR(15),
    toll_plaza_id SMALLINT
);
EOF

# Install kafka-python
python3 -m pip install kafka-python || { echo "Failed to install kafka-python"; exit 1; }

# Install mysql-connector-python
python3 -m pip install mysql-connector-python || { echo "Failed to install mysql-connector-python"; exit 1; }

echo "Environment Setup Completed!👌"