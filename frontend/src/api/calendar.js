import axios from 'axios'

const API_BASE = 'https://calendar.kuzyak.in/api/v1/calendar'

export const CalendarAPI = {
  async getYearCalendar(year) {
    if (calendarCache.has(year)) {
      return calendarCache.get(year)
    }

    try {
      const response = await axios.get(`${API_BASE}/${year}`)
      return response.data
    } catch (error) {
      console.error('Error fetching production calendar:', error)
      return null
    }
  },

  async isWorkingDay(date) {
    const dateObj = new Date(date)
    const year = dateObj.getFullYear()
    const calendar = await this.getYearCalendar(year)

    if (!calendar) {
      // Fallback: только выходные
      return dateObj.getDay() !== 0 && dateObj.getDay() !== 6
    }

    const dateStr = dateObj.toISOString().split('T')[0]
    const dayData = calendar.days.find(day => day.date === dateStr)

    return dayData ? dayData.is_working : (dateObj.getDay() !== 0 && dateObj.getDay() !== 6)
  },

  async getWorkingDaysCount(startDate, endDate) {
    const start = new Date(startDate)
    const end = new Date(endDate)

    if (start.getFullYear() !== end.getFullYear()) {
      return this._getWorkingDaysCountMultiYear(start, end)
    }

    const calendar = await this.getYearCalendar(start.getFullYear())
    if (!calendar) {
      return this._defaultWorkingDaysCount(start, end)
    }

    let count = 0
    let current = new Date(start)

    while (current <= end) {
      const dateStr = current.toISOString().split('T')[0]
      const dayData = calendar.days.find(day => day.date === dateStr)

      if (dayData) {
        if (dayData.is_working) count++
      } else {
        if (current.getDay() !== 0 && current.getDay() !== 6) count++
      }

      current.setDate(current.getDate() + 1)
    }

    return count
  },

  async _getWorkingDaysCountMultiYear(start, end) {
    let total = 0
    let current = new Date(start)

    while (current <= end) {
      const yearEnd = new Date(current.getFullYear(), 11, 31)
      const periodEnd = new Date(Math.min(yearEnd, end))

      total += await this.getWorkingDaysCount(current, periodEnd)
      current = new Date(periodEnd)
      current.setDate(current.getDate() + 1)
    }

    return total
  },

  _defaultWorkingDaysCount(start, end) {
    let count = 0
    let current = new Date(start)

    while (current <= end) {
      if (current.getDay() !== 0 && current.getDay() !== 6) {
        count++
      }
      current.setDate(current.getDate() + 1)
    }

    return count
  }
}