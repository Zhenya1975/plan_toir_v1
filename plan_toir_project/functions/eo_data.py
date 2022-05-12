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
  full_eo_list_actual["operation_start_date"] = pd.to_datetime(full_eo_list_actual["operation_start_date"])
  full_eo_list_actual["operation_finish_date"] = pd.to_datetime(full_eo_list_actual["operation_finish_date"])
  full_eo_list_actual = full_eo_list_actual.astype({'strategy_id': int, 'avearage_day_operation_hours': float})

  # оставляем строки, у которых eo_model_id - это число
  eo_list  = full_eo_list_actual.loc[~full_eo_list_actual["eo_model_id"].isin(['no_data', 'Консервация', 'Списание'])]
  eo_list = eo_list.loc[~full_eo_list_actual["level_1_description"].isin(['Сухой Лог'])]

  # отбираем колонки
  eo_list = eo_list.loc[:, ['level_1_description', 'eo_class_code', 'eo_class_description','constr_type', 'eo_model_id', 'eo_model_name', 'eo_description', 'teh_mesto', 'level_upper', 'sap_operation_status', 'operation_start_date', 'operation_finish_date']]

  eo_list['level_1_description'] = eo_list['level_1_description'].astype("category")

  eo_ierarhy_list = []
  level_1_be = list(eo_list['level_1_description'].cat.categories)

  
  eo_list.to_csv('temp_files/eo_list.csv')
  
get_eo_data()