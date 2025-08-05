from Services import DatabaseConnection
import paho.mqtt.client as mqtt
import datetime
import json
import uuid
import re


class MQTTToDatabaseWriter:
    """
    A class to write data from an MQTT topic to a database.
    
    This class waits for messages on a specified MQTT topic and writes the received data
    to a database using a provided DatabaseConnection instance.
    
    Attributes:
    - mqtt_client (mqtt.Client): The MQTT client instance.
    - topic (str): The MQTT topic to subscribe to.
    - db_connection (DatabaseConnection): The database connection instance.
    - table_name (str): The name of the database table to write data to.
    - columns (list): The list of columns in the database table.
    - last_message_time (datetime.datetime): The timestamp of the last received message.
    
    Methods:
    - on_connect(client, userdata, flags, rc): Callback for when the MQTT client connects to the broker.
    - on_message(client, userdata, msg): Callback for when a message is received on the subscribed topic.
    - write_to_database(data): Writes the received data to the database.
    """
    def __init__(self, topic: str, url: str, table_name: str, columns: list):
        """
        Initialize the MQTTToDatabaseWriter with a topic and database connection.
        
        Parameters:
        - topic (str): The MQTT topic to subscribe to.
        - url (str): The database URL to connect to.
        - table_name (str): The name of the database table to write data to.
        - columns (list): The list of columns in the database table.
        """
        self.mqtt_client = mqtt.Client()
        self.db = DatabaseConnection(url)
        self.topic = topic
        self.table_name = table_name
        self.columns = columns

        # Define the last message time as None initially
        self.last_message_time = None
        
        # Set up MQTT callbacks
        self.__setup_mqtt_callbacks()
        
        
    def __setup_mqtt_callbacks(self):
        """
        Set up the MQTT client callbacks for connection and message handling.
        
        This method defines the behavior of the MQTT client when it connects to the broker
        and when it receives messages on the subscribed topic.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        self.mqtt_client.on_connect = self.on_connect

        self.mqtt_client.on_message = self.on_message


    def start(self, endpoint: str, port: int, keep_alive: int = 60):
        """
        Start the MQTT client and connect to the specified endpoint and port.
        
        Parameters:
        - endpoint (str): The MQTT broker endpoint to connect to.
        - port (str): The port number of the MQTT broker.
        
        Returns:
        - None
        """
        print(f"Connecting to MQTT broker at {endpoint}:{port}")
        self.mqtt_client.connect(endpoint, port, keep_alive)
        print("Connected to MQTT broker, subscribing to vehicle telemetry topics...")
        self.mqtt_client.loop_forever()
    
    
    def on_connect(self, client, userdata, flags, rc):
        """
        Callback for when the MQTT client connects to the broker.
        
        Parameters:
        - client: The MQTT client instance
        - userdata: User defined data
        - flags: Response flags from the broker
        - rc: The connection result code (0 = success)
        """
        if rc == 0:
            print("Connected to MQTT Service!")
            # Subscribe to specific topics for units 1, 2, 3 (no wildcards to avoid issues)
            topics = [
                "U1_Combustible", "U2_Combustible", "U3_Combustible",
                "U1_Velocidad", "U2_Velocidad", "U3_Velocidad",
                "U1_Panic", "U2_Panic", "U3_Panic",
                "U1_RPM", "U2_RPM", "U3_RPM",
                "U1_Temperatura", "U2_Temperatura", "U3_Temperatura",
                "U1_Latitud", "U2_Latitud", "U3_Latitud",
                "U1_Longitud", "U2_Longitud", "U3_Longitud"
            ]
            
            success_count = 0
            for topic in topics:
                result = client.subscribe(topic)
                if result[0] == 0:
                    success_count += 1
                    print(f"✅ Subscribed to {topic}")
                else:
                    print(f"❌ Failed to subscribe to {topic}: {result}")
            
            print(f"🚐 Successfully subscribed to {success_count}/{len(topics)} topics!")
            if success_count > 0:
                print("Ready to receive vehicle telemetry data!")
        else:
            print(f"Failed to connect: {rc}. loop_forever() will retry connection")
    
    def on_message(self, client, userdata, msg):
        """
        Callback for when a message is received on the subscribed topic.
        
        Parameters:
        - client: The MQTT client instance
        - userdata: User defined data
        - msg: The message received
        """
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            print(f"📨 Received: {topic} = {payload}")
            
            # Parse the topic to extract unit and parameter
            unit_info = self._parse_topic(topic)
            if unit_info:
                print(f"🔍 Parsed: Unit {unit_info['unit_number']}, Parameter: {unit_info['parameter']}")
                self._write_to_database(unit_info, payload)
                self.last_message_time = datetime.datetime.now()
                print(f"✅ Data written to database")
            else:
                print(f"❌ Could not parse topic: {topic}")
                
        except Exception as e:
            print(f"💥 Error processing message: {e}")
            import traceback
            traceback.print_exc()
    
    def _parse_topic(self, topic):
        """
        Parse MQTT topic to extract unit ID and parameter type.
        
        Expected formats: 
        - U{unit_number}_{parameter} (e.g., U1_Combustible, U3_Velocidad, U2_Panic)
        - U{unit_number}/{parameter} (e.g., U1/Combustible, U3/Velocidad, U2/Panic)
        
        Parameters:
        - topic (str): The MQTT topic
        
        Returns:
        - dict: Dictionary with unit_id and parameter type, or None if parsing fails
        """
        # Try format with underscore first: U1_Combustible
        pattern1 = r'U(\d+)_(.+)'
        match = re.match(pattern1, topic)
        
        if match:
            unit_number = match.group(1)
            parameter = match.group(2)
            return {
                'unit_number': unit_number,
                'parameter': parameter.lower()
            }
        
        # Try format with slash: U1/Combustible  
        pattern2 = r'U(\d+)/(.+)'
        match = re.match(pattern2, topic)
        
        if match:
            unit_number = match.group(1)
            parameter = match.group(2)
            return {
                'unit_number': unit_number,
                'parameter': parameter.lower()
            }
        
        return None
    
    def _write_to_database(self, unit_info, value):
        """
        Write the received data to the appropriate database table.
        
        Parameters:
        - unit_info (dict): Dictionary with unit_number and parameter
        - value (str): The value received from MQTT
        """
        try:
            # Convert value to appropriate type
            try:
                numeric_value = float(value)
            except ValueError:
                numeric_value = None
            
            unit_number = unit_info['unit_number']
            parameter = unit_info['parameter']
            
            # Find the unit_id based on unit_number (assuming some naming convention)
            # For now, we'll generate a UUID based on unit number for demo purposes
            unit_uuid = self._get_or_create_unit_id(unit_number)
            
            current_time = datetime.datetime.now()
            
            if parameter in ['combustible', 'fuel']:
                self._update_unit_fuel_level(unit_uuid, numeric_value)
            elif parameter in ['velocidad', 'speed']:
                self._update_unit_speed(unit_uuid, numeric_value)
                self._record_speed_history(unit_uuid, numeric_value, current_time)
            elif parameter == 'panic':
                self._update_unit_panic(unit_uuid, bool(int(value)) if value.isdigit() else False)
            elif parameter == 'rpm':
                self._update_unit_rpm(unit_uuid, int(numeric_value) if numeric_value else 0)
            elif parameter in ['temperatura', 'temperature']:
                self._update_unit_temperature(unit_uuid, int(numeric_value) if numeric_value else 0)
            elif parameter in ['latitud', 'latitude']:
                # Store in a temporary location for pairing with longitude
                self._store_temp_location(unit_uuid, 'latitude', numeric_value, current_time)
            elif parameter in ['longitud', 'longitude']:
                # Store in a temporary location for pairing with latitude
                self._store_temp_location(unit_uuid, 'longitude', numeric_value, current_time)
            else:
                print(f"Unknown parameter: {parameter}")
                
        except Exception as e:
            print(f"Error writing to database: {e}")
    
    def _get_or_create_unit_id(self, unit_number):
        """
        Get or create a unit ID based on unit number.
        For demo purposes, this creates a deterministic UUID.
        """
        # Create a deterministic UUID based on unit number
        namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
        return str(uuid.uuid5(namespace, f"unit_{unit_number}"))
    
    def _update_unit_fuel_level(self, unit_id, fuel_level):
        """Update fuel level in Units table"""
        data = {
            'fuel_level': fuel_level,
            'updated_at': datetime.datetime.now()
        }
        where_clause = 'unit_id = :unit_id'
        where_params = {'unit_id': unit_id}
        self.db.update_data('Units', data, where_clause, where_params)
    
    def _update_unit_speed(self, unit_id, speed):
        """Update current speed in Units table"""
        data = {
            'current_speed': speed,
            'updated_at': datetime.datetime.now()
        }
        where_clause = 'unit_id = :unit_id'
        where_params = {'unit_id': unit_id}
        self.db.update_data('Units', data, where_clause, where_params)
    
    def _update_unit_panic(self, unit_id, panic_active):
        """Update panic button status in Units table"""
        data = {
            'panic_button_active': panic_active,
            'updated_at': datetime.datetime.now()
        }
        where_clause = 'unit_id = :unit_id'
        where_params = {'unit_id': unit_id}
        self.db.update_data('Units', data, where_clause, where_params)
    
    def _update_unit_rpm(self, unit_id, rpm):
        """Update RPM in Units table"""
        data = {
            'rpm': rpm,
            'updated_at': datetime.datetime.now()
        }
        where_clause = 'unit_id = :unit_id'
        where_params = {'unit_id': unit_id}
        self.db.update_data('Units', data, where_clause, where_params)
    
    def _update_unit_temperature(self, unit_id, temperature):
        """Update temperature in Units table"""
        data = {
            'temperature': temperature,
            'updated_at': datetime.datetime.now()
        }
        where_clause = 'unit_id = :unit_id'
        where_params = {'unit_id': unit_id}
        self.db.update_data('Units', data, where_clause, where_params)
    
    def _record_speed_history(self, unit_id, speed, timestamp):
        """Record speed in SpeedHistory table"""
        data = {
            'speed_id': str(uuid.uuid4()),
            'unit_id': unit_id,
            'speed': speed,
            'recorded_at': timestamp
        }
        self.db.insert_data('SpeedHistory', data)
    
    def _store_temp_location(self, unit_id, coord_type, value, timestamp):
        """
        Store location data in LocationHistory table
        """
        data = {
            'location_id': str(uuid.uuid4()),
            'unit_id': unit_id,
            'recorded_at': timestamp
        }
        
        if coord_type == 'latitude':
            data['latitude'] = value
            data['longitude'] = None
        else:  # longitude
            data['longitude'] = value
            data['latitude'] = None
        
        self.db.insert_data('LocationHistory', data)