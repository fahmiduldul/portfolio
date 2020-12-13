import pandas as pd
import plotly.graph_objs as go

def get_dataframe():
  '''
  OUTPUT:
  new_df - cleaned dataframe for visualization
  '''
  
  df = pd.read_csv('./dataset/data.csv')

  df = df.drop(columns=['Country Name', 'Country Code', 'Indicator Code'], axis=1)

  desired_row_list = [
    "Mortality rate, infant, male (per 1,000 live births)",
    "GDP (constant 2010 US$)",
    "Manufacturing, value added (constant LCU)",
    "CO2 emissions (kt)",
    r"Electricity production from oil, gas and coal sources (% of total)",
    r"Electricity production from hydroelectric sources (% of total)",
    r"Electricity production from renewable sources, excluding hydroelectric (% of total)"
  ]

  drop_first_and_last_row = [True] * df.shape[1]
  drop_first_and_last_row[0] = False
  drop_first_and_last_row[-1] = False

  desired_df_list = []
  for row_name in desired_row_list:
    temp_df = df[df['Indicator Name'] == row_name].transpose()
    temp_df = temp_df[drop_first_and_last_row]
    desired_df_list.append(temp_df)

  new_df = pd.concat(desired_df_list, axis=1)
  new_df['year'] = new_df.index

  columns_name_map = {
    11:"Mortality rate",
    259:"GDP",
    51:"Manufacturing",
    501:"CO2",
    130:"Fossil",
    345:"Renewable",
    915:"Hydroelectric"
  }

  new_df = new_df.rename(columns=columns_name_map)
  return new_df

def get_figures():
  '''
  OUTPUT:
  [plotly JSON] - list of JSON Plotly for frontend
  '''

  df = get_dataframe()

  # graph 1, line chart GPS & Manufacturing vs Year
  graph_one = []
  y_val_df = df[["GDP", "Manufacturing"]]
  x_val = df['year'].tolist()

  #plot data into the figure
  graph_one.append(
    go.Scatter(
      x = x_val,
      y = y_val_df["GDP"].tolist(),
      mode = 'lines+markers',
      name = "GDP"
    )
  )
  graph_one.append(
    go.Scatter(
      x = x_val,
      y = y_val_df["Manufacturing"].tolist(),
      mode = 'lines+markers',
      name = "Manufacturing",
      yaxis = 'y2'
    )
  )

  #figure configuration
  layout_one = dict(
    title = 'GDP & Manufacturing Added Value over Years',
    xaxis = dict(title='Year'),
    yaxis = dict(title='GDP USD)'),
    yaxis2 = dict(title='Manufacturing Added Value (USD)', overlaying='y', side='right')
  )

  # figure 2, scatterplot child mortality rate vs GDP
  graph_two = []
  x_val = df['GDP'].tolist()
  y_val = df['Mortality rate'].tolist()

  graph_two.append(
    go.Scatter(
      x = x_val,
      y = y_val,
      mode = 'markers'
    )
  )

  layout_two = dict(
    title='GDP vs Mortality Rate',
    xaxis = dict(title='GDP (USD)'),
    yaxis = dict(title='Child Mortality Rate per 1000')
  )

  # graph 3, line chart GDP & CO2 Emmisions vs Year
  graph_three = []
  y_val_df = df[["GDP", "CO2"]]
  x_val = df['year'].tolist()

  #plot data into the figure
  graph_three.append(
    go.Scatter(
      x = x_val,
      y = y_val_df["GDP"].tolist(),
      mode = 'lines+markers',
      name = "GDP"
    )
  )
  graph_three.append(
    go.Scatter(
      x = x_val,
      y = y_val_df["CO2"].tolist(),
      mode = 'lines+markers',
      name = "CO2",
      yaxis = 'y2'
    )
  )

  #figure configuration
  layout_three = dict(
    title = 'GDP & CO2 Emmisions over Years',
    xaxis = dict(title='Year'),
    yaxis = dict(title='GDP (USD)'),
    yaxis2 = dict(title='CO2 Emmisions (kt)', overlaying='y', side='right')
  )

  # graph 4, line chart of electricity production
  graph_four = []
  desired_col_name = ["Renewable", "Fossil", "Hydroelectric"]
  y_val_df = df[desired_col_name]
  x_val = df['year'].tolist()

  #plot data into the figure
  for col_name in desired_col_name:
    graph_four.append(
      go.Scatter(
        x = x_val,
        y = y_val_df[col_name].tolist(),
        mode = 'lines+markers',
        name = col_name
      )
    )

  #figure configuration
  layout_four = dict(
    title = r'% of Electricity Production',
    xaxis = dict(title='Year'),
    yaxis = dict(title=r'% of Electricity Production'),
  )

  return [
    dict(data=graph_one, layout=layout_one),
    dict(data=graph_two, layout=layout_two),
    dict(data=graph_three, layout=layout_three),
    dict(data=graph_four, layout=layout_four)
  ]
