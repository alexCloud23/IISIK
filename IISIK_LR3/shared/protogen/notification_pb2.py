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
    'notification.proto'
)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12notification.proto\x12\x0cnotification\x1a\x1bgoogle/protobuf/empty.proto\"\xf3\x01\n\x0cNotification\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x19\n\x11notification_type\x18\x03 \x01(\t\x12\r\n\x05title\x18\x04 \x01(\t\x12\x0f\n\x07message\x18\x05 \x01(\t\x12\x1e\n\x11related_entity_id\x18\x06 \x01(\tH\x00\x88\x01\x01\x12\x0e\n\x06status\x18\x07 \x01(\t\x12\x0f\n\x07is_read\x18\x08 \x01(\x08\x12\x12\n\ncreated_at\x18\t \x01(\t\x12\x14\n\x07sent_at\x18\n \x01(\tH\x01\x88\x01\x01\x42\x14\n\x12_related_entity_idB\n\n\x08_sent_at\"r\n\x18ListNotificationsRequest\x12\x14\n\x07is_read\x18\x01 \x01(\x08H\x00\x88\x01\x01\x12\x1e\n\x11notification_type\x18\x02 \x01(\tH\x01\x88\x01\x01\x42\n\n\x08_is_readB\x14\n\x12_notification_type\"N\n\x19ListNotificationsResponse\x12\x31\n\rnotifications\x18\x01 \x03(\x0b\x32\x1a.notification.Notification\"%\n\x13UnreadCountResponse\x12\x0e\n\x06unread\x18\x01 \x01(\x05\"\xae\x01\n\x19\x43reateNotificationRequest\x12\x19\n\x11notification_type\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x1e\n\x11related_entity_id\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07user_id\x18\x05 \x01(\tH\x01\x88\x01\x01\x42\x14\n\x12_related_entity_idB\n\n\x08_user_id\")\n\x1bMarkNotificationReadRequest\x12\n\n\x02id\x18\x01 \x01(\t\"&\n\x13MarkAllReadResponse\x12\x0f\n\x07updated\x18\x01 \x01(\x05\x32\xd9\x03\n\x13NotificationService\x12\x64\n\x11ListNotifications\x12&.notification.ListNotificationsRequest\x1a\'.notification.ListNotificationsResponse\x12K\n\x0eGetUnreadCount\x12\x16.google.protobuf.Empty\x1a!.notification.UnreadCountResponse\x12Y\n\x12\x43reateNotification\x12\'.notification.CreateNotificationRequest\x1a\x1a.notification.Notification\x12]\n\x14MarkNotificationRead\x12).notification.MarkNotificationReadRequest\x1a\x1a.notification.Notification\x12U\n\x18MarkAllNotificationsRead\x12\x16.google.protobuf.Empty\x1a!.notification.MarkAllReadResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'notification_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_NOTIFICATION']._serialized_start=66
  _globals['_NOTIFICATION']._serialized_end=309
  _globals['_LISTNOTIFICATIONSREQUEST']._serialized_start=311
  _globals['_LISTNOTIFICATIONSREQUEST']._serialized_end=425
  _globals['_LISTNOTIFICATIONSRESPONSE']._serialized_start=427
  _globals['_LISTNOTIFICATIONSRESPONSE']._serialized_end=505
  _globals['_UNREADCOUNTRESPONSE']._serialized_start=507
  _globals['_UNREADCOUNTRESPONSE']._serialized_end=544
  _globals['_CREATENOTIFICATIONREQUEST']._serialized_start=547
  _globals['_CREATENOTIFICATIONREQUEST']._serialized_end=721
  _globals['_MARKNOTIFICATIONREADREQUEST']._serialized_start=723
  _globals['_MARKNOTIFICATIONREADREQUEST']._serialized_end=764
  _globals['_MARKALLREADRESPONSE']._serialized_start=766
  _globals['_MARKALLREADRESPONSE']._serialized_end=804
  _globals['_NOTIFICATIONSERVICE']._serialized_start=807
  _globals['_NOTIFICATIONSERVICE']._serialized_end=1280
