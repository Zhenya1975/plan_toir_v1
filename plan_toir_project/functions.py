import pandas as pd
import numpy as np


  

def create_component_overhaul_schedule():
  interval_between_overhaul_data_df = pd.read_csv('plan_toir_project/data_files/interval_between_overhaul_data.csv')
  
  interval_between_overhaul_data_df['interval_between_overhaul'] = interval_between_overhaul_data_df['interval_between_overhaul'].replace(np.nan, 0)
  interval_between_overhaul_data_df['eo_main_class_id'] = interval_between_overhaul_data_df['eo_main_class_id'].replace(np.nan, 0)
  interval_between_overhaul_data_df['head_eo_model_id'] = interval_between_overhaul_data_df['head_eo_model_id'].replace(np.nan, 0)
  interval_between_overhaul_data_df['be_code'] = interval_between_overhaul_data_df['be_code'].replace(np.nan, 0)
  
  
  # interval_between_overhaul_data_df.to_csv('plan_toir_project/temp_files/interval_between_overhaul_data_df.csv')
  # получаем файл eo_list
  eo_data = pd.read_csv('plan_toir_project/data_files/eo_list.csv')
  
  for row in interval_between_overhaul_data_df.itertuples():
    # получаем значение межсервисного интервала. 
    interval_between_overhaul = getattr(row, "interval_between_overhaul")
    try:
      interval_between_overhaul = interval_between_overhaul*1
      # Если значение межсервисного интервала в строке ни о чем, то идем дальше по циклу
      if interval_between_overhaul <=0:
        print("нет данных в поле межремонтного интервала или ноль")
        continue
            
    except Exception as e:
      print("нет значения в поле interval_between_overhaul в строке ", getattr(row, 'Index')+1, e)
      continue
      
    print("кол-во записей в исходной таблице: ", len(eo_data))
    component_class_id = getattr(row, "component_class_id")
    # сначала фильтруем все записи по component_class_id
    eo_data_filtered = eo_data.loc[eo_data['component_class_id']==component_class_id]
    print("кол-во записей с component_class_id: ", len(eo_data_filtered))

    be_code = getattr(row, "be_code")
    # если be_code ненулевой, то сужаем выборку
    if be_code!=0:
      eo_data_filtered = eo_data_filtered.loc[eo_data_filtered['be_code']==be_code]
    
    # Определяем по какой колонке будем фильтровать таблицу
    # если есть нижестоящий класс, то фильтруем по нему и другие вышестоящие классы игнорируем

    head_eo_model_id = getattr(row, "head_eo_model_id")
    filter_column_name = ""
    filtering_value = 0
    if head_eo_model_id !=0:
      filter_column_name = "head_eo_model_id"
      filtering_value = head_eo_model_id
    else:
      eo_main_class_id = getattr(row, "eo_main_class_id")
      if eo_main_class_id != 0:
        filter_column_name = "eo_main_class_id"
        filtering_value = eo_main_class_id
      # если везде нули то записываем ранее полученное значение eo_data_filtered и уходим на следующую итериацию цикла
      else:
        eo_data_filtered_indexes = eo_data_filtered.index.values
        print('длина списка индексов: ', len(eo_data_filtered_indexes))
        eo_data.loc[eo_data_filtered_indexes, ['interval_between_overhaul']] = interval_between_overhaul
        continue
    print("filter_column_name: ", filter_column_name)
    print("filtering_value: ", filtering_value)
    # фильтруем по определенному имени колонки
    eo_data_filtered = eo_data_filtered.loc[eo_data_filtered[filter_column_name]==filtering_value]    
    
    eo_data_filtered_indexes = eo_data_filtered.index.values
    print('длина списка индексов: ', len(eo_data_filtered_indexes))
    eo_data.loc[eo_data_filtered_indexes, ['interval_between_overhaul']] = interval_between_overhaul
    

  eo_data.to_csv('plan_toir_project/data_files/eo_list_update.csv', index = False, decimal = ',')  
    

# create_component_overhaul_schedule()

def assign_overhaul_cost():
  overhaul_cost_data_df = pd.read_csv('plan_toir_project/data_files/overhaul_cost_data.csv')
  overhaul_cost_data_df['overhaul_cost_usd'] = overhaul_cost_data_df['overhaul_cost_usd'].replace(np.nan, 0)
  overhaul_cost_data_df['be_code'] = overhaul_cost_data_df['be_code'].replace(np.nan, 0)
  overhaul_cost_data_df['component_class_id'] = overhaul_cost_data_df['component_class_id'].replace(np.nan, 0)
  overhaul_cost_data_df['head_eo_model_id'] = overhaul_cost_data_df['head_eo_model_id'].replace(np.nan, 0)

  eo_data = pd.read_csv('plan_toir_project/data_files/eo_list.csv')

  for row in overhaul_cost_data_df.itertuples():
    # получаем значение стоимости. 
    overhaul_cost_usd = getattr(row, "overhaul_cost_usd")
    try:
      overhaul_cost_usd = overhaul_cost_usd*1
      # Если значение межсервисного интервала в строке ни о чем, то идем дальше по циклу
      if overhaul_cost_usd <=0:
        print("нет данных в поле стоимости или ноль")
        continue
            
    except Exception as e:
      print("нет значения в поле стоимости в строке ", getattr(row, 'Index')+1, e)
      continue

    component_class_id = getattr(row, "component_class_id")
    eo_data_filtered = eo_data.loc[eo_data['component_class_id']==component_class_id]
    be_code = getattr(row, "be_code")
    # если be_code ненулевой, то сужаем выборку
    if be_code!=0:
      eo_data_filtered = eo_data_filtered.loc[eo_data_filtered['be_code']==be_code]
    print("кол-во записей с component_class_id: ", len(eo_data_filtered))
    
    head_eo_model_id = getattr(row, "head_eo_model_id")
    filter_column_name = ""
    filtering_value = 0
    if head_eo_model_id !=0:
      filter_column_name = "head_eo_model_id"
      filtering_value = head_eo_model_id
    else:
      eo_main_class_id = getattr(row, "eo_main_class_id")
      if eo_main_class_id != 0:
        filter_column_name = "eo_main_class_id"
        filtering_value = eo_main_class_id
      # если везде нули то записываем ранее полученное значение eo_data_filtered и уходим на следующую итериацию цикла
      else:
        eo_data_filtered_indexes = eo_data_filtered.index.values
        print('длина списка индексов: ', len(eo_data_filtered_indexes))
        eo_data.loc[eo_data_filtered_indexes, ['overhaul_cost_usd']] = overhaul_cost_usd
        continue

     # фильтруем по определенному имени колонки
    eo_data_filtered = eo_data_filtered.loc[eo_data_filtered[filter_column_name]==filtering_value]    
    eo_data_filtered_indexes = eo_data_filtered.index.values
    print('длина списка индексов: ', len(eo_data_filtered_indexes))
    eo_data.loc[eo_data_filtered_indexes, ['overhaul_cost_usd']] = overhaul_cost_usd
    
  eo_data.to_csv('plan_toir_project/data_files/eo_list_update.csv', index = False, decimal = ',')  

  
assign_overhaul_cost()