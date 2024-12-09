import pandas as pd

def inspect_and_convert_csv():
    # Read CSV with the encoding we know works
    print("Reading CSV file...")
    df = pd.read_csv('NewBedfordMACodeofOrdinancesEXPORT20240530.csv', encoding='cp1252')
    
    # Print column names
    print("\nColumns in the CSV:")
    print(df.columns.tolist())
    
    # Print first few rows
    print("\nFirst few rows of data:")
    print(df.head())
    
    # Create text file
    print("\nConverting to text file...")
    with open('city_codes.txt', 'w', encoding='utf-8') as f:
        f.write("NEW BEDFORD CITY CODES\n\n")
        
        # Write each row without grouping
        for _, row in df.iterrows():
            for column in df.columns:
                f.write(f"{column}: {row[column]}\n")
            f.write("\n" + "-"*50 + "\n")  # Section separator

if __name__ == "__main__":
    inspect_and_convert_csv()
    print("\nCreated city_codes.txt!")