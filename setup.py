#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
import sys
from os.path import exists
from collections import OrderedDict
from setuptools import find_packages
from contextlib import contextmanager


@contextmanager
def silence_stdout():
    old_target = sys.stdout
    try:
        with open(os.devnull, 'w') as new_target:
            sys.stdout = new_target
            yield new_target
    finally:
        sys.stdout = old_target


def native_mb_python_tag(plat_impl=None, version_info=None):
    """
    Example:
        >>> print(native_mb_python_tag())
        >>> print(native_mb_python_tag('PyPy', (2, 7)))
        >>> print(native_mb_python_tag('CPython', (3, 8)))
    """
    if plat_impl is None:
        import platform

        plat_impl = platform.python_implementation()

    if version_info is None:
        import sys

        version_info = sys.version_info

    major, minor = version_info[0:2]
    ver = '{}{}'.format(major, minor)

    if plat_impl == 'CPython':
        # TODO: get if cp27m or cp27mu
        impl = 'cp'
        if ver == '27':
            IS_27_BUILT_WITH_UNICODE = True  # how to determine this?
            if IS_27_BUILT_WITH_UNICODE:
                abi = 'mu'
            else:
                abi = 'm'
        else:
            if ver == '38':
                # no abi in 38?
                abi = ''
            else:
                abi = 'm'
        mb_tag = '{impl}{ver}-{impl}{ver}{abi}'.format(**locals())
    elif plat_impl == 'PyPy':
        abi = ''
        impl = 'pypy'
        ver = '{}{}'.format(major, minor)
        mb_tag = '{impl}-{ver}'.format(**locals())
    else:
        raise NotImplementedError(plat_impl)
    return mb_tag


def parse_long_description(fpath='README.rst'):
    """
    Reads README text, but doesn't break if README does not exist.
    """
    if exists(fpath):
        with open(fpath, 'r') as file:
            return file.read()
    return ''


def parse_requirements(fname='requirements.txt', with_version=False):
    """
    Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file
        with_version (bool, default=False): if true include version specs

    Returns:
        List[str]: list of requirements items

    CommandLine:
        python -c "import setup; print(setup.parse_requirements())"
        python -c "import setup; print(chr(10).join(setup.parse_requirements(with_version=True)))"
    """
    from os.path import exists
    import re

    require_fpath = fname

    def parse_line(line):
        """
        Parse information from a line in a requirements text file
        """
        if line.startswith('-r '):
            # Allow specifying requirements in other files
            target = line.split(' ')[1]
            for info in parse_require_file(target):
                yield info
        else:
            info = {'line': line}
            if line.startswith('-e '):
                info['package'] = line.split('#egg=')[1]
            else:
                # Remove versioning from the package
                pat = '(' + '|'.join(['>=', '==', '>']) + ')'
                parts = re.split(pat, line, maxsplit=1)
                parts = [p.strip() for p in parts]

                info['package'] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    if ';' in rest:
                        # Handle platform specific dependencies
                        # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies
                        version, platform_deps = map(str.strip, rest.split(';'))
                        info['platform_deps'] = platform_deps
                    else:
                        version = rest  # NOQA
                    info['version'] = (op, version)
            yield info

    def parse_require_file(fpath):
        with open(fpath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    for info in parse_line(line):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info['package']]
                if with_version and 'version' in info:
                    parts.extend(info['version'])
                if not sys.version.startswith('3.4'):
                    # apparently package_deps are broken in 3.4
                    platform_deps = info.get('platform_deps')
                    if platform_deps is not None:
                        parts.append(';' + platform_deps)
                item = ''.join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


try:

    class EmptyListWithLength(list):
        def __len__(self):
            return 1

        def __repr__(self):
            return 'EmptyListWithLength()'

        def __str__(self):
            return 'EmptyListWithLength()'

except Exception:
    raise RuntimeError('FAILED TO ADD BUILD CONSTRUCTS')


NAME = 'wbia-pyhesaff'


MB_PYTHON_TAG = native_mb_python_tag()  # NOQA

ORIGINAL_AUTHORS = ['Krystian Mikolajczyk', 'Michal Perdoch']
EXTENDED_AUTHORS = ['Jon Crall', 'Avi Weinstock']
CURRENT_AUTHORS = ['WildMe Developers']

AUTHORS = ', '.join(ORIGINAL_AUTHORS + EXTENDED_AUTHORS + CURRENT_AUTHORS)
AUTHOR_EMAIL = 'dev@wildme.org'
URL = 'https://github.com/WildbookOrg/hesaff'
LICENSE = 'APL 2.0'
DESCRIPTION = 'PyHesaff - Python wrapper for Hessian Affine'


KWARGS = OrderedDict(
    name=NAME,
    author=AUTHORS,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=parse_long_description('README.rst'),
    long_description_content_type='text/x-rst',
    url=URL,
    license=LICENSE,
    install_requires=parse_requirements('requirements/runtime.txt'),
    extras_require={
        'all': parse_requirements('requirements.txt'),
        'tests': parse_requirements('requirements/tests.txt'),
        'build': parse_requirements('requirements/build.txt'),
        'runtime': parse_requirements('requirements/runtime.txt'),
    },
    # --- VERSION ---
    # The following settings retreive the version from git.
    # See https://github.com/pypa/setuptools_scm/ for more information
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'write_to': 'pyhesaff/_version.py',
        'write_to_template': '__version__ = "{version}"',
        'tag_regex': '^(?P<prefix>v)?(?P<version>[^\\+]+)(?P<suffix>.*)?$',
        'local_scheme': 'dirty-tag',
    },
    # --- PACKAGES ---
    # The combination of packages and package_dir is how scikit-build will
    # know that the cmake installed files belong in the pyhesaff module and
    # not the data directory.
    packages=find_packages(),
    package_dir={
        'pyhesaff': 'pyhesaff',
        # Note: this requires that HESAFF_LIB_INSTALL_DIR is set to pyhesaff/lib
        # in the src/cpp/CMakeLists.txt
        'pyhesaff.lib': 'pyhesaff/lib',
    },
    include_package_data=False,
    # List of classifiers available at:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 6 - Mature',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
    cmake_args=['-DBUILD_TESTS=OFF', '-DBUILD_DOC=OFF'],
    ext_modules=EmptyListWithLength(),  # hack for including ctypes bins
)

if __name__ == '__main__':
    """
    python -c "import pyhesaff; print(pyhesaff.__file__)"
    """
    with silence_stdout():
        import skbuild

    skbuild.setup(**KWARGS)
