# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: robot_control_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1brobot_control_service.proto\x12\rrobot_control\"\x1e\n\rspeed_message\x12\r\n\x05speed\x18\x01 \x01(\x05\"\x1e\n\x0cturn_message\x12\x0e\n\x06\x64\x65gree\x18\x01 \x01(\x05\"\x07\n\x05\x45mpty2\xa9\x03\n\x15robot_control_handler\x12\x42\n\x12robot_move_forward\x12\x14.robot_control.Empty\x1a\x14.robot_control.Empty\"\x00\x12\x43\n\x13robot_move_backward\x12\x14.robot_control.Empty\x1a\x14.robot_control.Empty\"\x00\x12@\n\x10robot_turn_right\x12\x14.robot_control.Empty\x1a\x14.robot_control.Empty\"\x00\x12?\n\x0frobot_turn_left\x12\x14.robot_control.Empty\x1a\x14.robot_control.Empty\"\x00\x12;\n\x0brobot_break\x12\x14.robot_control.Empty\x1a\x14.robot_control.Empty\"\x00\x12G\n\x0frobot_set_speed\x12\x1c.robot_control.speed_message\x1a\x14.robot_control.Empty\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'robot_control_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SPEED_MESSAGE._serialized_start=46
  _SPEED_MESSAGE._serialized_end=76
  _TURN_MESSAGE._serialized_start=78
  _TURN_MESSAGE._serialized_end=108
  _EMPTY._serialized_start=110
  _EMPTY._serialized_end=117
  _ROBOT_CONTROL_HANDLER._serialized_start=120
  _ROBOT_CONTROL_HANDLER._serialized_end=545
# @@protoc_insertion_point(module_scope)
