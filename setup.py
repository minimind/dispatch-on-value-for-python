from distutils.core import setup

setup(
    name='dispatchonvalue',
    version='0.9.2',
    author='Ian Macinnes',
    author_email='ian.macinnes@gmail.com',
    packages=['dispatchonvalue', 'dispatchonvalue.test'],
    url='https://github.com/minimind/dispatch-on-value-for-python',
    license='MIT',
    description='Python package providing dispatch on values for ' +
                'arbitrarily nested lists and dictionary data structures.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2 :: Only'
    ],
    keywords=['dispatch on value', 'multiple dispatch', 'dynamic dispatch'],
    include_package_data=True
)
