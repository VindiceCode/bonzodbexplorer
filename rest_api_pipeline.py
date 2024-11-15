from typing import Any

import dlt
from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_resources,
)

# Prompt for the hardcoded API key
API_KEY = input("Enter your API key: ")


# Function to get pipeline stage from user
def get_pipeline_stage():
    return input("Enter the pipeline stage: ")


@dlt.source(name="bonzo")
def bonzo_source() -> Any:
    # Call the function to get the pipeline stage from user input
    pipeline_stage = get_pipeline_stage()

    config: RESTAPIConfig = {
        "client": {
            "base_url": "http://app.getbonzo.com/api/v3",
            "auth": {
                "type": "bearer",
                "token": API_KEY,
            },
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
            "endpoint": {
                "params": {
                    "per_page": 100,  # Adjust based on the API's support
                },
            },
        },
        "resources": [
            # Adjusted to focus on the 'prospect' resource with dynamic pipeline stage
            {
                "name": "prospect",
                "endpoint": {
                    "path": f"pipeline-stages/{pipeline_stage}/prospects",  # Use the user-provided pipeline stage
                    "params": {
                        "per_page": 15,
                        "page": 1,
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_bonzo() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_bonzo",
        destination="duckdb",
        dataset_name="bonzo_data",
    )

    load_info = pipeline.run(bonzo_source())
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    load_bonzo()
