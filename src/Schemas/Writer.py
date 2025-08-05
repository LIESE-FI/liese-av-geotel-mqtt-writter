from Services import DatabaseConnection
import paho.mqtt.client as mqtt
import datetime


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
        self.mqtt_client.on_connect = lambda client, userdata, flags, reason_code, properties: (
            print("Connecting...") or
            print(f"Failed to connect: {reason_code}. loop_forever() will retry connection") if reason_code.is_failure else (
                print("Connected to MQTT Service!") or client.subscribe(self.topic)
            )
        )

        self.mqtt_client.on_message = lambda client, userdata, msg: print(f"{msg.topic} {msg.payload}")


    def start(self, endpoint: str, port: int, keep_alive: int = 60):
        """
        Start the MQTT client and connect to the specified endpoint and port.
        
        Parameters:
        - endpoint (str): The MQTT broker endpoint to connect to.
        - port (str): The port number of the MQTT broker.
        
        Returns:
        - None
        """
        print(f"Connecting to MQTT broker at {endpoint}:{port} (topic: {self.topic})")
        self.mqtt_client.connect(endpoint, port, keep_alive)
        print("Connected to MQTT broker, subscribing to topic...")
        self.mqtt_client.loop_forever()