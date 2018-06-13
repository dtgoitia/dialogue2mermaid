from setuptools import find_packages, setup

setup(
    name='dialogue2mermaid',
    version='0.0.1',
    description='',  # TODO
    long_description=open('README.rst').read(),
    author='David Torralba Goitia',
    author_email='david.torralba.goitia@gmail.com',
    packages=find_packages(exclude=['tests']),
    license='MIT',
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    install_requires=[],    # TODO: Automate extraction from Pipfile?
    entry_points={
        "console_scripts": [
            'do=dialogue2mermaid.cli:main'
        ],
    }
)
