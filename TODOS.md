# TODOS

> ### Current status
>
> - need to figure out how the F to make a custom param that builds a common list of tuples
> - figure out more pandas functionality to add

### References/things to read
- https://medium.com/towards-artificial-intelligence/how-i-wrangle-data-at-the-command-line-17ad48faf699
- https://github.com/rufuspollock/command-line-data-wrangling

----------------------------------------------------------------------------------
----------------------------------------------------------------------------------

## ots: sed
- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
- use replace.regex
- [x] basic: `--sed to_replace//new_value`
- [ ] by column: `--sed to_replace//new_val//colnames`
- maybe call it "replace"?
- remove dumb `//` hack delimiter

## CFrame

- [x] cli uses CFrame class to import data
- [x] cli uses CFrame.process_pipe to iterate through ops and yield meta and data
- [ ] DRY up `inplace` setting
- [ ] unit tests

## cli stuff

- import stuff
    - [ ] let user specify data types


## --verbose

- output the name/expr of each op, and the effect on the dataset, to stderr


## --zeta option

- replace `--zeta [foo] [expr]` option with proper `--query` `--sort` etc


## supported ops

- 

### groupby
- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
- groupby without transformation/agg is meaningless: https://stackoverflow.com/questions/12315810/output-pandas-grouped-dataframe-without-aggregation

### complete transformations, e.g. pivot, joins
- should be a post 1.0 feature
- should likely have its own "Op" class

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

### unlikely to do

- rename(cols)
- grep: select rows by regex pattern 
    - filter(regex='REGEX', axis=0) 
    - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html
    - this will require some manual work...




