cmake_minimum_required(VERSION 3.4)
project(LLSTauTools)

find_package(ROOT)
include(${ROOT_USE_FILE})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

include_directories(inc)
file(GLOB SOURCES "src/*.cc" "src/*.cpp")

# Building soft to analyse StauEfficiency
add_executable(STauefficiency bin/StauEfficiency.cpp ${SOURCES})
target_link_libraries(STauefficiency ${ROOT_LIBRARIES})
