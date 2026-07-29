import json

from engine.content_pipeline_adapter import ContentPipelineAdapter


adapter = ContentPipelineAdapter()


result = adapter.generate(
    {
        "product_id": "CHK24_001",
        "name": "Strom",
        "partner": "check24",
        "category": "Strom"
    }
)


print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    )
)
