from setuptools import setup, find_packages
import pathlib

# Get the long description from the file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='youtrack-datagen',
    version='0.1',
    description='YouTrack Test Data Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/avitalique/youtrack-test-data',
    author='Vitali Asheichyk',
    author_email='avitalique@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'ytdatagen=ytdatagen.main:entry',
        ],
    },
)
