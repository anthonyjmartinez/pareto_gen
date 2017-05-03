import pandas as pd
import numpy as np
from bokeh.plotting import figure 
from bokeh.layouts import gridplot
from bokeh.models import FuncTickFormatter, LinearAxis
from bokeh.models.ranges import Range1d

def pareto_gen(df,
               field,
               bins=4,
               labels=None,
               include_lowest=False,
               width=600,
               height=600,
               tools='pan,box_zoom,wheel_zoom,reset,save',
               title=None,
               x_axis_label=None,
               y_axis_label=None,
               **kwargs):
    """Return a Bokeh Pareto Chart object
    
    Arguments:
    data - must be a Pandas DataFrame    
    field - explicitly define the field to analyze (str)
    
    Keyword Arguments:
    
    bins - must satisfy requirements of pandas.cut, default 4
    labels - must satisfy requirements of pandas.cut, default None
    include_lowest - bool, default is False, passed on to pandas.cut
    width - chart width in pixels, default 600
    height - chart height in pixels, default 600
    tools - figure tools, default 'pan,box_zoom,wheel_zoom,reset,save'
    title - figure title
    x_axis_label - figure x-axis label
    y_axis_label - figure y-axis label
    
    Example Usage for a DataFrame object 'merged' with a field 'sessions'
    user-defined bins, and labels:
    
    bins = [0, 30, 60, 90, 180, 270, merged.sessions.max()]
    labels = ['0-1', '2', '3', '4', '5', '5+']

    plot = pareto_gen(merged,
                      'sessions',
                      bins=bins,
                      labels=labels,
                      include_lowest=True,
                      title='My Title',
                      x_axis_label='My X-Axis',
                      y_axis_label='My Y-Axis')
    
    #Display the plots
    from bokeh.plotting import output_notebook, show
    output_notebook()
    show(plot)"""
    
    df['categories'] = pd.cut(df[field],
                              bins=bins,
                              labels=labels,
                              include_lowest=include_lowest)
    
    a = df.groupby('categories')[field].count().sort_values(ascending=False)
    b = 100 * (a.cumsum()/a.sum())
    
    data = pd.DataFrame({'{}'.format(field) : a, 'pct' : b})
    x = np.arange(len(data))
    label_dict = {i : data.index[i] for i in x}
    
    #Create the plots
    plot = figure(plot_width=width,
                  plot_height=height,
                  tools=tools,
                  x_axis_label=x_axis_label,
                  y_axis_label=y_axis_label,
                  title=title)

    plot.extra_y_ranges = {'pct' : Range1d(start=0, end=100)}
    plot.add_layout(LinearAxis(y_range_name='pct',
                               axis_label='Percent'),
                    'left')

    plot.vbar(x=x,
              top=data[field],
              width=1,
              line_color='red',
              fill_color='red',
              alpha=0.5)

    plot.line(x,
              data.pct,
              line_color='blue',
              y_range_name='pct')

    #Reformat the x-axis
    plot.xaxis.formatter = FuncTickFormatter(code="""
                                            var labels = {};
                                            return labels[tick];
                                            """.format(label_dict))
                                             
    return plot
