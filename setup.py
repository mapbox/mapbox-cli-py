from setuptools import setup, find_packages


# Parse the version from the mapbox module.
with open('mbx/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

setup(name='mbx',
      version=version,
      description="Command line interface to Mapbox Web Services",
      classifiers=[],
      keywords='',
      author="Sean Gillies",
      author_email='sean@mapbox.com',
      url='https://github.com/mapbox/mbx-cli',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'click-plugins',
          'cligj',
          'mapbox',
      ],
      extras_require={
          'test': ['coveralls', 'pytest', 'pytest-cov', 'responses'],
      },
      entry_points="""
      [console_scripts]
      mbx=mbx.scripts.cli:main_group

      [mbx.mbx_commands]
      geocoding=mbx.scripts.geocoding:geocoding
      """
      )
