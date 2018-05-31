from setuptools import setup, find_packages


# Parse the version from the mapbox module.
with open('mapboxcli/__init__.py') as f:
    for line in f:
        if "__version__" in line:
            version = line.split("=")[1].strip().strip('"').strip("'")
            continue

setup(name='mapboxcli',
      version=version,
      description="Command line interface to Mapbox Web Services",
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: Implementation :: PyPy'],
      keywords='',
      author="Sean Gillies",
      author_email='sean@mapbox.com',
      url='https://github.com/mapbox/mapbox-cli-py',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'click-plugins',
          'cligj>=0.4',
          'mapbox==0.14.0',
          'six'],
      extras_require={
          'test': ['coveralls', 'pytest>=2.8', 'pytest-cov', 'responses',
                   'mock']},
      entry_points="""
      [console_scripts]
      mapbox=mapboxcli.scripts.cli:main_group
      """)
