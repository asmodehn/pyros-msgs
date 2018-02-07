##############################################################################
# CMake
##############################################################################

cmake_minimum_required(VERSION 2.8.3)
project(pyros_msgs)

##############################################################################
# Find Packages
##############################################################################

find_package(catkin REQUIRED COMPONENTS
    catkin_pip
    std_msgs
    message_generation
    message_runtime
)


#####
# MESSAGES
#####

add_message_files(
  DIRECTORY
    msg
  FILES
    OptionalFields.msg
)

generate_messages(DEPENDENCIES std_msgs)



##############################################################################
# Catkin
##############################################################################

catkin_pip_package(pyros_msgs)

#########
# Tests
#######

if (CATKIN_ENABLE_TESTING)
  catkin_add_pytests(tests/test_pyros_msgs/typecheck)
  catkin_add_pytests(tests/test_pyros_msgs/opt_as_array)
  catkin_add_pytests(tests/test_pyros_msgs/opt_as_nested)
endif()


