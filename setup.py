from setuptools import setup

short_description = 'A command-line python utility for applying watermarks to one or more photos'

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = short_description

setup(name='watermarker-cli',
      packages=['watermarker-cli'],
      version='0.0.1',
      description=short_description,
      long_description = long_description,
      author='Scott Vitale',
      author_email='svvitale@gmail.com',
      url='http://github.com/svvitale/watermarker-cli')
