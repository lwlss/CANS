from setuptools import setup

def readme():
    with open('README.rst', 'r') as f:
        return f.read()

setup(name='cans',
      version='0.1',
      description='Analysis of QFA with competition and signalling modelling',
      long_description=readme(),
      url='https://github.com/lwlss/CANS.git',
      author='Conor Lawless, Daniel Boocock',
      author_email='daniel.boocock@protonmail.ch',
      license='',
      packages=["cans"],
      scripts=[],
      install_requires=[],
      test_suite="tests",
      tests_require=['pytest'],
      zip_safe=False)
