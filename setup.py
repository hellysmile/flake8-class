import io
import os
from setuptools import setup

__dir__ = os.path.dirname(__file__)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


LONG_DESCRIPTION = read(os.path.join(__dir__, 'README.rst'))

about = {}
with open(os.path.join(__dir__, 'flake8_class', '__about__.py')) as file:
    exec(file.read(), about)


setup(
    name='flake8-class',
    author='hellysmile',
    author_email='hellysmile@gmail.com',
    version=about['__version__'],
    install_requires=[
        'flake8',
    ],
    url='http://github.com/hellysmile/flake8-class',
    long_description=LONG_DESCRIPTION,
    description='Flake8 lint for class declaration.',
    packages=['flake8_class'],
    test_suite='test',
    include_package_data=True,
    entry_points={
        'flake8.extension': [
            'flake8_class = flake8_class:ClassChecker',
        ],
    },
    license='MIT',
    zip_safe=True,
    keywords='flake8 lint class',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ]
)
