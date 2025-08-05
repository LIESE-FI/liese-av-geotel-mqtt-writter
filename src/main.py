import os
import threading
from dotenv import load_dotenv
from Schemas import MQTTToDatabaseWriter

# MQTT topics to subscribe to - using wildcard to catch all unit topics
TOPICS = ["U+_Combustible", "U+_Velocidad", "U+_Panic", "U+_RPM", "U+_Temperatura", "U+_Latitud", "U+_Longitud"]

def __main__():
    """
    Main function to initialize and run the MQTTToDatabaseWriter.
    
    This function loads environment variables, initializes the MQTTToDatabaseWriter with
    wildcard topics to catch all unit messages, and starts the MQTT client.
    
    Returns:
    - None
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the database URL from environment variables
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set.")
    
    # Get MQTT configuration from environment variables
    mqtt_host = os.getenv("MQTT_HOST", "localhost")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
    mqtt_keepalive = int(os.getenv("MQTT_KEEPALIVE", "60"))
    
    print(f"Starting MQTT to Database Writer...")
    print(f"Database URL: {db_url}")
    print(f"MQTT Broker: {mqtt_host}:{mqtt_port}")
    
    # Initialize the MQTTToDatabaseWriter - topic will be ignored since we subscribe to multiple topics in on_connect
    writer = MQTTToDatabaseWriter(
        topic="vehicle_telemetry",  # Descriptive name, not used for subscription
        url=db_url,
        table_name="Units",  # Main table for unit data
        columns=["unit_id", "fuel_level", "current_speed", "panic_button_active", "rpm", "temperature", "updated_at"]
    )
    
    try:
        # Start the MQTT client loop
        writer.start(
            endpoint=mqtt_host,
            port=mqtt_port,
            keep_alive=mqtt_keepalive
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
        writer.db.close()
    except Exception as e:
        print(f"Error: {e}")
        writer.db.close()
        
if __name__ == "__main__":
    __main__()