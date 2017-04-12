from __future__ import absolute_import, division, print_function

import os
import sys

import genpy

# TODO : find a better place for this ?
from pyros_msgs.importer.rosmsg_generator import generate_msgsrv_nspkg, import_msgsrv

# a dynamically generated message type just for testing...
generated_modules = generate_msgsrv_nspkg(
    [os.path.join(os.path.dirname(__file__), 'msg', 'test_opt_time_as_array.msg')],
    ns_pkg=True
)
for m in generated_modules:
    import_msgsrv(m)

test_opt_time_as_array = getattr(sys.modules['gen_msgs.msg._test_opt_time_as_array'], 'test_opt_time_as_array')

import pyros_msgs.opt_as_array
# patching (need to know the field name)
pyros_msgs.opt_as_array.duck_punch(test_opt_time_as_array, ['data'])

import pytest
import hypothesis
import hypothesis.strategies


@hypothesis.given(hypothesis.strategies.lists(
    hypothesis.strategies.builds(
        genpy.Time,
        secs=hypothesis.strategies.integers(min_value=0, max_value=4294967295 -3),
        nsecs=hypothesis.strategies.integers(min_value=0, max_value=4294967295)
    ), max_size=1
))
def test_init_rosdata(data):
    msg = test_opt_time_as_array(data=data)
    assert msg.data == data


@hypothesis.given(
    hypothesis.strategies.builds(
        genpy.Time,
        secs=hypothesis.strategies.integers(min_value=0, max_value=4294967295 -3),
        nsecs=hypothesis.strategies.integers(min_value=0, max_value=4294967295)
    )
)
def test_init_data(data):
    msg = test_opt_time_as_array(data=data)
    assert msg.data == [data]


@hypothesis.given(
    hypothesis.strategies.builds(
        genpy.Time,
        secs=hypothesis.strategies.integers(min_value=0, max_value=4294967295 -3),
        nsecs=hypothesis.strategies.integers(min_value=0, max_value=4294967295)
    )
)
def test_init_raw(data):
    msg = test_opt_time_as_array(data)
    assert msg.data == [data]


def test_init_default():
    msg = test_opt_time_as_array()
    assert msg.data == []


# TODO : test_wrong_init_except(data) check typecheck.tests.test_ros_mappings

# Just in case we run this directly
if __name__ == '__main__':
    pytest.main(['-s', __file__])
