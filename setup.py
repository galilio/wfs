from setuptools import setup, find_packages

setup(name = 'bayes-wfs',
    version = '0.1',
    description = 'tools to serve wfs',
    author = 'XiaoYuming',
    author_email = 'xiaoyuming@bayesba.com',
    packages = find_packages(),
    install_requires = [],
    include_package_data = True,
    namespace_packages = ['bayes'])