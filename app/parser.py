from collections import defaultdict
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
import pandas as pd
from config import url
import os


def get_data():
    """Получает JSON массив"""
    try:
        """
        response = requests.get(url, timeout=3)
        response.raise_for_status()  # Проверка на успешный HTTP-статус

        bs = BeautifulSoup(response.text, "lxml")
        temp = bs.find('pre')
        json_string = temp.text
        json_data = json.loads(json_string)
        """
        session = HTMLSession()
        json_data = session.get(url).json()

        unique_data = []
        seen_records = set()

        for record in json_data:
            record_id = record.get('CRM')
            if record_id not in seen_records:
                seen_records.add(record_id)
                unique_data.append(record)

        return unique_data

    except Exception as e:
        raise Exception(f"Err: {e}")


def parse_datetime(date_str):
    """Изменяет формат времени"""
    return datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')


def check_data():
    """Проверка массива JSON на добавление новых строк"""
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
            result_text = ""
            for record in new_records:
                create_date = parse_datetime(record['CREATE_KI'])
                open_date = parse_datetime(record['OPEN_DATE'])
                start_date = parse_datetime(record['START_KI'])
                stop_date = parse_datetime(record['STOP_KI'])
                current_date = datetime.now()

                result_text += f"1. Участок: {record['WORKSITE_SHORT_NAME']}\n"
                result_text += f"2. Номер заявки: {record['CRM']}\n"
                result_text += f"3. Исполнитель: {record['ASSIGNEE_NAME']}\n"
                result_text += f"4. Дата создания: {create_date}\n"
                result_text += f"5. КС 3 ЛТП: {create_date + timedelta(hours=20)}\n"
                result_text += f"6. КС 2+3: {open_date + timedelta(hours=24)}\n"
                result_text += f"7. Интервал согласованный: {start_date} | {stop_date}\n"

                if stop_date < (create_date + timedelta(hours=20)):
                    result_text += f"8. Статус: Нормально\n"
                elif stop_date > (create_date + timedelta(hours=20)):
                    result_text += f"8. Статус: Изменить интервал | {stop_date - (create_date + timedelta(hours=20))}\n"
                elif record['ASSIGNEE_NAME'] is None:
                    result_text += f"8. Статус: Назначить исполнителя | {current_date - create_date}\n"

                if record['DATE_CLOSE']:
                    result_text += f"9. Закрыто: Да | {record['DATE_CLOSE']}\n\n"
                else:
                    result_text += f"9. Закрыто: Нет\n\n"

            with open('downloads/open.json', 'w', encoding='utf-8') as file:
                json.dump(json_data, file, ensure_ascii=False)

            return result_text

    except Exception as e:
        raise Exception(f"Err: {e}")


def convert_data(message):
    """Форматирует данные из JSON и заносит их в Excel"""
    try:
        json_data = get_data()
        my_list = []

        if message == 'all':
            columns = ['CRM', 'WORKSITE_SHORT_NAME', 'CREATE_KI', 'OPEN_DATE', 'START_KI', 'STOP_KI', 'ASSIGNEE_NAME']

        elif message == 'unexecuted':
            for data in json_data:
                if data['ASSIGNEE_NAME'] is None:
                    my_list.append(data)
            columns = ['CRM', 'WORKSITE_SHORT_NAME', 'CREATE_KI', 'OPEN_DATE', 'START_KI', 'STOP_KI', 'COMMENTARY']

        else:
            raise ValueError("Invalid message type")

        status_list = []
        for record in my_list if my_list else json_data:
            create_date = parse_datetime(record['CREATE_KI'])
            stop_date = parse_datetime(record['STOP_KI'])
            current_date = datetime.now()

            result_text = ""
            if stop_date < (create_date + timedelta(hours=20)):
                result_text = "Нормально"
            elif stop_date > (create_date + timedelta(hours=20)):
                result_text = f"Изменить интервал | {stop_date - (create_date + timedelta(hours=20))}"
            elif record['ASSIGNEE_NAME'] is None:
                result_text = f"Назначить исполнителя | {current_date - create_date}"

            status_list.append(result_text)

        df = pd.DataFrame(my_list if my_list else json_data, columns=columns)
        df['STATUS'] = status_list

        file_name = f'{message}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.xlsx'
        file_path = f'downloads/{file_name}'
        df.to_excel(file_path, index=False)

        return file_path

    except Exception as e:
        raise Exception(f"Err: {e}")


def calculate_city():
    """Считает кол-во заявок по городам и время между заявками"""
    json_data = get_data()

    city_stats = defaultdict(lambda: {'today': 0, 'more_2_days': 0, 'more_7_days': 0})
    for data in json_data:
        city = data['CITY']
        create_date = parse_datetime(data['CREATE_KI'])
        current_date = datetime.now()
        time_difference = current_date - create_date

        if time_difference.days == 0:
            city_stats[city]['today'] += 1
        elif time_difference.days > 7:
            city_stats[city]['more_7_days'] += 1
        else:
            city_stats[city]['more_2_days'] += 1

    result_text = ""
    for city, stats in city_stats.items():
        total = stats['today'] + stats['more_2_days'] + stats['more_7_days']
        result_text += f"Город: {city} | Кол-во заявок: {total}\n"
        result_text += f"1. Новых сегодня - {stats['today']} шт\n"
        result_text += f"2. Более 2 дня- {stats['more_2_days']} шт\n"
        result_text += f"3. Более 7 дней - {stats['more_7_days']} шт\n\n"

    return result_text