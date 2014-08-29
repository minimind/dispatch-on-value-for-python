from distutils.core import setup

setup(
    name='pymultidispatchonvalue',
    version='0.1.0',
    author='Ian Macinnes',
    author_email='ianma@bitzoo.co.uk',
    packages=['pymultidispatchonvalue', 'pymultidispatchonvalue.test'],
    url='http://pypi.python.org/pypi/pymultidispatchonvalue/',
    license='LICENSE.txt',
    description='A Python package providing multiple dispatch on values for ' +
                'nested lists and dictionary data structures.',
    long_description=open('README.txt').read(),
    install_requires=[
    ],
)
