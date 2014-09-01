from distutils.core import setup

setup(
    name='dispatchonvalue',
    version='0.1.0',
    author='Ian Macinnes',
    author_email='ian.macinnes@gmail.com',
    packages=['dispatchonvalue', 'dispatchonvalue.test'],
    url='http://pypi.python.org/pypi/dispatchonvalue/',
    license='LICENSE.txt',
    description='Python package providing dispatch on values for ' +
                'arbitrarily nested lists and dictionary data structures.',
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
