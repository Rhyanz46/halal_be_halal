from setuptools import find_packages, setup

setup(
    name='app',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_cors',
        'flask_sqlalchemy',
        'pytest', 'mysql', 'click', 'pillow'
    ],
)

# pip install -e .
