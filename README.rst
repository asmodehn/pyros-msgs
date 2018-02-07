|Build Status|

Pyros-msgs
==========

Package enabling ROS communication for other Pyros multiprocess
systems.

Features
--------

ROS
~~~

-  optional field as a ROS array
-  optional field indicated by a specific message type

.. |Build Status| image:: https://travis-ci.org/pyros-dev/pyros-msgs.svg?branch=master
   :target: https://travis-ci.org/pyros-dev/pyros-msgs


Testing
-------

1) make sure you have downloaded the submodules (ros message definitions)
2) check `tox -l` to list the test environments
3) choose the tests matching your platform and run them

The tests are also run on travis, so any pull request need to have tests failing at first ( create test to illustrate the problem if needed).
Then add commits to fix the broken tests, and all must pass before merging.
