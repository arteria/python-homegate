from distutils.core import setup

from homegate import __version__

setup(
    name='homegate',
    version=__version__,
    packages=['homegate', ],
    license='BSD',
    long_description=open('README.md').read(),
    author='arteria GmbH',
    author_email='admin@arteria.ch',
)
