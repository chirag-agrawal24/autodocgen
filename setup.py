from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='autodocgen',
    version='0.1.0',
    description='AI-powered Python code documentation generator',
    author='Chirag Agrawal',
    author_email='2411chirag@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        'console_scripts': [
            'autodocgen=autodocgen.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.10',
)
