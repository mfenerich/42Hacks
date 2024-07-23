import sys
import csv

def escape_value(value):
    if value is None or value == '':
        return 'NULL'
    elif isinstance(value, str):
        # Escape single quotes
        value = value.replace("'", "''")
        return f"'{value}'"
    else:
        return str(value)

def generate_create_table_sql(table_name, header_row):
    column_defs = []
    for col in header_row:
        dtype = 'TEXT'
        if 'code' in col.lower() or 'number' in col.lower() or 'ident' in col.lower():
            dtype = 'VARCHAR(255)'
        elif 'id' in col.lower():
            dtype = 'INTEGER'
        elif 'latitude' in col.lower() or 'longitude' in col.lower() or 'elevation' in col.lower():
            dtype = 'REAL'
        elif 'date' in col.lower() or 'time' in col.lower():
            dtype = 'TIMESTAMP'
        column_defs.append(f"{col} {dtype}")
    
    column_defs_str = ",\n".join(column_defs)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n{column_defs_str}\n);"
    
    return create_table_sql

def generate_insert_sql(table_name, header_row, rows):
    column_names = ", ".join(header_row)
    values = []
    
    for row in rows:
        value_list = [escape_value(value) for value in row]
        values.append(f"({', '.join(value_list)})")
    
    values_str = ",\n".join(values)
    insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES\n{values_str};"
    
    return insert_sql

def process_csv(file_path, table_name):
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Get header row
        rows = list(reader)  # Get all rows
    
    create_sql = generate_create_table_sql(table_name, header)
    insert_sql = generate_insert_sql(table_name, header, rows)
    
    return create_sql, insert_sql

# Define file paths
user_airports_file = './assets/user_closest_airports.csv'
airports_file = './assets/airports_w_wiki.csv'

# Process both CSV files
user_airports_create_sql, user_airports_insert_sql = process_csv(user_airports_file, 'user_closest_airports')
airports_create_sql, airports_insert_sql = process_csv(airports_file, 'airports')

# Output SQL statements to a file
with open('./db/init.sql', 'w', encoding='utf-8') as f:
    f.write(f"-- Create tables\n{user_airports_create_sql}\n\n")
    f.write(f"-- Insert data into user_closest_airports\n{user_airports_insert_sql}\n\n")
    f.write(f"-- Create tables\n{airports_create_sql}\n\n")
    f.write(f"-- Insert data into airports_w_wiki\n{airports_insert_sql}\n")

print("SQL statements have been written to 'create_and_insert.sql'.")

sys.exit(0)
