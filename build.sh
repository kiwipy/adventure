#!/bin/bash
#
# Manual build-script for gnome builder projects.
# Can also handle install and remove.
#
script_version="0.1.0"
build_deps=("meson" "ninja-build" "cmake" "glib-compile-resources")

if [[ "$1" == "--remove" ]]; then
    sudo ninja uninstall -C build/
else
    for dep in ${build_deps[@]}; do
        if which $dep > /dev/null; then
            echo "Found: $dep"
        else
            echo "Missing: $dep"
            exit 1
        fi
    done
    meson build
    cd build/
    meson test
    meson compile

    if [[ "$1" == "--install" ]]; then
        echo -e "\nEnter password to install"
        sudo ninja install
    fi
fi
