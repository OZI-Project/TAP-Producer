# OZI 0.4 meson.build:test_files,test_children
# Part of TAP-Producer.
# See LICENSE.txt in the project root for details.
# DO NOT EDIT BY HAND - This file was generated for use with OZI tools.
# ozi-fix -> meson rewrite is the standard editing pipeline.
test_files = ['test_tap.py']
foreach file: test_files
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'tap_producer' / 'tests')
    endif
endforeach
test_children = []
foreach child: test_children
    subdir(child)
endforeach