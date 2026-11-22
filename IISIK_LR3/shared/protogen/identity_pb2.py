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
    'identity.proto'
)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eidentity.proto\x12\x08identity\x1a\x1bgoogle/protobuf/empty.proto\"[\n\x04User\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x11\n\tis_active\x18\x04 \x01(\x08\x12\x12\n\ncreated_at\x18\x05 \x01(\t\"I\n\x0b\x41uthPayload\x12\r\n\x05token\x18\x01 \x01(\t\x12\x1c\n\x04user\x18\x02 \x01(\x0b\x32\x0e.identity.User\x12\r\n\x05roles\x18\x03 \x03(\t\"/\n\x0cLoginRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"E\n\x0fRegisterRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\"\x1e\n\rLogoutRequest\x12\r\n\x05token\x18\x01 \x01(\t\"\"\n\x11IntrospectRequest\x12\r\n\x05token\x18\x01 \x01(\t\"V\n\x12IntrospectResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05roles\x18\x04 \x03(\t2\x8b\x02\n\x0fIdentityService\x12\x36\n\x05Login\x12\x16.identity.LoginRequest\x1a\x15.identity.AuthPayload\x12<\n\x08Register\x12\x19.identity.RegisterRequest\x1a\x15.identity.AuthPayload\x12\x39\n\x06Logout\x12\x17.identity.LogoutRequest\x1a\x16.google.protobuf.Empty\x12G\n\nIntrospect\x12\x1b.identity.IntrospectRequest\x1a\x1c.identity.IntrospectResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'identity_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USER']._serialized_start=57
  _globals['_USER']._serialized_end=148
  _globals['_AUTHPAYLOAD']._serialized_start=150
  _globals['_AUTHPAYLOAD']._serialized_end=223
  _globals['_LOGINREQUEST']._serialized_start=225
  _globals['_LOGINREQUEST']._serialized_end=272
  _globals['_REGISTERREQUEST']._serialized_start=274
  _globals['_REGISTERREQUEST']._serialized_end=343
  _globals['_LOGOUTREQUEST']._serialized_start=345
  _globals['_LOGOUTREQUEST']._serialized_end=375
  _globals['_INTROSPECTREQUEST']._serialized_start=377
  _globals['_INTROSPECTREQUEST']._serialized_end=411
  _globals['_INTROSPECTRESPONSE']._serialized_start=413
  _globals['_INTROSPECTRESPONSE']._serialized_end=499
  _globals['_IDENTITYSERVICE']._serialized_start=502
  _globals['_IDENTITYSERVICE']._serialized_end=769
