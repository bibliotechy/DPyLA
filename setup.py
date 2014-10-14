from distutils.core import setup

setup(
    name = 'dpla',
    packages = ['dpla'], # this must be the same as the name above
    version = '0.1.3',
    description = 'A python client for the DPLA API',
    author = 'Chad Nelson',
    author_email = 'chadbnelson@gmail.com',
    url = 'https://github.com/bibliotechy/DPyLA',   # use the URL to the github repo
    download_url = 'https://github.com/bibliotechy/DPyLA/tarball/0.1.3', # I'll explain this in a second
    keywords = ['libraries', 'DPLA', 'museums'], # arbitrary keywords
    classifiers = [],
    install_requires = [ 'requests' ]
    )
