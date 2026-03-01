import pandas as pd
import json
import math
import os

def parse_csv_to_list(filename):
    if not os.path.exists(filename):
        return []
    try:
        df = pd.read_csv(filename)
        # Replace NaN with None or 0
        df = df.where(pd.notnull(df), None)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
        return []

# Extract Historical Data (GWAP/LWAP)
def extract_historical():
    years = {1: '2021', 3: '2022', 5: '2023', 7: '2024', 9: '2025'}
    area_headers = ['NATIONAL (LUZON, VISAYAS and MINDANAO)', 'SYSTEM (LUZON, VISAYAS and MINDANAO)', 'LUZON', 'VISAYAS', 'MINDANAO']
    
    xls = pd.ExcelFile('GWAP&LWAP_2022-2025.xlsx')
    gwap_df = pd.read_excel(xls, 'GWAP')
    lwap_df = pd.read_excel(xls, 'LWAP')

    def extract_sheet(df):
        areas_res = {}
        for i, row in df.iterrows():
            val = str(row.iloc[0]).strip()
            if any(h in val for h in area_headers):
                area_name = 'SYSTEM' if 'SYSTEM' in val or 'NATIONAL' in val else val
                area_data = {}
                for col_idx, year_val in years.items():
                    months_data = []
                    for m_row in range(i + 2, i + 14):
                        if m_row >= len(df): break
                        month_name = str(df.iloc[m_row, 0]).strip()
                        price = df.iloc[m_row, col_idx]
                        try:
                            price = float(price)
                            if math.isnan(price): price = 0.0
                        except: price = 0.0
                        months_data.append({"month": month_name, "price": price})
                    area_data[year_val] = months_data
                areas_res[area_name] = area_data
        return areas_res

    return {"GWAP": extract_sheet(gwap_df), "LWAP": extract_sheet(lwap_df)}

# Load and Combine all data
data = {
    "historical": extract_historical(),
    "stl_prices": parse_csv_to_list('STLPRICE_202601260000.csv'),
    "mp_prices": parse_csv_to_list('MP_20260227.csv'),
    "capeg": parse_csv_to_list('CAPEG_20260216 (1).csv'),
    "caper": parse_csv_to_list('CAPER_20260216.csv'),
    "mru_mo": parse_csv_to_list('mru_mo_processed_20260209-20260215.csv')
}

with open('extensive_data.js', 'w') as f:
    f.write('const EXTENSIVE_DATA = ' + json.dumps(data) + ';')

print("Extensive data generated.")
