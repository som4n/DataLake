import boto3
import pandas as pd
from typing import Dict, List, Optional, Callable
import logging
from datetime import datetime
import awswrangler as wr

class DataTransformation:
    def __init__(self, source_bucket: str, target_bucket: str, region: str = 'us-east-1'):
        self.s3_client = boto3.client('s3', region_name=region)
        self.source_bucket = source_bucket
        self.target_bucket = target_bucket
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('DataTransformation')

    def transform_data(self,
                      source_path: str,
                      target_path: str,
                      transformation_func: Callable[[pd.DataFrame], pd.DataFrame],
                      partition_cols: Optional[List[str]] = None) -> Dict:
        """
        Apply transformation to data and save results
        """
        try:
            # Read data using AWS Wrangler
            df = wr.s3.read_parquet(f's3://{self.source_bucket}/{source_path}')
            
            # Apply transformation
            transformed_df = transformation_func(df)
            
            # Save transformed data
            if partition_cols:
                wr.s3.to_parquet(
                    df=transformed_df,
                    path=f's3://{self.target_bucket}/{target_path}',
                    dataset=True,
                    partition_cols=partition_cols
                )
            else:
                wr.s3.to_parquet(
                    df=transformed_df,
                    path=f's3://{self.target_bucket}/{target_path}',
                    dataset=True
                )

            return {
                'status': 'success',
                'message': f'Data transformed successfully to {target_path}',
                'rows_processed': len(transformed_df)
            }

        except Exception as e:
            self.logger.error(f"Error transforming data: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def apply_quality_checks(self, df: pd.DataFrame, rules: Dict) -> Dict:
        """
        Apply data quality checks
        """
        results = {}
        try:
            for rule_name, rule_func in rules.items():
                results[rule_name] = rule_func(df)
            
            return {
                'status': 'success',
                'quality_results': results
            }
        except Exception as e:
            self.logger.error(f"Error in quality checks: {str(e)}")
            return {'status': 'error', 'message': str(e)}

def get_sample_usage():
    """
    Example usage of the DataTransformation class
    """
    def sample_transformation(df: pd.DataFrame) -> pd.DataFrame:
        # Add derived columns
        df['total_amount'] = df['quantity'] * df['unit_price']
        df['processing_date'] = datetime.now().date()
        return df

    def sample_quality_rules(df: pd.DataFrame) -> bool:
        return len(df) > 0 and not df['total_amount'].isnull().any()

    transformer = DataTransformation(
        source_bucket='source-bucket',
        target_bucket='target-bucket'
    )

    # Transform data
    transform_response = transformer.transform_data(
        source_path='raw/sales',
        target_path='processed/sales',
        transformation_func=sample_transformation,
        partition_cols=['year', 'month']
    )

    # Apply quality checks
    quality_response = transformer.apply_quality_checks(
        pd.DataFrame(),  # Replace with actual DataFrame
        {'row_check': sample_quality_rules}
    )

    return transform_response, quality_response

if __name__ == '__main__':
    get_sample_usage()