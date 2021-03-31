from setuptools import setup, find_packages

#with open('README.md', 'r') as f:
#    long_desc='\n'.join(f.readlines())
long_desc="fdsfds"

install_requires = [
    'cairocffi==1.1.0',
    'CairoSVG==2.4.2',
    'cffi==1.14.0',
    'click==7.1.2',
    'cssselect==1.1.0',
    'cssselect2==0.3.0',
    'defusedxml==0.6.0',
    'Flask==1.1.2',
    'itsdangerous==1.1.0',
    'Jinja2==2.11.2',
    'lxml==4.6.3',
    'MarkupSafe==1.1.1',
    'Pillow==7.1.2',
    'pycparser==2.20',
    'pygal==2.4.0',
    'PyYAML==5.3.1',
    'tinycss==0.4',
    'tinycss2==1.0.2',
    'urllib3==1.25.9',
    'webencodings==0.5.1',
    'Werkzeug==1.0.1',
    'gunicorn==20.0.4',
    'ruamel.yaml==0.16.10',
]

setup(name='chartist',
    version='0.3',
    author='Joshua Patterson',
    author_email='joshua.d.patterson@gmail.com',
    description='A tool I want',
    long_description=long_desc,
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=install_requires,
)

