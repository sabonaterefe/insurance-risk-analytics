import pandas as pd
from pathlib import Path
import chardet
import sys
import warnings
from typing import Optional, Tuple

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def validate_file(file_path: Path) -> bool:
    """Check if file exists and is non-empty."""
    if not file_path.exists() or file_path.stat().st_size == 0:
        print(f"Error: File not found or empty at {file_path}")
        return False
    return True

def detect_file_properties(file_path: Path) -> Tuple[str, str]:
    """Detect file encoding and delimiter with fallbacks."""
    try:
        with open(file_path, 'rb') as f:
            encoding = chardet.detect(f.read(10000))['encoding'] or 'utf-8'
        
        # Read sample lines for delimiter detection
        sample_lines = Path(file_path).read_text(encoding, errors='replace').splitlines()[:5]
        delimiters = {d: sample_lines[1].count(d) for d in [',', '\t', ';', '|', ' ', ':']}
        
        return encoding, max(delimiters, key=delimiters.get, default='|')  # Using '|' as per your data
    except Exception as e:
        print(f"Warning: Could not detect file properties ({e}), using defaults")
        return 'utf-8', '|'

def try_loading_methods(file_path: Path, encoding: str, delimiter: str) -> Optional[pd.DataFrame]:
    """Try multiple pandas loading methods with fallbacks."""
    methods = [
        lambda: pd.read_csv(file_path, sep=delimiter, encoding=encoding, engine='python'),
        lambda: pd.read_table(file_path, sep=delimiter, encoding=encoding),
    ]
    
    for load_method in methods:
        try:
            df = load_method()
            if df.shape[1] > 1:  # Valid dataframe with multiple columns
                return df
        except Exception as e:
            print(f"❌ Error loading with method {load_method}: {e}")
            continue
    return None

def load_raw_data() -> Optional[pd.DataFrame]:
    """Load raw data with multiple fallback methods."""
    raw_path = Path("data/raw/MachineLearningRating_v3/MachineLearningRating_v3.txt")
    
    if not validate_file(raw_path):
        return None
    
    encoding, delimiter = detect_file_properties(raw_path)
    print(f"Attempting to load with encoding: {encoding}, delimiter: '{delimiter}'")
    
    df = try_loading_methods(raw_path, encoding, delimiter)
    
    if df is not None:
        print(f"✅ Successfully loaded data with shape: {df.shape}")
        return df
    
    print("All loading methods exhausted")
    return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize columns, convert dates and numeric values."""
    if df.empty:
        raise ValueError("No data provided for cleaning")
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Convert date columns to datetime
    for col in ['transactionmonth', 'vehicleintroductiondate']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Convert relevant columns to numeric
    numeric_cols = ['capital_outstanding', 'totalpremium', 'totalclaims', 'customvalueestimate']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def save_processed_data(df: pd.DataFrame) -> None:
    """Save processed data as Parquet, fallback to CSV if needed."""
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    processed_path = processed_dir / "insurance_data.parquet"
    
    try:
        df.to_parquet(processed_path)
        print(f"✅ Data saved successfully to {processed_path}")
    except Exception as e:
        print(f"❌ Error saving Parquet: {e}, trying CSV fallback...")
        df.to_csv(processed_dir / "insurance_data.csv", index=False)

def main() -> None:
    """Run full pipeline: Load → Clean → Save."""
    print("\n=== Starting Data Processing Pipeline ===")
    
    raw_df = load_raw_data()
    if raw_df is None:
        sys.exit("\n❌ Pipeline failed: Could not load raw data")

    print("\n[2/3] Cleaning data...")
    clean_df = clean_data(raw_df)

    print("\n[3/3] Saving processed data...")
    save_processed_data(clean_df)
    
    print("\n✅ Pipeline Completed Successfully!")

if __name__ == "__main__":
    main()