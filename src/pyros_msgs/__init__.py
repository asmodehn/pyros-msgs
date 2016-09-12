try:
    import std_msgs
except ImportError:
    # Because we need to access Ros message types here (from ROS env or from virtualenv, or from somewhere else)
    import pyros_setup
    # We rely on default configuration to point us ot the proper distro
    pyros_setup.configurable_import().configure().activate()
    import std_msgs


from .decorators import wraps_cls, with_explicitly_matched_type
from .std_bool import RosFieldBool, RosMsgBool
from .std_int import (
    RosFieldInt8, RosFieldInt16, RosFieldInt32, RosFieldInt64, RosFieldUInt8, RosFieldUInt16, RosFieldUInt32, RosFieldUInt64,
    RosMsgInt8, RosMsgInt16, RosMsgInt32, RosMsgInt64, RosMsgUInt8, RosMsgUInt16, RosMsgUInt32, RosMsgUInt64
)
from .std_float import RosFieldFloat32, RosFieldFloat64, RosMsgFloat32, RosMsgFloat64
from .std_string import RosFieldString, RosMsgString
from .std_time import RosFieldTime, RosMsgTime
from .std_duration import RosFieldDuration, RosMsgDuration

__all__ = [
    'with_explicitly_matched_type',
    'RosFieldBool', 'RosMsgBool',
    'RosFieldInt8', 'RosFieldInt16', 'RosFieldInt32', 'RosFieldInt64', 'RosFieldUInt8', 'RosFieldUInt16', 'RosFieldUInt32', 'RosFieldUInt64',
    'RosMsgInt8', 'RosMsgInt16', 'RosMsgInt32', 'RosMsgInt64', 'RosMsgUInt8', 'RosMsgUInt16', 'RosMsgUInt32', 'RosMsgUInt64',
    'RosFieldFloat32', 'RosFieldFloat64', 'RosMsgFloat32', 'RosMsgFloat64',
    'RosFieldString', 'RosMsgString',
    'RosFieldTime', 'RosMsgTime',
    'RosFieldDuration', 'RosMsgDuration',
]
