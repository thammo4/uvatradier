from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read();

setup(
	name='uvatradier',
	version='0.2.8',
	author='tom hammons',
	description='wahoowa',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/thammo4/uvatradier',
	packages=find_packages(),
	project_urls={'Bug Tracker':'https://github.com/thammo4/uvatradier/issues'},
	keywords='tradier finance api',
	install_requires=['requests>=2.0', 'pandas>=1.0']
);
