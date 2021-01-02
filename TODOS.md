# TODOS

## For 0.5 release

- [x] fillna
- [?] replace (no regex)
    - [x] basic tests
    - [ ] consider changing replace/replacex signature to: 'col1,col2,col3:pattern//replace'
- [?] just-text
- [ ] import as type -- force mixed num/str columns to drop str values or convert to a value
    - [ ] `--import-as "col1:text,col2:int,col3:date"`
- [ ] proper comma-delimited parsing
    - write a simple parser in Lark: https://lark-parser.readthedocs.io/en/latest/json_tutorial.html
        - `--replacex 'col1,col2:pattern//replacement'`
        - SortbyParser
            - [x] defined and basic test
            - [ ] make part of Click Type/formatter
- [x] add autocompletion
    - seems to be built-in by default...? https://click.palletsprojects.com/en/7.x/bashcomplete/
-  change `--` to `-`, like `find` syntax
    - [x] making double-dash optional



## Future 

- [ ] change query to filter
- [ ] update: query + eval
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.update.html
    ```py
    import pandas as pd
    df = pd.DataFrame([['a', 1], ['b', 2], ['c', 3], ['d', 4]], columns=['name', 'val'])
    sf = df.query('val > 2').replace()
    sf[['name']] = sf['name'] + ' is big'
    ```

- CFrame should keep state


- studying `groupby` and aggregates
    - https://realpython.com/pandas-groupby/
    - https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#group-by-split-apply-combine
- eval/assign for simple calculations: https://jakevdp.github.io/PythonDataScienceHandbook/03.12-performance-eval-and-query.html

- calculation-type methods
    
    - `--round 'col1,col2:1,col3:0:just_ints'`
        - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.round.html?highlight=round#pandas.DataFrame.round
        - support `--round *:decimalplaces[int]` (e.g. round all columns to decimalplaces)

- each WrangleOption should itself figure out what Operation to use, e.g. kill op.build_operation
- consider making input_file require `-i/--input`, and allowing WrangleOption to accept varadic nargs: https://stackoverflow.com/a/48394004/160863
    - or: consider making every option 1 arg
        - `--replacex '`a|b|c` `REPL` `cols`'`
- figure out more pandas functionality to add
    - https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
    - [x] head/tail
    - [?] round 
    - [?] calculation ops that add new column


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
- [a...] unit tests

## cli stuff

- import stuff
    - [] let user specify data types




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


- [x] fixed cli.main to handle options with more than 1 arg
- [x] OpThing is now a custom but functionally empty ParamType subclass
    - [x] and that's why it's now been removed in favor of WrangleOption
- WrangleOption
    - [x] automatically sets `multiple=True`
    - currently treats everything as string type
        - [x] WrangleCommand.extract_wrangle_ops now respects Option.type
- WrangleCommand
    - [x] figure out how to use OptionParser.parse_args to preserve option order

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

- [x] --verbose: output the name/expr of each op, and the effect on the dataset, to stderr
- [x] make Click.Option subclass for operation specific flags
- [x] kill --zeta: replace `--zeta [foo] [expr]` option with proper `--query` `--sort` etc

