from __future__ import absolute_import, division, print_function

from pyros_msgs.msg import (
    # no slot
    # None

    # data slot
    opt_empty,

    opt_bool,
    opt_int8, opt_int16, opt_int32, opt_int64,
    opt_uint8, opt_uint16, opt_uint32, opt_uint64,
    opt_float32, opt_float64,
    opt_string,

    opt_time,
    opt_duration,
    opt_header,

    # multiple slots
    # None
)

from pyros_msgs.common import ros_opt_as_nested_type_default_mapping

import genpy
import std_msgs.msg


def duck_punch(msg_mod):
    def init_punch(self, *args, **kwds):
        __doc__ = msg_mod.__init__.__doc__
        # excepting when passing initialized_. it is meant to be an internal field.
        if 'initialized_' in kwds.keys():
            raise AttributeError("The field 'initialized_' is an internal field of {0} and should not be set by the user.".format(msg_mod._type))
        if args:  # the args for super(msg_mod, self) are fixed to the slots in ros messages
            # so we can change it to kwarg to be more accepting (and more robust for changes)
            kwds.update(zip([s for s in self.__slots__ if s != 'initialized_'], args))

        if kwds:
            # special case for string type(to support unicode kwds)
            for s, st in zip(self.__slots__, self._slot_types):
                if st == 'string':
                    kwds[s] = str(kwds.get(s, ""))

            # ROS messages accept either args or kwargs, not both
            super(msg_mod, self).__init__(**kwds)
            # initialized value depends on all field assigned
            if 'data' in self.__slots__ and self.data is None:
                self.data = self._default_value
                self.initialized_ = False
            else:
                self.initialized_ = True
        else:
            self.initialized_ = False
            if 'data' in self.__slots__:
                self.data = self._default_value

    # duck punching into genpy generated message classes, to set initialized_ field properly
    msg_mod.__init__ = init_punch

    # adding settable default value behavior (doesnt matter for empty type though)
    msg_mod._default_value = ros_opt_as_nested_type_default_mapping[msg_mod._type]

    def reset_default(cls, new_default_value=None):
        cls._default_value = new_default_value or ros_opt_as_nested_type_default_mapping[msg_mod._type]

    msg_mod.reset_default = classmethod(reset_default)


#
# default data values extracted from genpy.generator:default_value()
#

for msg_int_mod in [
    opt_int8, opt_int16, opt_int32, opt_int64,
    opt_uint8, opt_uint16, opt_uint32, opt_uint64,
]:
    duck_punch(msg_int_mod)

for msg_float_mod in [
    opt_float32, opt_float64,
]:
    duck_punch(msg_float_mod)

duck_punch(opt_string)
duck_punch(opt_bool)

duck_punch(opt_time)
duck_punch(opt_duration)

#duck_punch(opt_header, std_msgs.msg.Header())

