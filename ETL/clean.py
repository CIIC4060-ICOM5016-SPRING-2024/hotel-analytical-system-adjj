import pandas as pd
import sqlite3
import os

class ETL:
    @staticmethod
    def compare_csv(file1:any,file2:any):
        # Read CSV files into pandas DataFrames
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        # Compare DataFrames
        if df1.equals(df2):
            print("The CSV files are identical.")
        else:
            # Find the differences
            differences = df1.compare(df2)
            print("Differences between the CSV files:")
            print(differences)

    @staticmethod
    def clean(file_path:str, clean_file_name:str = "") -> any:      
        if file_path.endswith('.csv'):
            file = pd.read_csv(file_path, index_col=None)               
        elif file_path.endswith('.xlsx'):
            file = pd.read_excel(file_path, index_col=None)
        elif file_path.endswith('.json'):
            file = pd.read_json(file_path)
        elif file_path.endswith('.db'):
            conn = sqlite3.connect(file_path)

            db_name, _ = os.path.splitext(os.path.basename(file_path))
            
            print("\n")
            print("Database Name: ", db_name)
            print("\n")


            # TODO: dynamic table finding
            if db_name == "rooms":
                sql_query = f"SELECT * FROM Room"

                file = pd.read_sql_query(sql_query,conn)

                print(file)
            elif db_name == "reserve":
                sql_query = f"SELECT * FROM reserve"

                file = pd.read_sql_query(sql_query,conn)

                print(file)
            
        
            
        print("\n")
        print("Input file:\n")
        print(file)
        print("\n")

        file = file.dropna(how='all') 
        header = file.columns.tolist()

        for h in header:
            condition = file[h].isnull() | (file[h] == '')
            file = file[~condition]
            if  h.endswith("id"):
                file[h] = file[h].astype(int)
            
        print("\n")
        print("Output file:\n")
        print(file)
        print("\n")



        if file_path.endswith('.csv'):
            new_file_path = f"./Phase#1_data/modified_data/{clean_file_name}.csv"
            if os.path.exists(new_file_path):
                user_choice = input(f'The file {new_file_path} already exists. Do you want to overwrite it? (yes/no): ').lower()
                if user_choice != 'yes':
                    print('File not overwritten. Exiting.')
                    exit()
            file.to_csv(new_file_path,index=False)

        elif file_path.endswith('.xlsx'):
            new_file_path = f"./Phase#1_data/modified_data/{clean_file_name}.xlsx"
            if os.path.exists(new_file_path):
                user_choice = input(f'The file {new_file_path} already exists. Do you want to overwrite it? (yes/no): ').lower()
                if user_choice != 'yes':
                    print('File not overwritten. Exiting.')
                    exit()

            file.to_excel(new_file_path,index=False)
        elif file_path.endswith('.json'):
            new_file_path = f"./Phase#1_data/modified_data/{clean_file_name}.json"
            if os.path.exists(new_file_path):
                user_choice = input(f'The file {new_file_path} already exists. Do you want to overwrite it? (yes/no): ').lower()
                # Check the user's choice
                if user_choice != 'yes':
                    print('File not overwritten. Exiting.')
                    exit()


            file.to_json(new_file_path, orient='records', lines=True)

            with open(f"./Phase#1_data/modified_data/{clean_file_name}.json", 'r') as file:
                json_data = '[' + file.read().rstrip(',\n').replace('\n', ',\n') + ']'

            with open(f"./Phase#1_data/modified_data/{clean_file_name}.json", 'w') as file:
                file.write(json_data)
        elif file_path.endswith('.db'):
            # TODO: .db file WRITING
            new_file_path = f"./Phase#1_data/modified_data/{clean_file_name}.db"
            if os.path.exists(new_file_path):
                user_choice = input(f'The file {new_file_path} already exists. Do you want to overwrite it? (yes/no): ').lower()
                if user_choice != 'yes':
                    print('File not overwritten. Exiting.')
                    exit()
            if db_name == "rooms":

                print(file)

                file.to_sql(name='Room', con=conn, index=False ,if_exists='replace')

                conn.close()
            elif db_name == "reserve":

                print(file)

                file.to_sql(name='reserve',con=conn , index=False , if_exists='replace')

                conn.close()



  

  
if __name__ == '__main__':
        
    # ETL.clean(file_path='./Phase#1_data/chain.xlsx', clean_file_name="clean_chain")
    ETL.clean(file_path='./Phase#1_data/room_unavailable.csv', clean_file_name="clean_rooms_unavailable")
    # ETL.compare_csv('./Phase#1_data/modified_data/ru_data.csv','./Phase#1_data/modified_data/int_clean_room_unavailable/room_unavailable.csv')

    # # ETL.clean(file_path='./Phase#1_data/employee.json', clean_file_name="clean_employee")
    # ETL.clean(file_path='./Phase#1_data/employee_updated.json', clean_file_name="clean_employee_updated")

    # ETL.clean(file_path='./Phase#1_data/hotel.csv', clean_file_name="clean_hotel")
    # ETL.clean(file_path='./Phase#1_data/login.xlsx', clean_file_name="clean_login")
    # # ETL.clean(file_path='./Phase#1_data/room_unavailable.csv', clean_file_name="clean_room_unavaiable") #!!!! returns float values
    # ETL.clean(file_path='./Phase#1_data/roomdetails.json', clean_file_name="clean_roomdetails")
    # ETL.clean(file_path='./Phase#1_data/rooms.db')
    # ETL.clean(file_path='./Phase#1_data/reserve.db')

    
   # print("No files to clean")
    
    



