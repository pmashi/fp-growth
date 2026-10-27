import csv 
from pathlib import Path 

ROOT = Path(__file__).parent.parent
data_path = ROOT / "data" / "Sttel_industry_data.csv"

def read_data(file_path):

    with open(file_path, "r") as f: 
        reader = csv.reader(f) 
        rows = list(reader) 


if __name__ == "__main__": 
    