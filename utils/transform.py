import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df_transform = df.copy()

        price_cleaned = df_transform['Price'].replace({r'\$': '', ',': ''}, regex=True)
        price_numeric = pd.to_numeric(price_cleaned, errors='coerce')
        df_transform['Price'] = price_numeric * 16000
        
        df_transform['Rating'] = df_transform['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        
        df_transform['Colors'] = df_transform['Colors'].str.extract(r'(\d+)').astype(int)
        
        df_transform['Size'] = df_transform['Size'].str.replace('Size: ', '', regex=False)
        
        df_transform['Gender'] = df_transform['Gender'].str.replace('Gender: ', '', regex=False)

        df_transform = df_transform[df_transform['Title'] != 'Unknown Product']
        df_transform.dropna(inplace=True)
        df_transform.drop_duplicates(inplace=True)

        df_transform = df_transform.astype({
            'Title': 'object',
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64',
            'Size': 'object',
            'Gender': 'object',
            'Timestamp': 'string'
        })

        print("Data transformation")
        return df_transform.reset_index(drop=True)

    except Exception as e:
        print(f"Error transformation: {e}")
        return pd.DataFrame()