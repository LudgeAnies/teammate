import requests
from datetime import date, timedelta
#from django.conf import settings
from django.core.cache import cache


class ProductionCalendarAPI:
    BASE_URL = "https://calendar.kuzyak.in/api/v1/calendar"

    @classmethod
    def get_calendar_data(cls, year=None):
        if not year:
            year = date.today().year

        cache_key = f"production_calendar_{year}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        try:
            response = requests.get(f"{cls.BASE_URL}/{year}", timeout=5)
            response.raise_for_status()
            data = response.json()
            cache.set(cache_key, data, timeout=86400)  # Кэшируем на 1 день
            return data
        except (requests.RequestException, ValueError) as e:
            # Fallback: можно вернуть дефолтные данные или залогировать ошибку
            return None

    @classmethod
    def is_working_day(cls, date_obj):
        year = date_obj.year
        calendar_data = cls.get_calendar_data(year)

        if not calendar_data:
            # Если API недоступно, считаем все будни рабочими днями
            return date_obj.weekday() < 5

        day_data = next(
            (day for day in calendar_data['days']
             if day['date'] == date_obj.isoformat()),
            None
        )

        if day_data:
            return day_data['is_working']

        return date_obj.weekday() < 5  # По умолчанию для неизвестных дат

    @classmethod
    def get_working_days_count(cls, start_date, end_date):
        year = start_date.year
        if end_date.year != year:
            # Если период охватывает несколько лет, нужно обработать отдельно
            return cls._get_working_days_count_multi_year(start_date, end_date)

        calendar_data = cls.get_calendar_data(year)
        if not calendar_data:
            # Fallback: считаем все будни рабочими днями
            return cls._default_working_days_count(start_date, end_date)

        working_days = 0
        current_date = start_date

        while current_date <= end_date:
            day_data = next(
                (day for day in calendar_data['days']
                 if day['date'] == current_date.isoformat()),
                None
            )

            if day_data:
                if day_data['is_working']:
                    working_days += 1
            else:
                # Если данные для даты отсутствуют, считаем по умолчанию
                if current_date.weekday() < 5:
                    working_days += 1

            current_date += timedelta(days=1)

        return working_days

    @classmethod
    def _get_working_days_count_multi_year(cls, start_date, end_date):
        # Обработка периода, охватывающего несколько лет
        total = 0
        current_date = start_date

        while current_date <= end_date:
            year_end = date(current_date.year, 12, 31)
            period_end = min(year_end, end_date)
            total += cls.get_working_days_count(current_date, period_end)
            current_date = period_end + timedelta(days=1)

        return total

    @classmethod
    def _default_working_days_count(cls, start_date, end_date):
        # Подсчет рабочих дней без учета праздников (только выходные)
        count = 0
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() < 5:
                count += 1
            current_date += timedelta(days=1)

        return count