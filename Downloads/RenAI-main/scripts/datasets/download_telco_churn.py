"""
Download TU Wien Telco Customer Churn dataset (real research data)
"""
import requests
from pathlib import Path

def main():
    base_dir = Path("data/raw/churn")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    url = "https://researchdata.tuwien.ac.at/records/etkr1-6zb46/files/telco_customer_churn_data.csv"
    r = requests.get(url)
    with open(base_dir / "telco_churn.csv", 'wb') as f:
        f.write(r.content)
    
    print("TU Wien Churn dataset downloaded.")

if __name__ == "__main__":
    main()