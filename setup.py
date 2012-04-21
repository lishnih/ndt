import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'docutils',
    'xlrd',
    ]

setup(name='ndt',
      version='0.1',
      description='ndt',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Pyramid",
        "Intended Audience :: Legal Industry",
        "License :: Repoze Public License",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Database :: Front-Ends",
        ],
      author='Stan',
      author_email='lishnih@gmail.com',
      url='http://pypi.python.org/pypi/ndt/',
      keywords='web wsgi bfg pylons pyramid ndt indexing',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='ndt',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = ndt:main
      """,
      )
