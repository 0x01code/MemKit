from setuptools import setup, find_packages

setup(
    name='memkit',
    version='1.1.1',
    packages=find_packages(),
    install_requires=[
        'memprocfs',
        'keystone-engine'
    ],
    description='Memkit is game hacking library for Direct Memory Access (DMA) ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/0x01code/memkit',
    author='0x01code',
    author_email='admin@0x01code.com',
    license='MIT',
)
