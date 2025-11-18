"""Setup script for bulkmailer"""
from setuptools import setup, find_packages

setup(
    name='bulkmailer',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client>=2.100.0',
        'google-auth-httplib2>=0.1.1',
        'google-auth-oauthlib>=1.1.0',
        'pandas>=2.1.0',
        'openpyxl>=3.1.0',
        'click>=8.1.0',
    ],
    entry_points={
        'console_scripts': [
            'bulkmailer=bulkmailer.cli:cli',
        ],
    },
    author='Your Name',
    description='Local Gmail Bulk Mailer CLI',
    python_requires='>=3.13',
)
