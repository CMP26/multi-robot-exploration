# Install script for directory: /media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/src/multi_limo

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/build/multi_limo/catkin_generated/installspace/multi_limo.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_limo/cmake" TYPE FILE FILES
    "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/build/multi_limo/catkin_generated/installspace/multi_limoConfig.cmake"
    "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/build/multi_limo/catkin_generated/installspace/multi_limoConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_limo" TYPE FILE FILES "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/src/multi_limo/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/multi_limo" TYPE PROGRAM FILES "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/build/multi_limo/catkin_generated/installspace/visual_search_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_limo" TYPE DIRECTORY FILES
    "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/src/multi_limo/launch"
    "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/src/multi_limo/worlds"
    "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/src/multi_limo/config"
    "/media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/limo_ws/src/multi_limo/rviz"
    )
endif()

