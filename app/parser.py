from requests_html import HTMLSession
import json
import pandas as pd
from datetime import datetime
from config import url
import os


def get_data():
    try:
        session = HTMLSession()
        response = session.get(url).json()

        return response

    except Exception as e:
        raise Exception(f"Err: {e}")


def check_data():
    try:
        json_data = get_data()

        if os.path.exists('downloads/open.json'):
            with open('downloads/open.json', 'r', encoding='utf-8') as file:
                read_json = json.load(file)
        else:
            read_json = []

        new_records = []
        for data_2 in json_data:
            if data_2 not in read_json:
                new_records.append(data_2)

        if new_records:
            with open('downloads/open.json', 'w', encoding='utf-8') as file:
                json.dump(json_data, file, ensure_ascii=False)

            df = pd.DataFrame(new_records, columns=['CRM', 'TASKNAME', 'CITY', 'ASSIGNEE_NAME', 'KS_3', 'KS_23'])
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
