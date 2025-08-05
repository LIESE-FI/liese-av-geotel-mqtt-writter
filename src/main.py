import os
from dotenv import load_dotenv
from Schemas import MQTTToDatabaseWriter

TOPICS = ["test"]

def __main__():
    """
    Main function to initialize and run the MQTTToDatabaseWriter.
    
    This function loads environment variables, initializes the MQTTToDatabaseWriter with
    the specified topic, database URL, table name, and columns, and starts the MQTT client loop.
    
    Returns:
    - None
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the database URL from environment variables
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set.")
    
    # Initialize the MQTTToDatabaseWriter with the specified parameters
    for topic in TOPICS:
        writer = MQTTToDatabaseWriter(
            topic=topic,
            url=db_url,
            table_name="test_table",
            columns=["column1", "column2"]
        )
        
        # Start the MQTT client loop
        writer.start(
            endpoint="localhost",
            port=1883,
            keep_alive=60
        )
        
if __name__ == "__main__":
    __main__()