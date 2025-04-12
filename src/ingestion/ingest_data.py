import boto3
import pandas as pd
from typing import Dict, List, Optional
import logging
from datetime import datetime

class DataLakeIngestion:
    def __init__(self, bucket_name: str, region: str = 'us-east-1'):
        self.s3_client = boto3.client('s3', region_name=region)
        self.bucket_name = bucket_name
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('DataLakeIngestion')

    def ingest_csv(self, 
                   file_path: str, 
                   target_path: str,
                   partition_cols: Optional[List[str]] = None) -> Dict:
        """
        Ingest CSV file to Data Lake with optional partitioning
        """
        try:
            df = pd.read_csv(file_path)
            return self._process_and_upload_data(df, target_path, partition_cols)
        except Exception as e:
            self.logger.error(f"Error ingesting CSV file: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def ingest_json(self, 
                    file_path: str, 
                    target_path: str,
                    partition_cols: Optional[List[str]] = None) -> Dict:
        """
        Ingest JSON file to Data Lake with optional partitioning
        """
        try:
            df = pd.read_json(file_path)
            return self._process_and_upload_data(df, target_path, partition_cols)
        except Exception as e:
            self.logger.error(f"Error ingesting JSON file: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def ingest_database(self,
                       connection_string: str,
                       query: str,
                       target_path: str,
                       partition_cols: Optional[List[str]] = None) -> Dict:
        """
        Ingest data from database using SQL query
        """
        try:
            df = pd.read_sql(query, connection_string)
            return self._process_and_upload_data(df, target_path, partition_cols)
        except Exception as e:
            self.logger.error(f"Error ingesting database data: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _process_and_upload_data(self,
                                df: pd.DataFrame,
                                target_path: str,
                                partition_cols: Optional[List[str]] = None) -> Dict:
        """
        Process and upload data to S3 with partitioning
        """
        try:
            if partition_cols:
                for partition_values, partition_df in df.groupby(partition_cols):
                    partition_path = self._build_partition_path(
                        target_path, 
                        partition_cols, 
                        partition_values
                    )
                    self._upload_parquet(partition_df, partition_path)
            else:
                self._upload_parquet(df, target_path)

            return {
                'status': 'success',
                'message': f'Data ingested successfully to {target_path}',
                'rows_processed': len(df)
            }

        except Exception as e:
            self.logger.error(f"Error processing and uploading data: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _upload_parquet(self, df: pd.DataFrame, target_path: str):
        """
        Upload DataFrame as Parquet file to S3
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'data_{timestamp}.parquet'
        s3_key = f'{target_path}/{file_name}'

        parquet_buffer = df.to_parquet()
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=parquet_buffer
        )

    def _build_partition_path(self,
                            base_path: str,
                            partition_cols: List[str],
                            partition_values) -> str:
        """
        Build S3 path with partitions
        """
        partition_path = base_path
        for col, val in zip(partition_cols, partition_values):
            partition_path += f'/{col}={val}'
        return partition_path

def get_sample_usage():
    """
    Example usage of the DataLakeIngestion class
    """
    ingestion = DataLakeIngestion(
        bucket_name='my-data-lake-bucket'
    )

    # Ingest CSV with partitioning
    csv_response = ingestion.ingest_csv(
        file_path='sample_data.csv',
        target_path='raw/sales',
        partition_cols=['year', 'month']
    )

    # Ingest JSON
    json_response = ingestion.ingest_json(
        file_path='sample_data.json',
        target_path='raw/customers'
    )

    # Ingest from database
    db_response = ingestion.ingest_database(
        connection_string='postgresql://user:pass@localhost:5432/db',
        query='SELECT * FROM orders',
        target_path='raw/orders',
        partition_cols=['order_date']
    )

    return csv_response, json_response, db_response

if __name__ == '__main__':
    get_sample_usage()