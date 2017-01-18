from setuptools import setup, find_packages


# Parse the version from the mapbox module.
with open('mapboxcli/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

setup(name='mapboxcli',
      version=version,
      description="Command line interface to Mapbox Web Services",
      classifiers=[],
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
          'mapbox>=0.11',
          'six'],
      extras_require={
          'test': ['coveralls', 'pytest>=2.8', 'pytest-cov', 'responses'],
      },
      entry_points="""
      [console_scripts]
      mapbox=mapboxcli.scripts.cli:main_group

      [mapboxcli.mapboxcli_commands]
      config=mapboxcli.scripts.config:config
      geocoding=mapboxcli.scripts.geocoding:geocoding
      directions=mapboxcli.scripts.directions:directions
      distance=mapboxcli.scripts.distance:distance
      mapmatching=mapboxcli.scripts.mapmatching:match
      upload=mapboxcli.scripts.uploads:upload
      staticmap=mapboxcli.scripts.static:staticmap
      surface=mapboxcli.scripts.surface:surface
      dataset=mapboxcli.scripts.datasets:datasets
      """)
