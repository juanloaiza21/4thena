from pymilvus import DataType, MilvusClient

IDENTIFYING_MSG_SCHEMA = MilvusClient.create_schema()

IDENTIFYING_MSG_SCHEMA.add_field(
    field_name="id",
    datatype=DataType.INT64,
    is_primary=True,
    auto_id=True
).add_field(
    field_name="merchant_id",
    datatype=DataType.VARCHAR,
    max_length=24
).add_field(
    field_name="msg_id",
    datatype=DataType.VARCHAR,
    max_length=24
).add_field(
    field_name="vector",
    datatype=DataType.FLOAT_VECTOR,
    dim=3072
)

RAG_SCHEMA = MilvusClient.create_schema()

RAG_SCHEMA.add_field(
    field_name="id",
    datatype=DataType.INT64,
    is_primary=True,
    auto_id=True
).add_field(
    field_name="merchant_id",
    datatype=DataType.VARCHAR,
    max_length=24
).add_field(
    field_name="msg_id",
    datatype=DataType.VARCHAR,
    max_length=24
).add_field(
    field_name="vector",
    datatype=DataType.FLOAT_VECTOR,
    dim=3072
)
