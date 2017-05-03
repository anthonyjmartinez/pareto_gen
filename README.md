# pareto_gen
## Pareto Chart Generator (Python / Pandas / Bokeh)
### Goals: 
- Accept a Pandas DataFrame
- Bin the contained data on a user specified field
  - Default to 4 bins, but allow user defined bins to be passed on to pd.cut
- Calculate the % occurance of each bin
- Create meaningful x-axis labels from the Categorical Index
  - Allow for explicit labels to be passed to pd.cut
- Return a Bokeh figure with the graphed data

### Depends:
*or developed on*
- pandas 0.19.2
- numpy 1.12.0
- bokeh 0.12.4
