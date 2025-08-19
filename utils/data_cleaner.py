import pandas as pd
import numpy as np
import re
from typing import Dict, Any, Tuple

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.original_df = df.copy()
        self.current_df = df.copy()
        self.cleaning_history = []
    
    def get_dataset_summary(self) -> Dict[str, Any]:
        """Get comprehensive dataset summary"""
        # Convert pandas data types to strings for JSON serialization
        data_types_dict = {}
        for col, dtype in self.current_df.dtypes.items():
            data_types_dict[str(col)] = str(dtype)
        
        # Convert missing values to regular Python types
        missing_values_dict = {}
        for col, count in self.current_df.isnull().sum().items():
            missing_values_dict[str(col)] = int(count)
        
        summary = {
            'rows': int(len(self.current_df)),
            'columns': int(len(self.current_df.columns)),
            'column_names': [str(col) for col in self.current_df.columns],
            'data_types': data_types_dict,
            'missing_values': missing_values_dict,
            'total_missing': int(self.current_df.isnull().sum().sum()),
            'duplicates': int(self.current_df.duplicated().sum()),
            'memory_usage': float(self.current_df.memory_usage(deep=True).sum() / 1024)  # KB
        }
        return summary
    
    def remove_duplicates(self) -> Dict[str, Any]:
        """Remove duplicate rows"""
        before_count = len(self.current_df)
        self.current_df.drop_duplicates(inplace=True)
        after_count = len(self.current_df)
        removed_count = before_count - after_count
        
        result = {
            'operation': 'Remove Duplicates',
            'description': f'Removed {removed_count} duplicate rows',
            'before_summary': self.get_dataset_summary(),
            'after_summary': self.get_dataset_summary()
        }
        
        self.cleaning_history.append(result)
        return result
    
    def fill_missing_values(self, method: str = 'mean') -> Dict[str, Any]:
        """Fill missing values using specified method"""
        before_summary = self.get_dataset_summary()
        
        numeric_columns = self.current_df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if self.current_df[col].isnull().sum() > 0:
                if method == 'mean':
                    fill_value = self.current_df[col].mean()
                elif method == 'median':
                    fill_value = self.current_df[col].median()
                elif method == 'mode':
                    fill_value = self.current_df[col].mode().iloc[0] if not self.current_df[col].mode().empty else 0
                else:
                    fill_value = 0
                
                self.current_df[col].fillna(fill_value, inplace=True)
        
        # For categorical columns, fill with mode
        categorical_columns = self.current_df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if self.current_df[col].isnull().sum() > 0:
                mode_value = self.current_df[col].mode().iloc[0] if not self.current_df[col].mode().empty else 'Unknown'
                self.current_df[col].fillna(mode_value, inplace=True)
        
        result = {
            'operation': f'Fill Missing Values ({method})',
            'description': f'Filled missing values using {method} method for numeric columns and mode for categorical columns',
            'before_summary': before_summary,
            'after_summary': self.get_dataset_summary()
        }
        
        self.cleaning_history.append(result)
        return result
    
    def drop_high_missing_columns(self, threshold: float = 0.5) -> Dict[str, Any]:
        """Drop columns with high percentage of missing data"""
        before_summary = self.get_dataset_summary()
        
        missing_percentage = self.current_df.isnull().sum() / len(self.current_df)
        columns_to_drop = missing_percentage[missing_percentage > threshold].index.tolist()
        
        if columns_to_drop:
            self.current_df.drop(columns=columns_to_drop, inplace=True)
            result = {
                'operation': f'Drop High Missing Columns (>{threshold*100}%)',
                'description': f'Dropped {len(columns_to_drop)} columns: {", ".join(columns_to_drop)}',
                'before_summary': before_summary,
                'after_summary': self.get_dataset_summary()
            }
        else:
            result = {
                'operation': f'Drop High Missing Columns (>{threshold*100}%)',
                'description': 'No columns met the threshold for removal',
                'before_summary': before_summary,
                'after_summary': self.get_dataset_summary()
            }
        
        self.cleaning_history.append(result)
        return result
    
    def remove_special_characters(self) -> Dict[str, Any]:
        """Remove special characters from string columns"""
        before_summary = self.get_dataset_summary()
        
        string_columns = self.current_df.select_dtypes(include=['object']).columns
        
        for col in string_columns:
            if self.current_df[col].dtype == 'object':
                # Remove special characters but keep alphanumeric, spaces, and common punctuation
                self.current_df[col] = self.current_df[col].astype(str).apply(
                    lambda x: re.sub(r'[^\w\s.,!?-]', '', x) if pd.notna(x) else x
                )
        
        result = {
            'operation': 'Remove Special Characters',
            'description': 'Removed special characters from string columns while preserving alphanumeric characters, spaces, and common punctuation',
            'before_summary': before_summary,
            'after_summary': self.get_dataset_summary()
        }
        
        self.cleaning_history.append(result)
        return result
    
    def convert_data_types(self) -> Dict[str, Any]:
        """Automatically convert data types for better performance"""
        before_summary = self.get_dataset_summary()
        
        # Convert numeric columns to appropriate types
        for col in self.current_df.columns:
            if self.current_df[col].dtype == 'object':
                # Try to convert to numeric
                try:
                    pd.to_numeric(self.current_df[col], errors='coerce')
                    # If successful, convert
                    self.current_df[col] = pd.to_numeric(self.current_df[col], errors='coerce')
                except:
                    pass
        
        # Optimize numeric types
        for col in self.current_df.select_dtypes(include=[np.number]).columns:
            if self.current_df[col].dtype == 'float64':
                # Check if we can convert to int
                if self.current_df[col].isnull().sum() == 0 and (self.current_df[col] % 1 == 0).all():
                    self.current_df[col] = self.current_df[col].astype('int64')
        
        result = {
            'operation': 'Convert Data Types',
            'description': 'Automatically converted data types for better performance and memory usage',
            'before_summary': before_summary,
            'after_summary': self.get_dataset_summary()
        }
        
        self.cleaning_history.append(result)
        return result
    
    def get_cleaned_dataframe(self) -> pd.DataFrame:
        """Return the cleaned dataframe"""
        return self.current_df.copy()
    
    def get_cleaning_history(self) -> list:
        """Return the history of all cleaning operations"""
        return self.cleaning_history
    
    def reset_to_original(self):
        """Reset to the original dataset"""
        self.current_df = self.original_df.copy()
        self.cleaning_history = []

def clean_data(df: pd.DataFrame, options: Dict[str, Any]) -> pd.DataFrame:
    """Legacy function for backward compatibility"""
    cleaner = DataCleaner(df)
    
    if options.get('remove_duplicates'):
        cleaner.remove_duplicates()
    
    if options.get('fill_missing'):
        cleaner.fill_missing_values('mean')
    
    if options.get('detect_outliers'):
        # Handle outliers by clipping them
        for col in df.select_dtypes(include='number').columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[col] = df[col].clip(lower_bound, upper_bound)
    
    return cleaner.get_cleaned_dataframe()
