import { ref } from 'vue'
import { useTaskDeadline } from '@/composables/useTaskDeadline'
import { describe, it, expect, vi } from 'vitest'

// Мокаем CalendarAPI
vi.mock('@/api/calendar', () => ({
  CalendarAPI: {
    getWorkingDaysCount: vi.fn(() => Promise.resolve(5)),
    isWorkingDay: vi.fn((date) =>
      Promise.resolve(date.endsWith('02-10') || date.endsWith('02-12'))
    )
  }
}))

describe('useTaskDeadline', () => {
  it('calculates working days and hours', async () => {
    const { workingDays, workingHours, updateDates } = useTaskDeadline()

    await updateDates('2025-02-10', '2025-02-20')

    expect(workingDays.value).toBe(5)
    expect(workingHours.value).toBe(40)
  })

  it('detects deadline warnings', async () => {
    const { isDeadlineWarning, updateDates } = useTaskDeadline()

    // Нерабочий день
    await updateDates('2025-02-10', '2025-02-11')
    expect(isDeadlineWarning.value).toBe(true)

    // Рабочий день
    await updateDates('2025-02-10', '2025-02-12')
    expect(isDeadlineWarning.value).toBe(false)
  })
})