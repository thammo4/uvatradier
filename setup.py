from setuptools import find_packages, setup

with open('README.md', encoding='utf-8') as fh:
	long_description = fh.read()

setup(
	name='lumiwealth_tradier',
	version='0.1.0',
	author='Robert Grzesik',
	description='wahoowah',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Lumiwealth/lumiwealth_tradier',
	packages=find_packages(),
	project_urls={'Bug Tracker': 'https://github.com/Lumiwealth/lumiwealth_tradier/issues'},
	keywords='tradier finance api',
)
