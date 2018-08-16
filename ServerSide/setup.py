from setuptools import setup
# Flask configure file 
# Used for installation of the required packages
setup(
	name='server',
	packages=['server'],
	include_package_data=True,
	install_requires=[
		'flask',
		# 'psycopg2',
	],
)