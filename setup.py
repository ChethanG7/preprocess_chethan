import setuptools

with open('README.md','r') as file:
	long_description = file.read()


setuptools.setup(
	name= 'preprocess_chethan', #this should be unique
	version ='0.0.1',
	author ='Chethan G',
	#author_email = 'info',
	description = 'This is preprocessing package',
	Long_description = long_description,
	Long_description_content_type = 'text/markdown',
	packages = setuptools.find_packages(),
	classifiers = [
	'Programming Language :: Pyhton ::3',
	'License :: OSI Approved :: MIT License',
	"Operating System :: OS Indepenedent"],
	python_requires = '>=3.5'
	)
