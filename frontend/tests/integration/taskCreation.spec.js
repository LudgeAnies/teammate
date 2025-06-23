import { mount } from '@vue/test-utils'
import TaskForm from '@/components/TaskForm.vue'
import { describe, it, expect, vi } from 'vitest'

describe('Task Creation Flow', () => {
  it('creates a task with subtasks', async () => {
    const mockSubmit = vi.fn()
    const users = [
      { id: 1, full_name: 'User One' }
    ]

    const wrapper = mount(TaskForm, {
      props: {
        users,
        onSubmit: mockSubmit
      }
    })

    // Заполняем основную информацию
    await wrapper.find('input[name="title"]').setValue('Main Task')
    await wrapper.find('select[name="priority"]').setValue('high')

    // Добавляем подзадачу
    await wrapper.find('button#add-subtask').trigger('click')
    await nextTick()

    const subtaskInput = wrapper.find('input[name="subtasks.0.title"]')
    await subtaskInput.setValue('First Subtask')

    // Отправляем форму
    await wrapper.find('form').trigger('submit.prevent')

    expect(mockSubmit).toHaveBeenCalled()
    expect(mockSubmit.mock.calls[0][0]).toMatchObject({
      title: 'Main Task',
      priority: 'high',
      subtasks: [
        { title: 'First Subtask' }
      ]
    })
  })
})