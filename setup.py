from setuptools import setup

setup(
    name = 'dpla',
    packages = ['dpla'], # this must be the same as the name above
    version = '0.4',
    description = 'A python client for the DPLA API',
    author = 'Chad Nelson',
    author_email = 'chadbnelson@gmail.com',
    url = 'https://github.com/bibliotechy/DPyLA',   # use the URL to the github repo
    download_url = 'https://github.com/bibliotechy/DPyLA/archive/0.4.tar.gz',
    keywords = ['libraries', 'DPLA', 'museums'], # arbitrary keywords
    test_suite='tests',
    classifiers = [],
    install_requires = [ 'requests' ]
    )
