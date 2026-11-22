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
    'analytics.proto'
)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x61nalytics.proto\x12\tanalytics\"\xbc\x01\n\x0f\x41nalyticsResult\x12\n\n\x02id\x18\x01 \x01(\t\x12\x17\n\nproduct_id\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x1e\n\x11recommendation_id\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x15\n\ranalysis_type\x18\x04 \x01(\t\x12\x14\n\x0cmetrics_json\x18\x05 \x01(\t\x12\x12\n\ncreated_at\x18\x06 \x01(\tB\r\n\x0b_product_idB\x14\n\x12_recommendation_id\"B\n\x12ListResultsRequest\x12\x1a\n\ranalysis_type\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x10\n\x0e_analysis_type\"B\n\x13ListResultsResponse\x12+\n\x07results\x18\x01 \x03(\x0b\x32\x1a.analytics.AnalyticsResult\"\xd2\x02\n\x12RunAnalysisRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x15\n\ranalysis_type\x18\x02 \x01(\t\x12\x0f\n\x07records\x18\x03 \x01(\x05\x12\x16\n\x0etotal_quantity\x18\x04 \x01(\x05\x12\x1a\n\x12\x61verage_unit_price\x18\x05 \x01(\t\x12\x1d\n\x10predicted_demand\x18\x06 \x01(\tH\x00\x88\x01\x01\x12\x1a\n\rcurrent_price\x18\x07 \x01(\tH\x01\x88\x01\x01\x12\x1e\n\x11recommended_price\x18\x08 \x01(\tH\x02\x88\x01\x01\x12\x1e\n\x11recommendation_id\x18\t \x01(\tH\x03\x88\x01\x01\x42\x13\n\x11_predicted_demandB\x10\n\x0e_current_priceB\x14\n\x12_recommended_priceB\x14\n\x12_recommendation_id2\xaa\x01\n\x10\x41nalyticsService\x12L\n\x0bListResults\x12\x1d.analytics.ListResultsRequest\x1a\x1e.analytics.ListResultsResponse\x12H\n\x0bRunAnalysis\x12\x1d.analytics.RunAnalysisRequest\x1a\x1a.analytics.AnalyticsResultb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'analytics_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANALYTICSRESULT']._serialized_start=31
  _globals['_ANALYTICSRESULT']._serialized_end=219
  _globals['_LISTRESULTSREQUEST']._serialized_start=221
  _globals['_LISTRESULTSREQUEST']._serialized_end=287
  _globals['_LISTRESULTSRESPONSE']._serialized_start=289
  _globals['_LISTRESULTSRESPONSE']._serialized_end=355
  _globals['_RUNANALYSISREQUEST']._serialized_start=358
  _globals['_RUNANALYSISREQUEST']._serialized_end=696
  _globals['_ANALYTICSSERVICE']._serialized_start=699
  _globals['_ANALYTICSSERVICE']._serialized_end=869
