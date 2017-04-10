from __future__ import absolute_import, division, print_function

import os

try:
    import std_msgs.msg as std_msgs
except ImportError:
    # Because we need to access Ros message types here (from ROS env or from virtualenv, or from somewhere else)
    import pyros_setup
    # We rely on default configuration to point us ot the proper distro
    pyros_setup.configurable_import().configure().activate()
    import std_msgs.msg as std_msgs


# TODO : find a better place for this ?
from pyros_msgs.typecheck.ros_genmsg_py import import_msgsrv

# a dynamically generated message type just for testing...
test_opt_std_empty_as_array = import_msgsrv(
    os.path.join(os.path.dirname(__file__), 'msg', 'test_opt_std_empty_as_array.msg'),
    dependencies=['std_msgs']
)

import pyros_msgs.opt_as_array
# patching (need to know the field name)
pyros_msgs.opt_as_array.duck_punch(test_opt_std_empty_as_array, ['data'])

import pytest

import hypothesis
import hypothesis.strategies


@hypothesis.given(hypothesis.strategies.lists(hypothesis.strategies.builds(std_msgs.Empty), max_size=1))
def test_init_rosdata(data):
    msg = test_opt_std_empty_as_array(data=data)
    assert msg.data == data


@hypothesis.given(hypothesis.strategies.builds(std_msgs.Empty))
def test_init_data(data):
    msg = test_opt_std_empty_as_array(data=data)
    assert msg.data == [data]


@hypothesis.given(hypothesis.strategies.builds(std_msgs.Empty))
def test_init_raw(data):
    msg = test_opt_std_empty_as_array(data)
    assert msg.data == [data]


def test_init_default():
    msg = test_opt_std_empty_as_array()
    assert msg.data == []


# Just in case we run this directly
if __name__ == '__main__':
    pytest.main(['-s', __file__])
