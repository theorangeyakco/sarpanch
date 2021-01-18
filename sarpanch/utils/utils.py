import boto3
from botocore.client import Config

from ..settings import AWS_PRIVATE_MEDIA_LOCATION


def get_presigned_url(relative_path_from_private_media_root: str) -> str:
	"""Returns a presigned url from the private media root to access
	   private media programmatically.
	"""

	s3 = boto3.client('s3', config=Config(signature_version='s3v4',
	                                      region_name='ap-south-1'))
	url = s3.generate_presigned_url(
			ClientMethod='get_object',
			Params={
				'Bucket': 'typc-assets',
				'Key'   : f'{AWS_PRIVATE_MEDIA_LOCATION}/{relative_path_from_private_media_root}',
			}
	)
	return url
