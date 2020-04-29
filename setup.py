from setuptools import setup, find_packages

#with open('README.md', 'r') as f:
#    long_desc='\n'.join(f.readlines())
long_desc="fdsfds"

setup(name='metsvg',
    version='0.1',
    author='Joshua Patterson',
    author_email='joshua.d.patterson@gmail.com',
    description='A tool I want',
    long_description=long_desc,
    python_requires='>=3.6',
    packages=find_packages(),
    #entry_points={
    #  'console_scripts' : [
    #      'beerme=beerbot.main:main',
    #  ]
    #},
    #include_package_data=True
)

