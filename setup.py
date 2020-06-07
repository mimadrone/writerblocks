import os.path

from setuptools import setup, find_packages


# Cribbed from https://pythonhosted.org/an_example_pypi_project/setuptools.html
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="writerblocks", version='0.1',
      packages=find_packages(exclude=['writerblocks/test']),
      install_requires=['pypandoc', 'PyYAML'], entry_points={
        'console_scripts': ['writerblocks-cli=writerblocks.cli:main']},
      author='M. I. Madrone',
      author_email='mimadrone@gmx.com',
      url='https://github.com/mimadrone/writerblocks',
      description='A toolkit for writing stories in a modular way.',
      license="GPLv3",
      keywords="writing",
      long_description=read('README.md'),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Topic :: Text Processing'
      ]
      )
