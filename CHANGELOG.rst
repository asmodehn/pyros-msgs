Changelog
=========


0.2.0 (2018-02-13)
------------------
- Adding pyup config to manage dependencies. [AlexV]
- Merge pull request #14 from pyros-dev/nested_implement. [AlexV]

  Nested implement
- Fixing tests in CMakeLists. [AlexV]
- Fixing travis links in README. [AlexV]
- Added README comments about CI, tests and PR merges. [AlexV]
- Moving version to base package. cleanup hypothesis data via manifest.
  [alexv]
- Somewhat cleaner test run. Now relying on pypi released test depends.
  [alexv]
- Not testing latest python3 on ubuntu not supporting it. [alexv]
- Tox indigo test now uses debs for test tools. [alexv]
- Encode/decode already taken care of by genpy not accepting bytes for
  str since genpy currently breaks. [alexv]
- Nested implementations now passing tests. [alexv]
- Merge pull request #21 from asmodehn/importer. [AlexV]

  Importer
- Restructuring requirements for different tests with different
  versions... [alexv]
- Merge pull request #23 from asmodehn/travis_matrix. [AlexV]

  Travis matrix
- Attempting to fix link between travis and tox. dropping py3 fix for
  genpy dep. [alexv]
- Configuring travis matrix with tox envs. [alexv]
- Activating python3 support. [alexv]
- Restructuring to extract tests, fix package dist, replace ros
  submodules with pips. [alexv]
- Attempting to fix setup.py to include .msg. [alexv]
- Removing rosimport submodule since it has been released. [alexv]
- Fixing hypothesis deprecation warnings. [alexv]
- Moving tests out of package to avoid changing python import logic
  without the final user knowing. [alexv]
- Tox tests now passing on python 2.7 with dev version of rosimport.
  [alexv]
- Moving importer out to rosimport, and fixing tests. [alexv]
- Extracting filefinder to separate pip package. [alexv]
- Some cleanup. [alexv]
- Python2 generated modules import working! [alexv]
- Import with implicit namespace package working on 2.7. [alexv]
- WIP starting to backport for python2.7. [alexv]
- Unified ROSloaders. [AlexV]
- Importing services definitions now works on py3.4. [AlexV]
- Importlib tests passing. [AlexV]
- WIP import test passing, added pytest-boxed. [AlexV]
- WIP import tests starting to pass ! [AlexV]
- WIP python code generation starting to work... [AlexV]
- WIP extracted tests out of package to be able to test importing from
  existing python package, without having the python package already
  imported. [AlexV]
- WIP improved test structure, now using more basic unittest. [alexv]
- WIP improving ROS import finder for python 3.5. [alexv]
- WIP importer improvements. [AlexV]
- WIP improving ROS import finder for latest python 2.7. [alexv]
- WIP beginning of custom importer implementation. [AlexV]


0.1.1 (2017-05-31)
------------------
- Requiring pytest 2.5.1 to match trusty package. [AlexV]
- 0.1.1. [alexv]
- Preparing for ros release. [alexv]
- Merge pull request #16 from yotabits/nested_implement. [AlexV]

  Added test for time in opt_as_nested
- Added test for time in opt_as_nested. [Thomas]

  The actual test seems to be failing because the type checker seems to be waiting
  for int32 datatype instead of uint32
- Now nesting using type checker method instead of duplicating it.
  [AlexV]
- Merge pull request #10 from yotabits/nested_implement. [AlexV]

  Adding tests in opt_as_nested
- Added test for duration in opt_as_nested. [Thomas]
- Added test for std_empty in opt_as_nested. [Thomas]
- Added test for string in opt_as_nested. [Thomas]

  This include also a small bug fix in the typechecker, now object of type any
  can "contain" objects of type any aswell
- Stand alone working. [Thomas]
- Fixed test_opt_duration in opt_as_array. [Thomas]

  Actually Ros does not allow to have negative nano-seconds:
  1s, -100 000 000ns
  will be transformed into
  900 000 ns

  in the case we test with limit values this could create issues
  so the testing limit values have been changed
- Merge pull request #3 from asmodehn/nested_implement. [yotabits]

  Nested implement
- Fixing yaml dependency name. [AlexV]
- Adding quantified code badge. [AlexV]
- Adding yaml as dependency since our genpy source code relies on it.
  [AlexV]
- Cleaning up doc and comments. [AlexV]
- Testing... [Thomas]
- Testing... [Thomas]
- Testing... [Thomas]
- Added test for uint64 in opt_as_nested. [Thomas]
- Added test for uint32 in opt_as_nested. [Thomas]
- Added test for uint16 in opt_as_nested. [Thomas]
- Added test for uint8 in opt_as_nested. [Thomas]
- Adapted all int type size tests. [Thomas]
- Merge pull request #2 from asmodehn/nested_implement. [yotabits]

  Nested implement
- Merge pull request #9 from asmodehn/fixing_catkin_tests. [AlexV]

  Fixing catkin tests
- Fixing array test to use new msg_generate. [AlexV]
- Merge branch 'nested_implement' of https://github.com/asmodehn/pyros-
  msgs into fixing_catkin_tests. [AlexV]
- Merge pull request #8 from yotabits/nested_implement. [AlexV]

  Nested implement
- Fixing import_msgsrv to handle namespace packages properly. recovered
  accidently lost comment for namespace package in __init__. [AlexV]
- Fixing setup.py usage of generator. [AlexV]
- Fixing generator tests. [AlexV]
- Refactored how we do generation to privilege the common usecase. now
  generating message into a temporary directory. fixed all tests for
  basic pytest. [AlexV]
