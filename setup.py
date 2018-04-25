import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import x10_any


if len(sys.argv) <= 1:
    print("""
Suggested setup.py parameters:

    * build
    * install
    * sdist  --formats=zip
    * sdist  # NOTE requires tar/gzip commands

""")

readme_filename = 'README.rst'
if os.path.exists(readme_filename):
    f = open(readme_filename)
    long_description = f.read()
    f.close()
else:
    long_description = None

setup(
    name='x10_any',
    version=x10_any.__version__,
    author=x10_any.__author__,
    url='https://github.com/clach04/x10_any',
    description='Issue x10 commands via CM17A Firecracker or Mochad (CM15A RF/PL and CM19A RF)',
    long_description=long_description,
    packages=['x10_any'],
    #data_files=[('.', [readme_filename])],  # does not work :-( ALso tried setup.cfg [metadata]\ndescription-file = README.md # Maybe try include_package_data = True and a MANIFEST.in?
    classifiers=[  # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation',
        ],
    platforms='any',  # or distutils.util.get_platform()
    install_requires=['pyserial'],
)
