# gams_addon
python package to read out GAMS gdx files into pandas dataframes

## Installation

* Open command window/terminal
* change to location of folder containing the `setup.py` file
`cd c:\YOUR PATH\gams_addon`
* Install package to your local python installation
`pip install -e .` This will also check if all required packages are installed.


## Usage
```python
import gams_addon as ga

gdx_file = 'tests/test_database.gdx' # path to gdx-file 

data_frame_s = ga.gdx_to_df(gdx_file, symbol='S')
print data_frame_s 
```

## Contributing
The testing needs to be extended. 

If you encounter problem, send me your gdx or adapt the python code.

## History
* 23/10/2015 First version put online
* 03/05/2017 Added a setup file
* 29/06/2017 Refactoring of gdx_to_df

## Credits
* Thanks to Arne for providing extensive test cases during development of first version.
* Thanks to Kris for providing extensive test cases during development of second version.