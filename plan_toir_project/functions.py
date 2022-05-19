import pandas as pd
import numpy as np
from datetime import timedelta



# обработка данных с счетчиков наработки
def motohours_counter_procurement():
  motohours_counter_raw_data = pd.read_csv('plan_toir_project/temp_files/785С_motohours.csv', decimal=",")
  motohours_counter_raw_data['datetime_raw'] = motohours_counter_raw_data['Дата'] +"/"+ motohours_counter_raw_data['Момент измерений']
  motohours_counter_raw_data['datetime_raw'] = pd.to_datetime(motohours_counter_raw_data['datetime_raw'], format='%Y-%m-%d/%H:%M:%S')


  motohours_counter_raw_data = motohours_counter_raw_data.loc[motohours_counter_raw_data['ЕдиницаИзмерПризнака']=='МТЧ']
  motohours_counter_raw_data.drop_duplicates(subset=['Документ измерений'], inplace=True)
  # получаем список уникальных ЕО в выборке
  eo_list = list(set(motohours_counter_raw_data['Единица оборудования']))
  # итерируемся по списку ЕО
  result_data = []
  i=0
  for eo_code in eo_list:
    i=i+1
    print("eo: ", i, " из ", len(eo_list))
    motohours_counter_raw_data_subset = motohours_counter_raw_data.loc[motohours_counter_raw_data['Единица оборудования']==eo_code]
    # сортируем по datetime
    motohours_counter_raw_data_subset = motohours_counter_raw_data_subset.copy()
    motohours_counter_raw_data_subset.sort_values(['datetime_raw'], inplace=True, ascending=False)
    # получаем строку с минимальной датой. Это старт для этой выборки
    eo_motohour_eirliest_row = motohours_counter_raw_data_subset.iloc[motohours_counter_raw_data_subset["datetime_raw"].argmin()]
    # print(eo_motohour_eirliest_row)
    eo_subset_start_datetime = eo_motohour_eirliest_row['datetime_raw']
    eo_subset_start_counter = eo_motohour_eirliest_row['Показания счетчика']
    # print(eo_subset_start_datetime, eo_subset_start_counter)
    # итерируемся по записям. и считаем дельту в datetime и дельту наработки
    # print(motohours_counter_raw_data_subset.info())
    # переименовываем колонки 
    motohours_counter_raw_data_subset = motohours_counter_raw_data_subset.rename(columns={"Единица оборудования":"eo_code", "Показания счетчика":"counter_current"})
    for row in motohours_counter_raw_data_subset.itertuples():
      temp_dict = {}
      eo_code = getattr(row, "eo_code")
      date_time = getattr(row, "datetime_raw")
      counter_current = getattr(row, "counter_current")
      time_delta = (date_time - eo_subset_start_datetime).total_seconds()/(60*60)
      counter_delta = counter_current - eo_subset_start_counter
      motohour_coef = time_delta / counter_delta
      temp_dict['head_eo_model_id'] = 65
      temp_dict['Самосвалы CAT 785C'] = 'Самосвалы CAT 785C'
      temp_dict['eo_code'] = eo_code
      temp_dict['counter_current'] = counter_current
      temp_dict['motohour_coef'] = motohour_coef
      result_data.append(temp_dict)
  
  counter_data_df = pd.DataFrame(result_data)
  counter_data_df.to_csv('plan_toir_project/temp_files/counter_data.csv')

      
    
    
  # print(motohours_counter_raw_data.info())
  # print(motohours_counter_raw_data.head())
  head_eo_model_id = 65
  head_eo_model_descr = 'Самосвалы CAT 785C'
  
motohours_counter_procurement()  

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

  
# assign_overhaul_cost()