import pandas as pd
import numpy as np


  

def create_component_overhaul_schedule():
  interval_between_overhaul_data_df = pd.read_csv('plan_toir_project/data_files/interval_between_overhaul_data.csv')

  # пробуем понять какие данные мы получили
  # Пусть целевые колонки, по которым мы можем понять что именно мы получили  будут в списке 
  explore_data_column_list = ['eo_class_code']
  # итерируемся по interval_between_overhaul_data и изучаем что к нам приехало.
  interval_between_overhaul_data_df['interval_between_overhaul'] = interval_between_overhaul_data_df['interval_between_overhaul'].replace(np.nan, 0) 
  for row in interval_between_overhaul_data_df.itertuples():
    # получаем значение межсервисного интервала. 
    interval_between_overhaul = getattr(row, "interval_between_overhaul")
    try:
      interval_between_overhaul = interval_between_overhaul*1
      if interval_between_overhaul <=0:
        print("нет данных в поле межремонтного интервала или ноль")
        continue
        
    except Exception as e:
      print("нет значения в поле interval_between_overhaul в строке ", getattr(row, 'Index')+1, e)
      continue
    
    print(interval_between_overhaul)      
  # получаем файл eo_list
  eo_data = pd.read_csv('plan_toir_project/data_files/eo_list.csv')
  
create_component_overhaul_schedule()