- Fixing a bunch of tests for catkin. WIP before rosmsg_generator
  refactor. [AlexV]
- Fixing pyros_msgs.msg path in nested test. [AlexV]
- WIP. attempting to generate all messages at once so that starting
  tests in same or different interpreter doesnt matter anymore. [alexv]
- Fixing hardcoded path of generator for test. [alexv]
- Added test for int64 in opt_as_nested. [Thomas]
- Added test for int32 in opt_as_nested. [Thomas]
- Added test for int16 in opt_as_nested. [Thomas]
- Small fix on test_opt_int8 in opt_as_nested. [Thomas]
- Added test for int8 in opt_as_nested. [Thomas]
- Added test for uint64 in opt_as_array. [Thomas]
- Added test for uint32 in opt_as_array. [Thomas]
- Added test for uint16 in opt_as_array. [Thomas]
- Added test for uint8 in opt_as_array. [Thomas]
- Added test for int16 and int 32. [Thomas]

  Added test for int16 and int32 for opt_as_array
- Merge pull request #1 from asmodehn/nested_implement. [yotabits]

  Nested implement
- Adding importer tests into tox. [alexv]
- Fixing path for package message adding test for using rosmsg_generator
  module directly fixing tests. [alexv]
- Tox fixes... [AlexV]
- Improving code to make it more ROS independent. [AlexV]
- Improved message generation and tests. [AlexV]
- Moving ros_genmsg_py and improving API. [alexv]
- Fixed all tests but still a problem remain : reloading package of
  newly generated module... [AlexV]
- Fixing all tests for opt_as_array with runtime message generation.
  [AlexV]
- Fix to handle rosmsg_py dependency path search during generation.
  [AlexV]
- Adapted set_opt_bool to dynamically generate and import message class
  for tests. [AlexV]
- Some fixes still WIP. [AlexV]
- Making test work for jade. But we still depend on pure ROS package
  pyros_utils. [AlexV]
- Adding pyros-setup as dependency, plus a few comments. [AlexV]
- Found a method usable by tox to generate ros messages. needs
  refining... [AlexV]
- Adding setup.py custom command to generate message modules. [AlexV]
- Fixing test assert that could break on set repr with different order.
  [AlexV]
- Modifying travis script to run pytest directly on install directory.
  [AlexV]
- Adding python-pytest dependency. [AlexV]
- Fixing travis checks. [AlexV]
- More common -> typecheck renaming. [AlexV]
- Fixing setup.py with proper name. [AlexV]
- Renamed subpackage common to typecheck. fixed tests. [AlexV]
- Adding tests and dependency on hypothesis. [AlexV]
- Adding dependency on hypothesis. now patching messages inside
  opt_as_array package. [AlexV]
- Finalizing optional fields as nested implementation. [AlexV]
- Fixing basic common tests to work with xenial version of hypothesis.
  [AlexV]
- Fixing imports for test runs. other small fixes. [AlexV]
- Refining tests. [AlexV]
- Reorganized tests. [AlexV]
- Merge pull request #5 from asmodehn/hypothesis. [AlexV]

  Hypothesis
- Adding catkin_pip as dependency. [AlexV]
- Small improvements. all array tests running... [AlexV]
- Fixing array tests. [AlexV]
- Now seems to work fine with catkin_pip. [AlexV]
- Fixing opt_as_array tests. [AlexV]
- Now able to generate type checker from rosmsg type. [AlexV]
- Improved type checker tests. [AlexV]
- More typechecker hypothesis tests. [AlexV]
- Improved typechecker, not relying on ROS types for it anymore. [AlexV]
- Experimenting with hypothesis for proper testing. [AlexV]
- Opt_as_nested seems to work fine now. more tests required... [AlexV]
- All opt_as_array tests passing. [AlexV]
- Better type checking by introducing typeschemas. [AlexV]
- Start of refactor to allow multiple implementations for optional
  fields... added lots of doctests. [AlexV]
- Adding travis badge. [alexv]
- Updating Readme to reflect opt_as_nested as WIP. [alexv]
- Now travis uses shadow-fixed repository. [alexv]
- Adding pyros_utils as dependency. [alexv]
- Adding python-six as system dependency. [alexv]
- Merge pull request #1 from asmodehn/http. [AlexV]

  optional fields implemented as array
- Merge branch 'http' of https://github.com/asmodehn/pyros-msgs into
  http. [alexv]
- Merge branch 'master' into http. [AlexV]
- Added readme for dropping repo. [AlexV]
- Cleaning up wrong init file. [alexv]
- Adding README. [alexv]
- Adding _opt_slots field to the punched message type. other changes to
  get all httpbin tests to pass. [alexv]
- Slightly different way to initializa when doing opt_as_array. [alexv]
- Attempting travis fix. comments. [alexv]
- Resurrecting optional message fields, since it is necessary to make
  explicit the intent of having an optional field in a message. [alexv]
- WIP. commit before changing internal dict representation of optional
  messages. [alexv]
- Extending path if needed to get ros generated messages. useful when
  running from here (nose has his own import behavior). [alexv]
- Adding http status code message. [alexv]
- Base optional message types and test template. [alexv]
- Cleanup bad __init__ file. added ignore for *.pyc and build/ [alexv]
- Small refactoring. fixed all tests. [alexv]
- Adding dependency on marshmallow. [alexv]
- Adding roslint as build depend. [alexv]
- Standard message types implemented with doc test. added travis files.
  [alexv]
- Started implementing standard ROS message -> dict serialization.
  [alexv]
- Initial commit. [AlexV]


