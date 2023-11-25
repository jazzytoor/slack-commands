import boto3
import jmespath
from functools import lru_cache


@lru_cache(maxsize=None)
def get_all_regions():
    """
    Get a list of all available AWS regions.

    Returns:
    - list: A list of region names.

    Example:
    ```python
    all_regions = get_all_regions()
    print(all_regions)
    ```
    """

    ec2_client = boto3.client("ec2")
    regions = [
        region["RegionName"]
        for region in ec2_client.describe_regions()["Regions"]
    ]

    return regions


def get_tagged_resources(region, service):
    """
    Get resources filtered by region and service type.

    Parameters:
    - region (str): The AWS region where resources will be retrieved.
    - service (str): The type of AWS service for which to retrieve tagged resources.

    Returns:
    - list: A list of ARNs (Amazon Resource Names) for tagged resources.

    Example:
    ```python
    region = 'us-east-1'
    service = 'ec2'
    tagged_resources = get_tagged_resources(region, service)
    print(tagged_resources)
    ```
    """

    tagging_client = boto3.client(
        'resourcegroupstaggingapi',
        region_name=region
    )

    paginator = tagging_client.get_paginator('get_resources')
    page_iterator = paginator.paginate(
        ResourceTypeFilters=[
            service,
        ]
    )

    resources = []
    for page in page_iterator:
        resource_arns = jmespath.search(
            "[].ResourceARN",
            page.get('ResourceTagMappingList', [])
        )
        resources.extend(resource_arns)

    return resources
