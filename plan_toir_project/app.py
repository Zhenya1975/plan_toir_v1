from dash import Dash, dcc, html, Input, Output, State, dash_table
from flask import flash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import base64
import io
import pandas as pd
import tab_main

# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
# template_theme1 = "sketchy"
template_theme1 = "flatly"
template_theme2 = "darkly"
# url_theme1 = dbc.themes.SKETCHY
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY



loading_style = {
    # 'position': 'absolute',
                 # 'align-self': 'center'
                 }

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
    "sandstone"
]

load_figure_template(templates)


dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)
app = Dash(__name__, external_stylesheets=[url_theme1, dbc_css])


app.layout = dbc.Container(
    dbc.Row(        [
            dbc.Col(
                [
                    html.H4("Overhaul estimator"),
                    ThemeSwitchAIO(
                      aio_id="theme", themes=[url_theme1, url_theme2],
                    ),

                    html.Div([
                     
                      dcc.Tabs(
                            id="tabs-all",
                            style={
                                # 'width': '50%',
                                # 'font-size': '200%',
                                'height':'10vh'
                            },
                            value='tab_main',
                            # parent_className='custom-tabs',
                            # className='custom-tabs-container',
                            children=[
                                tab_main.main_tab(),
                                # coverage_tab.coverage_tab(),
                                # messages_orders_tab.messages_orders_tab(),
                                # orders_moved_tab.orders_moved_tab(),
                                # settings_tab.settings_tab()

                                # tab2(),
                                # tab3(),
                            ]
                        ),
                    ]),

                ]
            )
        ]
    ),
    className="m-4 dbc",
    fluid=True,
)



############### ПАРСЕР ЗАГРУЖАЕМОГО ФАЙЛА ########################
def parse_contents(contents, filename):
  content_type, content_string = contents.split(',')
  decoded = base64.b64decode(content_string)

  try:
    if 'xlsx' in filename and "interval_between_overhaul" in filename:
      # Assume that the user uploaded an excel file
      df = pd.read_excel(io.BytesIO(decoded))
      # проверяем, что в файле есть нужные колонки 
      list_of_columns_in_uploaded_df = df.columns.tolist()
      check_column_list = ['component_class_id',	'component_class_descr', 'interval_between_overhaul'
        ]
      control_value = 1
      for column in check_column_list:
        if column in list_of_columns_in_uploaded_df:
          continue
        else:
          control_value = 0
          break
      if control_value == 1:
        df.to_csv('plan_toir_project/data_files/interval_between_overhaul_data.csv', index = False)
      else:
        print("не удалось сохранить файл interval_between_overhaul_data.csv")
       
          
  except Exception as e:
    print(e)
    return html.Div([
        'There was an error processing this file.'
    ])

  return html.Div([
      html.H5(filename),
      dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            filter_action='native',
            style_header={
                # 'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_cell={'textAlign': 'left'},

        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              )
def update_output_(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        
        return children

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=False)

