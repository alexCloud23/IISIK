"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    7,
    35,
    1,
    '',
    'strategy.proto'
)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0estrategy.proto\x12\x08strategy\"\x82\x02\n\x08Strategy\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nproduct_id\x18\x02 \x01(\t\x12\x17\n\x0f\x63ompetitor_name\x18\x03 \x01(\t\x12\x15\n\rstrategy_type\x18\x04 \x01(\t\x12\x18\n\x10\x63ompetitor_price\x18\x05 \x01(\t\x12!\n\x14price_change_percent\x18\x06 \x01(\tH\x00\x88\x01\x01\x12\"\n\x15\x65stimated_probability\x18\x07 \x01(\tH\x01\x88\x01\x01\x12\x12\n\ncreated_at\x18\x08 \x01(\tB\x17\n\x15_price_change_percentB\x18\n\x16_estimated_probability\"?\n\x15ListStrategiesRequest\x12\x17\n\nproduct_id\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\r\n\x0b_product_id\"@\n\x16ListStrategiesResponse\x12&\n\nstrategies\x18\x01 \x03(\x0b\x32\x12.strategy.Strategy\"h\n\x14\x43ompetitorPricePoint\x12\x17\n\x0f\x63ompetitor_name\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\t\x12\x18\n\x0bobserved_at\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0e\n\x0c_observed_at\"~\n\x16\x41nalyzeStrategyRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x15\n\rcurrent_price\x18\x02 \x01(\t\x12\x39\n\x11\x63ompetitor_prices\x18\x03 \x03(\x0b\x32\x1e.strategy.CompetitorPricePoint2\xaf\x01\n\x0fStrategyService\x12S\n\x0eListStrategies\x12\x1f.strategy.ListStrategiesRequest\x1a .strategy.ListStrategiesResponse\x12G\n\x0f\x41nalyzeStrategy\x12 .strategy.AnalyzeStrategyRequest\x1a\x12.strategy.Strategyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'strategy_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STRATEGY']._serialized_start=29
  _globals['_STRATEGY']._serialized_end=287
  _globals['_LISTSTRATEGIESREQUEST']._serialized_start=289
  _globals['_LISTSTRATEGIESREQUEST']._serialized_end=352
  _globals['_LISTSTRATEGIESRESPONSE']._serialized_start=354
  _globals['_LISTSTRATEGIESRESPONSE']._serialized_end=418
  _globals['_COMPETITORPRICEPOINT']._serialized_start=420
  _globals['_COMPETITORPRICEPOINT']._serialized_end=524
  _globals['_ANALYZESTRATEGYREQUEST']._serialized_start=526
  _globals['_ANALYZESTRATEGYREQUEST']._serialized_end=652
  _globals['_STRATEGYSERVICE']._serialized_start=655
  _globals['_STRATEGYSERVICE']._serialized_end=830
