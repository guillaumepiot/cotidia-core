from setuptools import find_packages, setup

setup(
    name="cotidia-core",
    description="Core utils for Cotidia Admin.",
    version="1.0",
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://code.cotidia.com/cotidia/core/",
    packages=find_packages(),
    package_dir={'core': 'core'},
    package_data={},
    namespace_packages=['cotidia'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
