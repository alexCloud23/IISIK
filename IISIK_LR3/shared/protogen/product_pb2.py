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
    'product.proto'
)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rproduct.proto\x12\x07product\"\xc0\x01\n\x07Product\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x18\n\x0b\x64\x65scription\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x10\n\x08\x63\x61tegory\x18\x04 \x01(\t\x12\x12\n\nbase_price\x18\x05 \x01(\t\x12\x10\n\x08\x63urrency\x18\x06 \x01(\t\x12\x11\n\tis_active\x18\x07 \x01(\x08\x12\x12\n\ncreated_at\x18\x08 \x01(\t\x12\x12\n\nupdated_at\x18\t \x01(\tB\x0e\n\x0c_description\"\xe8\x01\n\x13ListProductsRequest\x12\x15\n\x08\x63\x61tegory\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tis_active\x18\x02 \x01(\x08H\x01\x88\x01\x01\x12\x13\n\x06search\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x16\n\tmin_price\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x16\n\tmax_price\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x0c\n\x04sort\x18\x06 \x01(\t\x12\r\n\x05order\x18\x07 \x01(\tB\x0b\n\t_categoryB\x0c\n\n_is_activeB\t\n\x07_searchB\x0c\n\n_min_priceB\x0c\n\n_max_price\":\n\x14ListProductsResponse\x12\"\n\x08products\x18\x01 \x03(\x0b\x32\x10.product.Product\"\x1f\n\x11GetProductRequest\x12\n\n\x02id\x18\x01 \x01(\t\"H\n\x12GetProductResponse\x12&\n\x07product\x18\x01 \x01(\x0b\x32\x10.product.ProductH\x00\x88\x01\x01\x42\n\n\x08_product\"\x86\x01\n\x14\x43reateProductRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x18\n\x0b\x64\x65scription\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x10\n\x08\x63\x61tegory\x18\x03 \x01(\t\x12\x12\n\nbase_price\x18\x04 \x01(\t\x12\x10\n\x08\x63urrency\x18\x05 \x01(\tB\x0e\n\x0c_description\"\x9a\x01\n\x14UpdateProductRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x17\n\nbase_price\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0b\x64\x65scription\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x16\n\tis_active\x18\x04 \x01(\x08H\x02\x88\x01\x01\x42\r\n\x0b_base_priceB\x0e\n\x0c_descriptionB\x0c\n\n_is_active2\xa8\x02\n\x0eProductService\x12K\n\x0cListProducts\x12\x1c.product.ListProductsRequest\x1a\x1d.product.ListProductsResponse\x12\x45\n\nGetProduct\x12\x1a.product.GetProductRequest\x1a\x1b.product.GetProductResponse\x12@\n\rCreateProduct\x12\x1d.product.CreateProductRequest\x1a\x10.product.Product\x12@\n\rUpdateProduct\x12\x1d.product.UpdateProductRequest\x1a\x10.product.Productb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'product_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRODUCT']._serialized_start=27
  _globals['_PRODUCT']._serialized_end=219
  _globals['_LISTPRODUCTSREQUEST']._serialized_start=222
  _globals['_LISTPRODUCTSREQUEST']._serialized_end=454
  _globals['_LISTPRODUCTSRESPONSE']._serialized_start=456
  _globals['_LISTPRODUCTSRESPONSE']._serialized_end=514
  _globals['_GETPRODUCTREQUEST']._serialized_start=516
  _globals['_GETPRODUCTREQUEST']._serialized_end=547
  _globals['_GETPRODUCTRESPONSE']._serialized_start=549
  _globals['_GETPRODUCTRESPONSE']._serialized_end=621
  _globals['_CREATEPRODUCTREQUEST']._serialized_start=624
  _globals['_CREATEPRODUCTREQUEST']._serialized_end=758
  _globals['_UPDATEPRODUCTREQUEST']._serialized_start=761
  _globals['_UPDATEPRODUCTREQUEST']._serialized_end=915
  _globals['_PRODUCTSERVICE']._serialized_start=918
  _globals['_PRODUCTSERVICE']._serialized_end=1214
