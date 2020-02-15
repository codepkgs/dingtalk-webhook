
from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='dingtalk-webhook',
    version='1.1.5',
    keywords='dingtalk, dingding, dingtalk-webhook, ding, alert',
    description='send dingtalk message to dingding webhook robot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='zhanghe',
    author_email='x_hezhang@126.com',
    url='https://github.com/x-hezhang/dingtalk-webhook',
    license='GNU GPLv3',
    packages=find_packages()
)
