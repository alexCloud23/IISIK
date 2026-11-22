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
    'market_data.proto'
)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11market_data.proto\x12\nmarketdata\"v\n\x0bSalesRecord\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nproduct_id\x18\x02 \x01(\t\x12\x10\n\x08quantity\x18\x03 \x01(\x05\x12\x12\n\nunit_price\x18\x04 \x01(\t\x12\x10\n\x08\x63urrency\x18\x05 \x01(\t\x12\x0f\n\x07sold_at\x18\x06 \x01(\t\"\x90\x01\n\x0f\x43ompetitorPrice\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nproduct_id\x18\x02 \x01(\t\x12\x17\n\x0f\x63ompetitor_name\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\t\x12\x10\n\x08\x63urrency\x18\x05 \x01(\t\x12\x0e\n\x06source\x18\x06 \x01(\t\x12\x13\n\x0bobserved_at\x18\x07 \x01(\t\")\n\x13SalesSummaryRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\t\"o\n\x14SalesSummaryResponse\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x0f\n\x07records\x18\x02 \x01(\x05\x12\x16\n\x0etotal_quantity\x18\x03 \x01(\x05\x12\x1a\n\x12\x61verage_unit_price\x18\x04 \x01(\t\"I\n\x10ListSalesRequest\x12\x17\n\nproduct_id\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\r\n\x05limit\x18\x02 \x01(\x05\x42\r\n\x0b_product_id\";\n\x11ListSalesResponse\x12&\n\x05sales\x18\x01 \x03(\x0b\x32\x17.marketdata.SalesRecord\"T\n\x1bListCompetitorPricesRequest\x12\x17\n\nproduct_id\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\r\n\x05limit\x18\x02 \x01(\x05\x42\r\n\x0b_product_id\"K\n\x1cListCompetitorPricesResponse\x12+\n\x06prices\x18\x01 \x03(\x0b\x32\x1b.marketdata.CompetitorPrice2\x9b\x02\n\x11MarketDataService\x12Q\n\x0cSalesSummary\x12\x1f.marketdata.SalesSummaryRequest\x1a .marketdata.SalesSummaryResponse\x12H\n\tListSales\x12\x1c.marketdata.ListSalesRequest\x1a\x1d.marketdata.ListSalesResponse\x12i\n\x14ListCompetitorPrices\x12\'.marketdata.ListCompetitorPricesRequest\x1a(.marketdata.ListCompetitorPricesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'market_data_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SALESRECORD']._serialized_start=33
  _globals['_SALESRECORD']._serialized_end=151
  _globals['_COMPETITORPRICE']._serialized_start=154
  _globals['_COMPETITORPRICE']._serialized_end=298
  _globals['_SALESSUMMARYREQUEST']._serialized_start=300
  _globals['_SALESSUMMARYREQUEST']._serialized_end=341
  _globals['_SALESSUMMARYRESPONSE']._serialized_start=343
  _globals['_SALESSUMMARYRESPONSE']._serialized_end=454
  _globals['_LISTSALESREQUEST']._serialized_start=456
  _globals['_LISTSALESREQUEST']._serialized_end=529
  _globals['_LISTSALESRESPONSE']._serialized_start=531
  _globals['_LISTSALESRESPONSE']._serialized_end=590
  _globals['_LISTCOMPETITORPRICESREQUEST']._serialized_start=592
  _globals['_LISTCOMPETITORPRICESREQUEST']._serialized_end=676
  _globals['_LISTCOMPETITORPRICESRESPONSE']._serialized_start=678
  _globals['_LISTCOMPETITORPRICESRESPONSE']._serialized_end=753
  _globals['_MARKETDATASERVICE']._serialized_start=756
  _globals['_MARKETDATASERVICE']._serialized_end=1039
