import json
import os
import re

class MiniDB:
    def __init__(self, db_name="mydb"):
        self.db_name = db_name
        self.tables = {}
        # Create DB folder if it doesn't exist
        if not os.path.exists(self.db_name):
            os.makedirs(self.db_name)
        self._load_metadata()

    def _load_metadata(self):
        # Load all existing .json files as tables
        for filename in os.listdir(self.db_name):
            if filename.endswith(".json"):
                table_name = filename.split(".")[0]
                self.tables[table_name] = self._read_table(table_name)

    def _save_table(self, table_name, data):
        filepath = os.path.join(self.db_name, f"{table_name}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def _read_table(self, table_name):
        filepath = os.path.join(self.db_name, f"{table_name}.json")
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def execute(self, query):
        query = query.strip()
        
        # --- 1. CREATE TABLE ---
        # Usage: CREATE TABLE users (id, name, age)
        if query.upper().startswith("CREATE TABLE"):
            match = re.match(r"CREATE TABLE (\w+)\s*\((.+)\)", query, re.IGNORECASE)
            if match:
                table_name, columns = match.groups()
                if table_name in self.tables:
                    return f"Error: Table '{table_name}' already exists."
                
                # We initialize with an empty list
                self.tables[table_name] = [] 
                self._save_table(table_name, [])
                return f"Table '{table_name}' created."

        # --- 2. INSERT ---
        # Usage: INSERT INTO users VALUES (1, "John", 25)
        elif query.upper().startswith("INSERT INTO"):
            match = re.match(r"INSERT INTO (\w+) VALUES \((.+)\)", query, re.IGNORECASE)
            if match:
                table_name, values_str = match.groups()
                if table_name not in self.tables:
                    return f"Error: Table '{table_name}' not found."
                
                # Clean values: split by comma, remove quotes and spaces
                values = [v.strip().strip('"').strip("'") for v in values_str.split(",")]
                
                # Validation: Check Primary Key (Assuming 1st column is PK)
                current_data = self.tables[table_name]
                for row in current_data:
                    if row[0] == values[0]:
                        return f"Error: Duplicate ID {values[0]}."

                current_data.append(values)
                self._save_table(table_name, current_data)
                return "1 row inserted."

        # --- 3. SELECT (with simple JOIN support) ---
        # Usage: SELECT * FROM users
        # Usage: SELECT * FROM users JOIN orders ON users.id = orders.user_id
        elif query.upper().startswith("SELECT"):
            
            # CASE A: JOIN
            if " JOIN " in query.upper():
                # Rough parsing for demo purposes
                # Splits string into: [SELECT * FROM, table1, table2, condition]
                parts = re.split(r" FROM | JOIN | ON ", query, flags=re.IGNORECASE)
                
                if len(parts) < 4: return "Error: Invalid JOIN syntax."

                table1_name = parts[1].strip()
                table2_name = parts[2].strip()
                condition = parts[3].strip() # e.g., "users.id = orders.user_id"

                t1_data = self.tables.get(table1_name, [])
                t2_data = self.tables.get(table2_name, [])
                
                results = []
                
                # Parse condition (very basic: assumes col_index 0 vs col_index 1 logic for demo)
                # REAL WORLD: You would parse column names. 
                # DEMO HACK: We will assume we are joining Table1 Col 0 (ID) with Table2 Col 1 (Foreign Key)
                
                for row1 in t1_data:
                    for row2 in t2_data:
                        # Join Condition: If T1 ID matches T2's second column (user_id)
                        if row1[0] == row2[1]: 
                            results.append(row1 + row2)
                return results

            # CASE B: Simple SELECT
            else:
                match = re.match(r"SELECT \* FROM (\w+)", query, re.IGNORECASE)
                if match:
                    table_name = match.groups()[0]
                    return self.tables.get(table_name, "Error: Table not found.")

        return "Error: Syntax not recognized."