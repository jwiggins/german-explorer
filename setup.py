from setuptools import setup, find_packages

setup(name='germanexplore',
      version='0.0.1',
      author='John Wiggins',
      author_email='john.wiggins@xfel.eu',
      description='A program for exploring German.',
      long_description='',
      packages=find_packages(),
      package_data={'germanexplore': ['de-en-abridged.txt']},
      entry_points={
          'console_scripts': [
              'build-db = germanexplore.build_db:main',
              'germanexplore = germanexplore.explore:main',
          ],
      },
      )
