import yadisk
import os
import pandas as pd
import zipfile

y = yadisk.YaDisk(token="AQAAAABfSJVEAAfMGMams7U1xkJGgxmm7sinToc")

def check_ya_token():
  try:
    print(y.check_token()) # Проверим токен
  except:
    print("не удалось подрубиться к ядиску")
# check_ya_token()

def get_file(file_name):
  try:
    y.download(file_name, "temp_files/df.csv")
    print("файл ", file_name, " скачан в temp_files")
  except Exception as e:
    print("не получилось get_file", e)

# get_file("maintanance_jobs_df.csv")
get_file("full_eo_list_actual.csv")

def delete_file(file_path):
  try:
    os.remove(file_path)
    print("Файл ", file_path, " удален")
  except Exception as e:
    print("Не удалось удалить файл", e)


def upload_file(file_path, file_name):
  try:
    y.upload(file_path, file_name, overwrite = True)
    print("Файл ", file_name, " успешно выгружен")
  except Exception as e:
    print('не получилось upload_file ', file_name, " Ошибка: ", e)


# upload_file('temp_files/full_eo_list_actual.csv', 'full_eo_list_actual.csv')