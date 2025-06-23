from django.test import TestCase
from unittest.mock import patch, Mock
from datetime import date
from projects.services.calendar_api import ProductionCalendarAPI


class ProductionCalendarAPITest(TestCase):
    @patch('requests.get')
    def test_get_calendar_data(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'year': 2025,
            'days': [
                {'date': '2025-01-01', 'is_working': False},
                {'date': '2025-01-02', 'is_working': False},
                {'date': '2025-01-09', 'is_working': True}
            ]
        }
        mock_get.return_value = mock_response

        data = ProductionCalendarAPI.get_calendar_data(2025)
        self.assertEqual(data['year'], 2025)
        self.assertEqual(len(data['days']), 3)

    @patch('projects.services.calendar_api.ProductionCalendarAPI.get_calendar_data')
    def test_is_working_day(self, mock_get_calendar_data):
        mock_get_calendar_data.return_value = {
            'year': 2025,
            'days': [
                {'date': '2025-01-01', 'is_working': False},
                {'date': '2025-01-09', 'is_working': True}
            ]
        }

        # Проверка известного праздника
        self.assertFalse(ProductionCalendarAPI.is_working_day(date(2025, 1, 1)))

        # Проверка известного рабочего дня
        self.assertTrue(ProductionCalendarAPI.is_working_day(date(2025, 1, 9)))

        # Проверка неизвестной даты (должна работать по умолчанию)
        self.assertTrue(ProductionCalendarAPI.is_working_day(date(2025, 1, 10)))  # Пятница
        self.assertFalse(ProductionCalendarAPI.is_working_day(date(2025, 1, 11)))  # Суббота

    @patch('projects.services.calendar_api.ProductionCalendarAPI.get_calendar_data')
    def test_get_working_days_count(self, mock_get_calendar_data):
        mock_get_calendar_data.return_value = {
            'year': 2025,
            'days': [
                {'date': '2025-01-01', 'is_working': False},  # Ср
                {'date': '2025-01-02', 'is_working': False},  # Чт
                {'date': '2025-01-03', 'is_working': True},  # Пт
                {'date': '2025-01-04', 'is_working': False},  # Сб
                {'date': '2025-01-05', 'is_working': False},  # Вс
                {'date': '2025-01-06', 'is_working': True},  # Пн
            ]
        }

        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 6)

        count = ProductionCalendarAPI.get_working_days_count(start_date, end_date)
        self.assertEqual(count, 2)  # 3 и 6 января