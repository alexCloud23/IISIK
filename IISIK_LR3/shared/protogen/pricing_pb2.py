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
    'pricing.proto'
)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rpricing.proto\x12\x07pricing\x1a\x1bgoogle/protobuf/empty.proto\"\xe7\x01\n\x0eRecommendation\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nproduct_id\x18\x02 \x01(\t\x12\x13\n\x0b\x66orecast_id\x18\x03 \x01(\t\x12\x18\n\x0bstrategy_id\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x15\n\rcurrent_price\x18\x05 \x01(\t\x12\x19\n\x11recommended_price\x18\x06 \x01(\t\x12\x10\n\x08\x63urrency\x18\x07 \x01(\t\x12\x0e\n\x06reason\x18\x08 \x01(\t\x12\x0e\n\x06status\x18\t \x01(\t\x12\x12\n\ncreated_at\x18\n \x01(\tB\x0e\n\x0c_strategy_id\"\x81\x01\n\x1aListRecommendationsRequest\x12\x17\n\nproduct_id\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x13\n\x06status\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x0c\n\x04sort\x18\x03 \x01(\t\x12\r\n\x05order\x18\x04 \x01(\tB\r\n\x0b_product_idB\t\n\x07_status\"O\n\x1bListRecommendationsResponse\x12\x30\n\x0frecommendations\x18\x01 \x03(\x0b\x32\x17.pricing.Recommendation\"&\n\x18GetRecommendationRequest\x12\n\n\x02id\x18\x01 \x01(\t\"d\n\x19GetRecommendationResponse\x12\x34\n\x0erecommendation\x18\x01 \x01(\x0b\x32\x17.pricing.RecommendationH\x00\x88\x01\x01\x42\x11\n\x0f_recommendation\"\xe9\x01\n\x1b\x43reateRecommendationRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x13\n\x0b\x66orecast_id\x18\x02 \x01(\t\x12\x15\n\rcurrent_price\x18\x03 \x01(\t\x12\x1a\n\rstrategy_type\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x1d\n\x10\x63ompetitor_price\x18\x05 \x01(\tH\x01\x88\x01\x01\x12\x18\n\x0bstrategy_id\x18\x06 \x01(\tH\x02\x88\x01\x01\x42\x10\n\x0e_strategy_typeB\x13\n\x11_competitor_priceB\x0e\n\x0c_strategy_id\";\n\x1b\x44\x65\x63ideRecommendationRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08\x64\x65\x63ision\x18\x02 \x01(\t\"`\n\x1eRecommendationsSummaryResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0b\n\x03new\x18\x02 \x01(\x05\x12\x10\n\x08\x61\x63\x63\x65pted\x18\x03 \x01(\x05\x12\x10\n\x08rejected\x18\x04 \x01(\x05\x32\xd7\x03\n\x0ePricingService\x12`\n\x13ListRecommendations\x12#.pricing.ListRecommendationsRequest\x1a$.pricing.ListRecommendationsResponse\x12Z\n\x11GetRecommendation\x12!.pricing.GetRecommendationRequest\x1a\".pricing.GetRecommendationResponse\x12U\n\x14\x43reateRecommendation\x12$.pricing.CreateRecommendationRequest\x1a\x17.pricing.Recommendation\x12U\n\x14\x44\x65\x63ideRecommendation\x12$.pricing.DecideRecommendationRequest\x1a\x17.pricing.Recommendation\x12Y\n\x16RecommendationsSummary\x12\x16.google.protobuf.Empty\x1a\'.pricing.RecommendationsSummaryResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pricing_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RECOMMENDATION']._serialized_start=56
  _globals['_RECOMMENDATION']._serialized_end=287
  _globals['_LISTRECOMMENDATIONSREQUEST']._serialized_start=290
  _globals['_LISTRECOMMENDATIONSREQUEST']._serialized_end=419
  _globals['_LISTRECOMMENDATIONSRESPONSE']._serialized_start=421
  _globals['_LISTRECOMMENDATIONSRESPONSE']._serialized_end=500
  _globals['_GETRECOMMENDATIONREQUEST']._serialized_start=502
  _globals['_GETRECOMMENDATIONREQUEST']._serialized_end=540
  _globals['_GETRECOMMENDATIONRESPONSE']._serialized_start=542
  _globals['_GETRECOMMENDATIONRESPONSE']._serialized_end=642
  _globals['_CREATERECOMMENDATIONREQUEST']._serialized_start=645
  _globals['_CREATERECOMMENDATIONREQUEST']._serialized_end=878
  _globals['_DECIDERECOMMENDATIONREQUEST']._serialized_start=880
  _globals['_DECIDERECOMMENDATIONREQUEST']._serialized_end=939
  _globals['_RECOMMENDATIONSSUMMARYRESPONSE']._serialized_start=941
  _globals['_RECOMMENDATIONSSUMMARYRESPONSE']._serialized_end=1037
  _globals['_PRICINGSERVICE']._serialized_start=1040
  _globals['_PRICINGSERVICE']._serialized_end=1511
