from setuptools import setup, find_packages

setup(name='piddle',
      version='1.0.15gn',
      include_package_data=True,
      # packages=find_packages()
      packages=['piddle','piddle/piddleGTK','piddle/piddleSVG','piddle/piddleTK2'],
      package_data = 
          {'piddle': ['truetypefonts/*', 'pilfonts/*'] }
      
)

