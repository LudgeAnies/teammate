import { CalendarAPI } from '@/api/calendar'
import { describe, it, expect, vi } from 'vitest'

describe('CalendarAPI', () => {
  beforeEach(() => {
    global.fetch = vi.fn()
  })

  it('fetches calendar data for a year', async () => {
    const mockData = {
      year: 2025,
      days: [
        { date: '2025-01-01', is_working: false },
        { date: '2025-01-02', is_working: true }
      ]
    }

    fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData)
    })

    const data = await CalendarAPI.getYearCalendar(2025)
    expect(data).toEqual(mockData)
    expect(fetch).toHaveBeenCalledWith(
      'https://calendar.kuzyak.in/api/v1/calendar/2025'
    )
  })

  it('checks if a day is working', async () => {
    const mockData = {
      year: 2025,
      days: [
        { date: '2025-01-01', is_working: false },
        { date: '2025-01-02', is_working: true }
      ]
    }

    fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData)
    })

    // Проверка известного праздника
    expect(await CalendarAPI.isWorkingDay('2025-01-01')).toBe(false)

    // Проверка известного рабочего дня
    expect(await CalendarAPI.isWorkingDay('2025-01-02')).toBe(true)

    // Проверка неизвестной даты (должна работать по умолчанию)
    expect(await CalendarAPI.isWorkingDay('2025-01-03')).toBe(true)  // Пятница
    expect(await CalendarAPI.isWorkingDay('2025-01-04')).toBe(false) // Суббота
  })

  it('calculates working days count', async () => {
    const mockData = {
      year: 2025,
      days: [
        { date: '2025-01-01', is_working: false },  // Ср
        { date: '2025-01-02', is_working: false },  // Чт
        { date: '2025-01-03', is_working: true },   // Пт
        { date: '2025-01-04', is_working: false },  // Сб
        { date: '2025-01-05', is_working: false },  // Вс
        { date: '2025-01-06', is_working: true },   // Пн
      ]
    }

    fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData)
    })

    const count = await CalendarAPI.getWorkingDaysCount(
      '2025-01-01',
      '2025-01-06'
    )
    expect(count).toBe(2)  // 3 и 6 января
  })
})