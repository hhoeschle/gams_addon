# gams_addon
python package to read out GAMS gdx files into pandas dataframes

## Installation
Copy folder into source directory or add to python path

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
23/10/2015 First version put online

## Credits
Thanks to Arne for providing extensive test cases during development of first version.