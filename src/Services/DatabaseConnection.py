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
    def execute_query(self, query: str, params=None):
        """
        Execute a SQL query and return the result.
        
        Parameters:
        query (str): The SQL query to execute.
        params (dict): Parameters for the query (optional).
        
        Returns:
        Result: The result of the query execution.
        """
        try:
            if params:
                result = self.conn.execute(db.text(query), params)
            else:
                result = self.conn.execute(db.text(query))
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Database error: {e}")
            self.conn.rollback()
            raise e
    
    # Insert data into a specified table
    def insert_data(self, table_name: str, data: dict):
        """
        Insert data into a specified table.
        
        Parameters:
        table_name (str): The name of the table to insert data into.
        data (dict): A dictionary containing column names as keys and values to insert.
        
        Returns:
        bool: True if the insertion was successful, False otherwise.
        """
        try:
            columns = ', '.join([f'"{col}"' for col in data.keys()])
            placeholders = ', '.join([f':{col}' for col in data.keys()])
            query = f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders})'
            
            self.conn.execute(db.text(query), data)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.conn.rollback()
            return False
    
    # Update data in a specified table
    def update_data(self, table_name: str, data: dict, where_clause: str, where_params: dict = None):
        """
        Update data in a specified table.
        
        Parameters:
        table_name (str): The name of the table to update.
        data (dict): A dictionary containing column names as keys and new values.
        where_clause (str): The WHERE clause for the update.
        where_params (dict): Parameters for the WHERE clause.
        
        Returns:
        bool: True if the update was successful, False otherwise.
        """
        try:
            set_clause = ', '.join([f'"{col}" = :{col}' for col in data.keys()])
            query = f'UPDATE "{table_name}" SET {set_clause} WHERE {where_clause}'
            
            params = data.copy()
            if where_params:
                params.update(where_params)
            
            self.conn.execute(db.text(query), params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating data: {e}")
            self.conn.rollback()
            return False
    
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