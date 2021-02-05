cmake_minimum_required(VERSION 3.4)
project(LLSTauTools)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")

# setup boost library
find_package( Boost REQUIRED program_options regex filesystem system)
INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIR} )

# setup boost library
find_package(ROOT)
include(${ROOT_USE_FILE})

include_directories(inc)
file(GLOB SOURCES "src/*.cc" "src/*.cpp")

# Building soft to analyse StauEfficiency
add_executable(LifeTimeTauEfficiency bin/LifeTimeTauEfficiency.cpp ${SOURCES})
target_link_libraries(LifeTimeTauEfficiency ${ROOT_LIBRARIES} ${Boost_LIBRARIES})
