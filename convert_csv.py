import pandas as pd
import json

# Try different encodings
encodings = ['cp1252', 'latin1', 'iso-8859-1']

for encoding in encodings:
    try:
        print(f"Trying encoding: {encoding}")
        df = pd.read_csv('NewBedfordMACodeofOrdinancesEXPORT20240530.csv', encoding=encoding)
        
        # Convert to list of dictionaries
        codes = df.to_dict('records')
        
        # Save to JSON file
        with open('city_codes.json', 'w', encoding='utf-8') as f:
            json.dump(codes, f, ensure_ascii=False, indent=2)
        
        print(f"Success! Used encoding: {encoding}")
        print("city_codes.json has been created.")
        break
        
    except UnicodeDecodeError:
        print(f"Failed with encoding: {encoding}")
        continue
    except Exception as e:
        print(f"Other error: {str(e)}")
        continue