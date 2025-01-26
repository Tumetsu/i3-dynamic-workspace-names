from setuptools import setup

setup(name='i3-dynamic-workspace-names',
      version='0.2',
      description='Set i3 workspace names dynamically based on windows in the workspace',
      author='Tuomas Salmi',
      license='MIT',
      packages=['i3_dynamic_workspace_names'],
      install_requires=[
          'i3ipc>=2.2.1',
          'python-xlib',
          'six',
      ],
      scripts=['bin/i3-dynamic-workspace-names'])
