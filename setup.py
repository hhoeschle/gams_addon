from distutils.core import setup

setup(
    name='gams_addon',
    version='17.05',
    packages=['gams_addon'],
    url='https://github.com/hhoeschle/gams_addon',
    license='',
    author='Hanspeter Höschle',
    author_email='hanspeter.hoeschle@',
    description='python package to read out GAMS gdx files into pandas dataframes',
    install_requires=[
        'pandas >= 0.19',
        'unicodecsv >= 0.14',
        'gams'
    ]
)
