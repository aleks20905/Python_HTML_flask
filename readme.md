# IoT Brick Telemetry Server v2 

## Project Description

This project is an IoT telemetry server that listens for incoming connections from IoT devices, receives telemetry data, and stores it in a PostgreSQL database. The server is designed to handle multiple connections simultaneously using multithreading.


- **Socket Server**: Listens for incoming connections on a specified port.
- **Data Reception**: Receives telemetry data from IoT devices.
- **Data Parsing**: Parses the received data into a structured format.
- **Database Storage**: Stores the parsed telemetry data into a PostgreSQL database.
- **Multithreading**: Handles multiple client connections concurrently.

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Required Python packages: `psycopg2`

### Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/aleks20905/Python_HTML_flask.git
    cd Python_HTML_flask
    ```

2. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up the PostgreSQL database not needed for app.py**:
    - Ensure PostgreSQL is installed and running.
    - Create a database named `iotBrick`.
    - Create a table named `ftest` with the following schema:
        ```sql
        CREATE TABLE ftest (
            id SERIAL PRIMARY KEY,
            device VARCHAR(50),
            temp1 FLOAT,
            temp2 FLOAT,
            temp3 FLOAT,
            temp4 FLOAT,
            state1 VARCHAR(50),
            time TIMESTAMP
        );
        ```

4. **Update the database connection settings** in the script if necessary:
    ```python
    hostname = 'localhost'
    database = 'iotBrick'
    username = 'postgres'
    pwd = 'postgres'
    port_id = 5432
    ```

## Usage

1. **Start the server**:
    ```sh
    python v2\app.py
    ```

2. **Server Output**:
    - The server will start listening for incoming connections on the specified port.
    - When a new connection is established, it will print a message indicating the new connection.
    - The server will receive telemetry data, parse it, and store it in the PostgreSQL database.
    - If a client disconnects, it will print a message indicating the disconnection.

# Code Explanation

The code utilizes Flask to create a web application for interacting with the telemetry data and alarms.
SQLAlchemy facilitates database interactions.
Models define the structure of data stored in the PostgreSQL database.
Functions handle data retrieval, processing, and manipulation.
Routes map URLs to specific functionalities within the application.

## Key Functionalities

- **Retrieve and display the latest telemetry data for all devices**: The application fetches the most recent telemetry readings from the database and presents them in a user-friendly format.
  
- **View individual device pages with detailed telemetry and alarm information**: Each device has a dedicated page displaying its telemetry history and any associated alarms, providing detailed insights into its performance and issues.
  
- **Monitor the connection status of devices**: The application continuously checks and reports the connection status of each device, helping users ensure all devices are online and functioning correctly.
  
- **Manage alarm thresholds and configurations**: Users can set and adjust alarm thresholds and configurations through the web interface, allowing for customized monitoring and alerting.
  
- **Download all telemetry data as a CSV file**: The application includes functionality for exporting the telemetry data into a CSV file, facilitating offline analysis and reporting.

## Additional Considerations

- **Error handling mechanisms**: Implementing robust error handling ensures the application can gracefully handle unexpected issues, providing a smooth user experience.
  
- **Security measures**: For production environments, it is crucial to implement authentication and authorization to secure the application and protect sensitive data.
  
- **Database optimization and server scalability**: As the dataset and number of connections grow, exploring techniques for optimizing the database and scaling the server will be important for maintaining performance and reliability.


