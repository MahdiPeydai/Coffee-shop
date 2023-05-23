from setuptools import setup

setup(
    name='coffee shop',
    packages=['coffee-shop'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)