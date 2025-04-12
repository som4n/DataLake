import boto3
from typing import Dict, List

class GlueCrawlerConfig:
    def __init__(self, crawler_name: str, role_arn: str):
        self.glue_client = boto3.client('glue')
        self.crawler_name = crawler_name
        self.role_arn = role_arn

    def create_crawler(self, 
                      database_name: str,
                      s3_targets: List[str],
                      schedule: str = None,
                      table_prefix: str = None) -> Dict:
        """
        Create a new Glue Crawler with specified configuration
        """
        crawler_config = {
            'Name': self.crawler_name,
            'Role': self.role_arn,
            'DatabaseName': database_name,
            'Targets': {
                'S3Targets': [{'Path': target} for target in s3_targets]
            },
            'SchemaChangePolicy': {
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'LOG'
            },
            'Configuration': {
                'Version': 1.0,
                'CrawlerOutput': {
                    'Partitions': {'AddOrUpdateBehavior': 'InheritFromTable'},
                    'Tables': {'AddOrUpdateBehavior': 'MergeNewColumns'}
                }
            }
        }

        if schedule:
            crawler_config['Schedule'] = schedule
        
        if table_prefix:
            crawler_config['TablePrefix'] = table_prefix

        try:
            response = self.glue_client.create_crawler(**crawler_config)
            return {'status': 'success', 'response': response}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def start_crawler(self) -> Dict:
        """
        Start the Glue Crawler
        """
        try:
            response = self.glue_client.start_crawler(Name=self.crawler_name)
            return {'status': 'success', 'response': response}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_crawler_status(self) -> Dict:
        """
        Get the current status of the crawler
        """
        try:
            response = self.glue_client.get_crawler(Name=self.crawler_name)
            return {'status': 'success', 'crawler_status': response['Crawler']['State']}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_crawler_schedule(self, schedule: str) -> Dict:
        """
        Update the crawler's schedule
        """
        try:
            response = self.glue_client.update_crawler(
                Name=self.crawler_name,
                Schedule=schedule
            )
            return {'status': 'success', 'response': response}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

def get_sample_usage():
    """
    Example usage of the GlueCrawlerConfig class
    """
    crawler_config = GlueCrawlerConfig(
        crawler_name='sample-data-crawler',
        role_arn='arn:aws:iam::123456789012:role/GlueCrawlerRole'
    )

    # Create a new crawler
    create_response = crawler_config.create_crawler(
        database_name='sample_database',
        s3_targets=['s3://my-bucket/raw-data/'],
        schedule='cron(0 12 * * ? *)',  # Run daily at 12:00 PM UTC
        table_prefix='raw_'
    )

    # Start the crawler
    start_response = crawler_config.start_crawler()

    # Check crawler status
    status_response = crawler_config.get_crawler_status()

    return create_response, start_response, status_response

if __name__ == '__main__':
    get_sample_usage()