 Data Lake Project

## Project Description
A comprehensive AWS-based Data Lake solution that handles data ingestion, transformation, and cataloging. Features robust error handling, data quality checks, and efficient S3 storage management.

## Tech Stack
- Python 3.8+
- AWS Services:
  - S3 (Storage)
  - Glue (Data Catalog)
  - Athena (Query Engine)
- Key Libraries: 
  - boto3
  - pandas
  - awswrangler


## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/csv-to-db-loader.git
   cd csv-to-db-loader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your database:
   Create a database and a table:
   ```sql
   CREATE TABLE users (
       id INT PRIMARY KEY,
       name VARCHAR(255),
       email VARCHAR(255)
   );
   ```   

4. Test with the sample CSV file in `data/sample.csv`.

## How to Run the Script
Run the main script directly:
```bash
python src/db_loader.py
```

Or use the CLI:
```bash
python src/cli.py --csv data/sample.csv --host localhost --user root --password root --database test_db
```

## Example Usage
Sample CSV file:
```
id,name,email
1,John Doe,john.doe@example.com
2,Jane Smith,jane.smith@example.com
```

## Suggestions for Next Features
- Add a scheduler to load CSV files periodically.
- Implement data validation.
- Create a web-based dashboard to view upload history.

## Requirements
See `requirements.txt` for library dependencies.
