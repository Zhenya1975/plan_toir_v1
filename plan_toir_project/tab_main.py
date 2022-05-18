from dash import dcc, html
import dash_bootstrap_components as dbc
# import datetime
# import json
# Opening JSON file
loading_style = {
    # 'position': 'absolute',
    # 'align-self': 'center'
                 }


def main_tab():
    main_tab_block = dcc.Tab(
        label='Data converter',
        value='tab_main',
        children=[
            dbc.Row([
                dbc.Col(
                    children=[
                    
                      dcc.Loading(id='loading_settings_1', parent_style=loading_style),
                      # html.Div([
                      #       html.P(),          
                 
                      #       dbc.Button("Выгрузить eo_list.xlsx", id="btn_download_eo_list", size="sm",
                      #                  style={'marginBottom': '3px',
                      #                         'marginTop': '3px',
                      #                         'backgroundColor': '#232632'}, ),
                      #       dcc.Download(id="download_eo_list")
                      #   ]
                      #         ),


                        html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Перетащи или ',
                                    html.A('выбери файл')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),

                            html.Hr(),                  
                            html.Div(id='output-data-upload'),
                          # html.Div(id='output-data-2'),
                          # html.Div(id='output-data-3'),
                          # html.P(id='output-data-4'),
                        ]),
                      html.P("interval_between_overhaul в имени файла для загрузки межремонтного интервала компонентов"),


                    ])
                ])

        ])
    return main_tab_block