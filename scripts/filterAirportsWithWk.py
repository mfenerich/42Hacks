import pandas as pd

def filter_airports_with_wikipedia(csv_file, output_file):
    """
    Reads a CSV file of airports, filters for rows with valid Wikipedia links, 
    and saves the results to a new CSV file.

    Args:
        csv_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
    """
    try:
        df = pd.read_csv(csv_file)

        filtered_df = df[df["wikipedia_link"].astype(str).str.contains(r"^https://.*wikipedia\.org/", regex=True)]

        # Save the filtered DataFrame to a new CSV file
        filtered_df.to_csv(output_file, index=False)

        print(f"Filtered results saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: File not found: {csv_file}")
    except KeyError:
        print(f"Error: 'wikipedia_link' column not found in {csv_file}")
    except Exception as e:  # Catch any other potential errors
        print(f"An unexpected error occurred: {e}")

# Example usage
csv_file_path = "/assets/airports.csv"
output_file_path = "/assets/airports_w_wiki.csv"
filter_airports_with_wikipedia(csv_file_path, output_file_path)
