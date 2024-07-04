# OZI 0.4 meson.build:source_files,source_children
# Part of TAP-Producer.
# See LICENSE.txt in the project root for details.
# DO NOT EDIT BY HAND - This file was generated for use with OZI tools.
# ozi-fix -> meson rewrite is the standard editing pipeline.
source_files = ['__init__.py', '__init__.pyi', 'py.typed']
foreach file: source_files
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'tap_producer')
    endif
endforeach
ext_files = []
foreach file: ext_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.extension_module(
            fs.replace_suffix(file, ''),
            file,
            install: true,
            subdir: 'tap_producer',
            dependencies: python.dependency()
        )
    endif
endforeach
source_children = []
foreach child: source_children
    subdir(child)
endforeach