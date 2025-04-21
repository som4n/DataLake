import click
from db_loader import load_csv_to_db

@click.command()
@click.option('--csv', required=True, type=click.Path(exists=True), help="Path to the CSV file")
@click.option('--host', required=True, help="Database host")
@click.option('--user', required=True, help="Database user")
@click.option('--password', required=True, help="Database password")
@click.option('--database', required=True, help="Database name")
def upload_csv(csv, host, user, password, database):
    """CLI to upload CSV to database."""
    db_config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }
    load_csv_to_db(csv, db_config)

if __name__ == '__main__':
    upload_csv()