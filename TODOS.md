# TODOS

### Current status

- fixed cli.main to handle options with more than 1 arg
- [x] OpThing is now a custom but functionally empty ParamType subclass
    - [x] and that's why it's now been removed in favor of WrangleOption
- WrangleOption
    - [x] automatically sets `multiple=True`
    - [ ] currently treats everything as string type
- WrangleCommand
    - [ ] figure out how to use OptionParser.parse_args to preserve option order


- figure out more pandas functionality to add
    - [x] head/tail

### References/things to read
- https://medium.com/towards-artificial-intelligence/how-i-wrangle-data-at-the-command-line-17ad48faf699
- https://github.com/rufuspollock/command-line-data-wrangling

----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
## better options/zed bye bye

- [x] basic implementation of `extract_ops_from_raw_args()`
- rewrite CFrame to accept the extract_ops result

## ots: dropna
- [x] user cannot pass in empty string; instead, pass in '*' to signify "ALL columns"

## ots: sed
- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
- use replace.regex
- [x] basic: `--sed to_replace//new_value`
- [x] by column: `--sed to_replace//new_val//colnames`
- maybe call it "replacex"?
- remove dumb `//` hack delimiter

## CFrame

- [x] cli uses CFrame class to import data
- [x] cli uses CFrame.process_pipe to iterate through ops and yield meta and data
- [ ] DRY up `inplace` setting
- [ ] unit tests

## cli stuff

- import stuff
    - [ ] let user specify data types

- make Click.Option subclass for operation specific flags

## --verbose

- output the name/expr of each op, and the effect on the dataset, to stderr


## --zeta option
- replace `--zeta [foo] [expr]` option with proper `--query` `--sort` etc


## --info option
- print df.dtype / df.info



## supported ops


### groupby
- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
- groupby without transformation/agg is meaningless: https://stackoverflow.com/questions/12315810/output-pandas-grouped-dataframe-without-aggregation

### complete transformations, e.g. pivot, joins
- should be a post 1.0 feature
- should likely have its own "Op" class



### unlikely to do

- rename(cols)
- grep: select rows by regex pattern 
    - filter(regex='REGEX', axis=0) 
    - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html
    - this will require some manual work...



### done


- query: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html
- dropna: 
    - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html#pandas.DataFrame.dropna
    - param is `subset` of columns to match NA
    - [x] `--dropna ""`
    - [x] `--dropna "name,region"`


- sortby
    - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    - [x] `--sortby col1:asc,col2:desc`

- migrated `--zed` system to proper `--query,--dropna,--sortby` options
  - zed tests moved to ZUNK
    - [x] finish porting zed tests
  - [x] tests/ops/test_dropna.py is currently failing the most basic test
  - [x] **tests/test_cli:test_hello indicates that context isn't being shared as expected...**
    - because when running pytest, sys.argv will be: `['pytest', 'tests/test_cli.py', '-v']` 
    - [x] resolved: created custom WrangleCommand that has orgargs (will ask in Click github issues)
