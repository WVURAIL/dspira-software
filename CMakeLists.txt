cmake_minimum_required(VERSION 3.16)
project(dspira-software VERSION 1.0 LANGUAGES CXX)

find_package(Gnuradio "3.10" REQUIRED COMPONENTS runtime)
include(GrPython)

set(DSPIRA_BLOCKS
    chart_recorder comparator correlate csv_filesink hdf5_sink integration
    png_print_spectrum power_spectrum running_norm_std systemp_calibration
    triggered_save_csv vector_moving_average)
set(DSPIRA_PYTHON python/gnuradio/dspira/__init__.py)
foreach(block IN LISTS DSPIRA_BLOCKS)
    list(APPEND DSPIRA_PYTHON python/gnuradio/dspira/${block}.py)
    set(installed_block ${block})
    if(block STREQUAL "power_spectrum")
        set(installed_block powerSpectrum)
    endif()
    install(FILES grc/radio_astro_${block}.block.yml
            DESTINATION share/gnuradio/grc/blocks
            RENAME radio_astro_${installed_block}.block.yml)
endforeach()
GR_PYTHON_INSTALL(FILES ${DSPIRA_PYTHON}
                  DESTINATION ${GR_PYTHON_DIR}/gnuradio/dspira)

enable_testing()
add_test(NAME dspira_blocks
         COMMAND ${PYTHON_EXECUTABLE} -m unittest discover -s ${CMAKE_CURRENT_SOURCE_DIR}/tests/blocks -p "test_*.py")
add_test(NAME original_block_checks
         COMMAND ${PYTHON_EXECUTABLE} -m unittest discover -s ${CMAKE_CURRENT_SOURCE_DIR}/tests/blocks -p "qa_*.py")
set_tests_properties(dspira_blocks original_block_checks PROPERTIES
    ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/python;PYTHONNOUSERSITE=1;MPLBACKEND=Agg")
