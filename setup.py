from setuptools import setup, find_packages

setup(
    name='r3c0nX',
    version='0.2',
    author='D2Cy',
    description='Reconnaissance Tool',

    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'r3c0nX = r3c0nX.main:main'
        ]
    },
    package_data={
        'mypackage.config': ['*.ini'],
    }


)


        
