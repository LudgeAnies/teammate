import { mount } from '@vue/test-utils'
import TaskCard from '@/components/TaskCard.vue'

describe('TaskCard', () => {
  it('renders task title correctly', () => {
    const task = {
      id: 1,
      title: 'Test Task',
      status: 'new',
      priority: 'medium',
      end_date: '2025-02-20T18:00:00Z'
    }
    
    const wrapper = mount(TaskCard, {
      props: { task }
    })

    expect(wrapper.text()).toContain('Test Task')
  })

  it('applies correct priority class', () => {
    const highPriorityTask = {
      id: 1,
      title: 'Urgent Task',
      status: 'new',
      priority: 'high',
      end_date: '2025-02-20T18:00:00Z'
    }

    const wrapper = mount(TaskCard, {
      props: { task: highPriorityTask }
    })

    expect(wrapper.classes()).toContain('high-priority')
  })

  it('emits drag events', async () => {
    const task = {
      id: 1,
      title: 'Draggable Task',
      status: 'new',
      priority: 'medium',
      end_date: '2025-02-20T18:00:00Z'
    }

    const wrapper = mount(TaskCard, {
      props: { task }
    })

    await wrapper.trigger('dragstart')
    expect(wrapper.emitted()).toHaveProperty('dragstart')

    await wrapper.trigger('dragend')
    expect(wrapper.emitted()).toHaveProperty('dragend')
  })
})