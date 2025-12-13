from pymilvus import DataType

IDENTIFYING_MSG_SCHEMA = {
    "fields": [
        {
            "name": "id",
            "dtype": DataType.INT64,
            "is_primary": True,
            "auto_id": True
        },
        {
            "name": "merchant_id",
            "dtype": DataType.VARCHAR,
            "max_length": 24
        },
        {
            "name": "msg_id",
            "dtype": DataType.VARCHAR,
            "max_length": 24
        },
        {
            "name": "vector",
            "dtype": DataType.FLOAT_VECTOR,
            "max_length": 3072
        },
    ]
}
