# OZI 0.4 meson.build:root_files,root_children
# Part of TAP-Producer.
# See LICENSE.txt in the project root for details.
# DO NOT EDIT BY HAND - This file was generated for use with OZI tools.
# ozi-fix -> meson rewrite is the standard editing pipeline.
project(
    'TAP-Producer',
    default_options: ['warning_level=3'],
    license: 'Apache-2.0 WITH LLVM-exception',
    license_files: ['LICENSE.txt'],
    meson_version: '>=1.1.0',
    version: run_command(
        'python3',
        [
            '-c',
            'from setuptools_scm import get_version;print(get_version(normalize=False))',
        ],
        check: true,
    ).stdout().strip(),
)
fs = import('fs')
pymod = import('python')
python_dependencies = get_option('python-dependencies')
python = pymod.find_installation()
project_name = meson.project_name()
pip_compile = find_program('pip-compile', required: true)
root_files = [
    'README',
    'CHANGELOG.md',
    'LICENSE.txt',
    'requirements.in',
    'requirements.in',
    'pyproject.toml',
    '.gitignore',
]
custom_target(
    'requirements-TAP-Producer',
    input: root_files[3],
    output: 'requirements.txt',
    build_always_stale: true,
    build_by_default: true,
    command: [
        'pip-compile',
        '--allow-unsafe',
        '--strip-extras',
        '-q',
        '--generate-hashes',
        '-o',
        '@OUTPUT@',
        '@INPUT@'
    ]
)
pyproject_config = configuration_data()
pyproject_config.set(
    'PYTHON_VERSION_DIST',
    'py'+''.join(python.language_version().split('.'))
)
pyproject_config.set('SCM_VERSION', meson.project_version())
pyproject_config.set('VCS_TAG', '@VCS_TAG@')
pyproject_config.set('PROJECT_NAME', project_name)
pyproject_config.set('README_TEXT', fs.read('README'))
pyproject_config.set('REQUIREMENTS_IN', 
    run_command(
        python, ['-c', '''import os;import pathlib
requirements = (
    r.partition('\u0023')[0]
    for r in filter(
        lambda r: not (r.startswith('\u0023') or r == '\n'),
        pathlib.Path('./requirements.in').read_text('utf-8').splitlines(),
    )
)
for req in requirements:
    if len(req) > 0:
        print(f'Requires-Dist: {req}')
'''], check: true
    ).stdout().strip()
)
pyproject_config.set('LICENSE', meson.project_license()[0])
configure_file(
    input: 'pyproject.toml',
    output: 'pyproject.toml',
    configuration: pyproject_config
)
vcs_tag(input: 'pyproject.toml', output: 'pyproject.orig.toml')

foreach source : root_files
    if source not in ['pyproject.toml', 'requirements.in', '.gitignore', 'README', 'CHANGELOG.md']
        fs.copyfile(source)
    elif source == 'README'
        fs.copyfile(source, 'README.rst')
    endif
endforeach
root_children = ['tap_producer', 'tests']
foreach child: root_children
    subdir(child)
endforeach
if false
    executable('root_files', root_files)
    executable('source_files', source_files)
    executable('ext_files', ext_files)
    executable('test_files', test_files)
    executable('root_children', root_children)
    executable('source_children', source_children)
    executable('test_children', test_children)
endif
if not meson.is_subproject()
    dev = subproject('ozi')
    foreach var : get_option('variables')
        name = var.replace('-', '_')
        set_variable(name, dev.get_variable(name))
    endforeach
    meson.add_dist_script(dev.get_variable('pip'), 'install', 'tomli>=2.0.0')
    meson.add_dist_script(python, '-c', dev.get_variable('meson_dist_setuptools_scm'))
endif