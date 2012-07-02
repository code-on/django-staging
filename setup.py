from distutils.core import setup

setup(
    name='django-staging',
    version='0.1',
    packages=['staging', 'staging.management', 'staging.management.commands'],
    url='https://github.com/code-on/django-staging',
    license='BSD licence, see LICENCE',
    description='Project staging helpers',
    long_description=open('README.md').read()
)
