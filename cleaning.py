import pandas as pd

def clean_data(df, options):
    if options.get('remove_duplicates'):
        df.drop_duplicates(inplace=True)

    if options.get('fill_missing'):
        df.fillna(df.mean(numeric_only=True), inplace=True)

    if options.get('detect_outliers'):
        for col in df.select_dtypes(include='number').columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[col] = df[col].clip(lower_bound, upper_bound)

    return df