# CSV to Database Loader

## Project Description
A Python-based utility to load CSV files into a MySQL or PostgreSQL database. Includes error handling and logging for robust operations.

## Tech Stack
- Python (3.9+)
- MySQL or PostgreSQL
- Key Libraries: pandas, pymysql/psycopg2, click (optional)

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
