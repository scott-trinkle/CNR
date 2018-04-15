from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='cnrgui',
      version='0.1',
      description='',
      long_description=readme(),
      url='https://github.com/scott-trinkle/CNR',
      author='Scott Trinkle',
      author_email='tscott.trinkle@gmail.com',
      license='MIT',
      packages=['cnrgui'],
      install_requires=['numpy', 'matplotlib'],
      zip_safe=False)
