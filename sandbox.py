#!/usr/bin/env python3
"""
just a scratchpad for quickly interactively testing things out

testing out top-level config
"""
from IPython import embed as IBREAKPOINT
import numpy as np
import pandas as pd
from vega_datasets import data as vdata

def main():
    df = pd.read_csv('examples/fruits.csv')
    print('Breakpoint time!')
    IBREAKPOINT()


if __name__ == '__main__':
    main()

