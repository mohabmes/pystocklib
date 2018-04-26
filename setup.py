from setuptools import setup

setup(
	name='pystocklib',
	version=1.0,
	description='Python package for Stock Market analysis. (Historical Data, News analysis, visual, Empirical Mode Decomposition)',
	author="mohabmes",
	author_email='mohab.elsheikh@gmail.com',
	url='https://github.com/mohabmes/pystocklib',
	packages=['pystocklib', 'pystocklib.emd_lib', 'pystocklib.yahoo_historical'],
	include_package_data=True,
	install_requires=['pandas', 'scipy', 'textblob', 'numpy', 'matplotlib', 'bs4', 'tld'],
	license='MIT',
	zip_safe=False
)
