from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))


about = {}
with open(os.path.join(here, 'async_unshortenit', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    include_package_data=True,
    zip_safe=True,
    setup_requires=['pytest-runner<=3.0.1'],
    tests_require=['pytest'],
    install_requires=[
        'aiohttp>=3.8.1',
        'click>=8.1.3',
        'lxml>=4.9.1'
    ],
    license=about['__license__'],
    keywords='unshortener adf.ly lnx.lu sh.st shortener',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)