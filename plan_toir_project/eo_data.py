import pandas as pd
import yad

# функция забирает мегасписок, фильтрует целевые строки, выбирает колонки и расставляет их
def get_eo_data():
  # скачиваем полный список
  yad.get_file("full_eo_list_actual.csv")
  # читаем его в датафрейм
  full_eo_list_actual = pd.read_csv('temp_files/df.csv', dtype=str, low_memory=False)
  # удаляем df из временных
  yad.delete_file("temp_files/df.csv")
  # print(full_eo_list_actual.info())
  full_eo_list_actual["operation_start_date"] = pd.to_datetime(full_eo_list_actual["operation_start_date"])
  full_eo_list_actual["operation_finish_date"] = pd.to_datetime(full_eo_list_actual["operation_finish_date"])
  full_eo_list_actual = full_eo_list_actual.astype({'strategy_id': int, 'avearage_day_operation_hours': float})
    
  # оставляем строки, у которых eo_model_id - это число
  eo_list  = full_eo_list_actual.loc[~full_eo_list_actual["eo_model_id"].isin(['no_data', 'Консервация', 'Списание'])]
  eo_list = eo_list.loc[~full_eo_list_actual["be_description"].isin(['Сухой Лог'])]
  
  head_tehmesto_df = eo_list.dropna(subset = ['teh_mesto'])
  
  head_tehmesto_list = list(set(head_tehmesto_df['teh_mesto']))

  # получаем узлы к техместам голов
  head_node_eo_list = full_eo_list_actual.loc[full_eo_list_actual['teh_mesto'].isin(head_tehmesto_list)]
  
  # отбираем колонки
  head_node_eo_list = head_node_eo_list.loc[:, ['be_description',	'be_code', 'eo_main_class_id',	'eo_main_class_descr','eo_class_code', 'eo_class_description','constr_type', 'eo_model_id', 'eo_model_name','head_eo_model_id','head_eo_model_descr','component_class_id','component_class_descr', 'eo_description', 'eo_code', 'teh_mesto', 'teh_mesto_description', 'level_upper', 'sap_operation_status', 'operation_start_date', 'operation_finish_date','strategy_id', 'head_type']]

  # убираем строки с пустыми строками в head_eo_model_id
  head_node_eo_list = head_node_eo_list.dropna(subset = ['head_eo_model_id'])
  print(len(head_node_eo_list))
  # сортируем 
  head_node_eo_list.sort_values(['teh_mesto', 'be_description', 'eo_class_code', 'head_eo_model_descr'], inplace=True)
  

  head_node_eo_list['be_description'] = head_node_eo_list['be_description'].astype("category")


  level_1_be = list(head_node_eo_list['be_description'].cat.categories)
  
  
  head_node_eo_list.to_csv('temp_files/eo_list.csv', index = False)
  
get_eo_data()


def update_eo_data():
  # скачиваем полный список
  yad.get_file("full_eo_list_actual.csv")
  # читаем его в датафрейм
  full_eo_list_actual = pd.read_csv('temp_files/df.csv', dtype=str, low_memory=False)
  # удаляем df из временных
  yad.delete_file("temp_files/df.csv")
  # print(full_eo_list_actual.info())
  full_eo_list_actual["operation_start_date"] = pd.to_datetime(full_eo_list_actual["operation_start_date"])
  full_eo_list_actual["operation_finish_date"] = pd.to_datetime(full_eo_list_actual["operation_finish_date"])
  full_eo_list_actual = full_eo_list_actual.astype({'eo_model_id':int, 'strategy_id': int, 'avearage_day_operation_hours': float})
  
  eo_list_df  = full_eo_list_actual.loc[~full_eo_list_actual["eo_model_id"].isin(['Консервация', 'Списание'])]

  eo_list_df = eo_list_df.loc[~eo_list_df["level_1_description"].isin(['Сухой Лог'])]
  
  eo_list_df = eo_list_df.dropna(subset = ['teh_mesto'])
  
  # в колонке eo_model_id меняем No_data на ноль
  eo_list_df.loc[eo_list_df['eo_model_id']=='no_data', ['eo_model_id']] = 0
  eo_list_df = eo_list_df.astype({'eo_model_id': int})
  
  eo_model_id_list = list(set(eo_list_df.loc[eo_list_df['eo_model_id'] != 0]['eo_model_id']))
  # отбираем строки, в которых есть eo_model_id
  eo_list_df_heads = eo_list_df.loc[eo_list_df['eo_model_id'].isin(eo_model_id_list)]
  # eo_list_df_heads.to_csv('temp_files/eo_list_df_heads.csv', index = False)

  tehmesto_list = list(set(eo_list_df_heads['teh_mesto']))
  # # print(len(tehmesto_list))
  tehmesto_list_len = len(tehmesto_list)
  eo_list_df_heads_data = pd.read_csv('temp_files/eo_list_df_heads.csv')
  eo_list_df_heads_data = eo_list_df_heads_data.astype({'eo_model_id':int})
  
  i=0
  for tehmesto in tehmesto_list:
    i = i+1
    # print("tehmesto ", i, " из ", tehmesto_list_len)
    eo_list_df_subset = eo_list_df.loc[eo_list_df['teh_mesto']==tehmesto]
    subset_indexes = eo_list_df_subset.index.values
    # print(list(eo_list_df_subset['eo_model_id']))
    subset_eo_model_id = max(list(eo_list_df_subset['eo_model_id']))
    eo_list_df.loc[subset_indexes, ['head_eo_model_id']] = subset_eo_model_id
    eo_list_df.loc[subset_indexes, ['head_eo_model_description']] = subset_eo_model_id
    

  eo_list_df2 = pd.merge(eo_list_df, eo_list_df_heads_data, left_on = 'head_eo_model_id', right_on='eo_model_id', how='left')
    
  # # yad.upload_file('temp_files/eo_list_df.csv', 'full_eo_list_actual.csv')  
  eo_list_df2.to_csv('temp_files/eo_list_df.csv', index = False)
  
# update_eo_data()  

