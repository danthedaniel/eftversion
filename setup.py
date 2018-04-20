from setuptools import setup

setup(
    name='eftversion',
    packages=['eftversion'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
    ]
)
