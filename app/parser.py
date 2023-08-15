import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
from config import url
import os


def get_data():
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()  # Проверка на успешный HTTP-статус

        bs = BeautifulSoup(response.text, "lxml")
        temp = bs.find('pre')
        json_string = temp.text
        json_data = json.loads(json_string)

        return json_data

    except requests.exceptions.Timeout:
        raise TimeoutError('Превышено время ожидания при запросе к серверу')

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Ошибка при запросе: {e}')


def check_data():
    try:
        json_data = get_data()

        if os.path.exists('downloads/open.json'):
            with open('downloads/open.json', 'r', encoding='utf-8') as file:
                read_json = json.load(file)
        else:
            read_json = []

        my_list = []
        for data_1, data_2 in zip(read_json, json_data):
            if data_1 != data_2:
                my_list.append(data_2)

        with open('downloads/open.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False)

        if my_list:
            df = pd.DataFrame(my_list, columns=['CRM', 'TASKNAME', 'CITY', 'ASSIGNEE_NAME', 'KS_3', 'KS_23'])
            file_name = f'new_{datetime.now().strftime("%d%m%Y_%H%M%S")}.xlsx'
            file_path = f'downloads/{file_name}'
            df.to_excel(file_path, index=False)

            return file_path

    except Exception as e:
        raise Exception(f"Err: {e}")


def convert_data(message):
    try:
        json_data = get_data()
        my_list = []

        if message == 'all':
            columns = ['CRM', 'TASKNAME', 'CITY', 'ASSIGNEE_NAME', 'KS_3', 'KS_23']

        elif message == 'unexecuted':
            for data in json_data:
                if data['ASSIGNEE_NAME'] is None:
                    my_list.append(data)
            columns = ['CRM', 'TASKNAME', 'CITY', 'KS_3', 'KS_23']

        else:
            raise ValueError("Invalid message type")

        df = pd.DataFrame(my_list if my_list else json_data, columns=columns)
        file_name = f'{message}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.xlsx'
        file_path = f'downloads/{file_name}'
        df.to_excel(file_path, index=False)

        return file_path

    except Exception as e:
        raise Exception(f"Err: {e}")
