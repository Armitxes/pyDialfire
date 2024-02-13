import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyDialfire',
    version='0.1.1',
    author='Armitxes',
    author_email='support@armitxes.net',
    description='Access Dialfire API via python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://armitxes.net/Project/pyDialfire',
    project_urls={
        'Bug Tracker': 'https://github.com/Armitxes/pyDATEV/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir={'dialfire': 'src/dialfire'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
)
