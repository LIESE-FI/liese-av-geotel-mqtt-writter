import sqlalchemy as db
import polars as pl

class DatabaseConnection:
    # Initialize the database connection
    def __init__(self, db_url: str):
        """
        Initialize the DatabaseConnection with a database URL.
        
        Parameters:
        db_url (str): The database URL to connect to.
        """
        self.engine = db.create_engine(db_url)
        self.conn = self.engine.connect()
        
    # Close the database connection
    def close(self):
        """
        Close the database connection.
        
        This method should be called when the connection is no longer needed.
        """
        if self.conn:
            self.conn.close()
            self.engine.dispose()
            
    # Execute a query and return the result
    def execute_query(self, query: str):
        """
        Execute a SQL query and return the result.
        
        Parameters:
        query (str): The SQL query to execute.
        
        Returns:
        list: The result of the query as a list of tuples.
        """
        result = self.conn.execute(query)
        return result.fetchall()
    
    # Fetch one record from a table
    def fetch_one(self, table_name: str, columns: list = None):
        """
        Fetch one record from a specified table.
        
        Parameters:
        table_name (str): The name of the table to fetch a record from.
        
        Returns:
        pl.DataFrame: A Polars DataFrame containing the first record from the table.
        """
        if columns is None:
            query = f"SELECT * FROM {table_name} LIMIT 1"
        else:
            cols = ', '.join(columns)
            query = f"SELECT {cols} FROM {table_name} LIMIT 1"
        
        df = pl.read_database(
            query = query,
            connection = self.conn
        )
        return df
    
    # Fetch all records from a table
    def fetch_all(self, table_name: str, columns: list = None):
        """
        Fetch all records from a specified table.
        
        Parameters:
        table_name (str): The name of the table to fetch records from.
        
        Returns:
        pl.DataFrame: A Polars DataFrame containing the records from the table.
        """
        if columns is None:
            query = f"SELECT * FROM {table_name}"
        else:
            cols = ', '.join(columns)
            query = f"SELECT {cols} FROM {table_name}"
        
        df = pl.read_database(
            query = query,
            connection = self.conn
        )
        return df