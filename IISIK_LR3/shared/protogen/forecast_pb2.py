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
    'forecast.proto'
)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x66orecast.proto\x12\x08\x66orecast\"\xc1\x01\n\x08\x46orecast\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nproduct_id\x18\x02 \x01(\t\x12\x14\n\x0cperiod_start\x18\x03 \x01(\t\x12\x12\n\nperiod_end\x18\x04 \x01(\t\x12\x18\n\x10predicted_demand\x18\x05 \x01(\t\x12\x17\n\nconfidence\x18\x06 \x01(\tH\x00\x88\x01\x01\x12\x15\n\rmodel_version\x18\x07 \x01(\t\x12\x12\n\ncreated_at\x18\x08 \x01(\tB\r\n\x0b_confidence\">\n\x14ListForecastsRequest\x12\x17\n\nproduct_id\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\r\n\x0b_product_id\">\n\x15ListForecastsResponse\x12%\n\tforecasts\x18\x01 \x03(\x0b\x32\x12.forecast.Forecast\" \n\x12GetForecastRequest\x12\n\n\x02id\x18\x01 \x01(\t\"M\n\x13GetForecastResponse\x12)\n\x08\x66orecast\x18\x01 \x01(\x0b\x32\x12.forecast.ForecastH\x00\x88\x01\x01\x42\x0b\n\t_forecast\".\n\tSalePoint\x12\x10\n\x08quantity\x18\x01 \x01(\x05\x12\x0f\n\x07sold_at\x18\x02 \x01(\t\"f\n\x17GenerateForecastRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x13\n\x0bperiod_days\x18\x02 \x01(\x05\x12\"\n\x05sales\x18\x03 \x03(\x0b\x32\x13.forecast.SalePoint2\xfa\x01\n\x0f\x46orecastService\x12P\n\rListForecasts\x12\x1e.forecast.ListForecastsRequest\x1a\x1f.forecast.ListForecastsResponse\x12J\n\x0bGetForecast\x12\x1c.forecast.GetForecastRequest\x1a\x1d.forecast.GetForecastResponse\x12I\n\x10GenerateForecast\x12!.forecast.GenerateForecastRequest\x1a\x12.forecast.Forecastb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'forecast_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FORECAST']._serialized_start=29
  _globals['_FORECAST']._serialized_end=222
  _globals['_LISTFORECASTSREQUEST']._serialized_start=224
  _globals['_LISTFORECASTSREQUEST']._serialized_end=286
  _globals['_LISTFORECASTSRESPONSE']._serialized_start=288
  _globals['_LISTFORECASTSRESPONSE']._serialized_end=350
  _globals['_GETFORECASTREQUEST']._serialized_start=352
  _globals['_GETFORECASTREQUEST']._serialized_end=384
  _globals['_GETFORECASTRESPONSE']._serialized_start=386
  _globals['_GETFORECASTRESPONSE']._serialized_end=463
  _globals['_SALEPOINT']._serialized_start=465
  _globals['_SALEPOINT']._serialized_end=511
  _globals['_GENERATEFORECASTREQUEST']._serialized_start=513
  _globals['_GENERATEFORECASTREQUEST']._serialized_end=615
  _globals['_FORECASTSERVICE']._serialized_start=618
  _globals['_FORECASTSERVICE']._serialized_end=868
