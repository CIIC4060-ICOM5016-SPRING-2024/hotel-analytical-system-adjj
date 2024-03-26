import os
import pandas as pd

def clean_room_unavailable(file_path, output_dir):

    df = pd.read_csv(file_path)
    df_cleaned = df.dropna()
    df_cleaned["ruid"] = df_cleaned["ruid"].astype(int)
    df_cleaned["rid"] = df_cleaned["rid"].astype(int)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate the output file path
    clean_file_name = os.path.splitext(os.path.basename(file_path))[0]
    new_file_path = os.path.join(output_dir, f"{clean_file_name}.csv")

    # Check if the file already exists
    if os.path.exists(new_file_path):
        user_choice = input(f'The file {new_file_path} already exists. Do you want to overwrite it? (yes/no): ').lower()
        if user_choice != 'yes':
            print('File not overwritten. Exiting.')
            exit()

    # Save the cleaned data to the specified output file
    df_cleaned.to_csv(new_file_path, index=False)
    print(f"Cleaned data saved to {new_file_path}")

    return df_cleaned

# Example usage:
# input_file_path = "Phase#1_data/room_unavailable.csv"  # Replace with the actual input file path
# output_directory = "./Phase#1_data/modified_data"  # Replace with your desired output directory

# cleaned_data = clean_room_unavailable(input_file_path, output_directory)


clean_room_unavailable('Phase#1_data/room_unavailable.csv', './Phase#1_data/modified_data/int_clean_room_unavailable') 

