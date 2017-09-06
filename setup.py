from setuptools import setup

setup(
    name='pycomics',
    packages=['pycomics'],
    package_dir={'': 'src'},
    version='0.1',
    description='A random description',
    author='Jim Chang',
    author_email='cwebb.tw@gmail.com',
    url='https://github.com/id/pkg',
    download_url='',
    keywords=['comic', 'pycomics'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'pycomics=pycomics.main:main',
        ],
    },
    install_requires=[
        "requests",
    ],
    extras_require={
        ":sys_platform=='darwin'": [
            'pync',
        ],

    }
)
