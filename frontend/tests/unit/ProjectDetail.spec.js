import { mount } from '@vue/test-utils'
import ProjectDetail from '@/views/ProjectDetail.vue'
import { createPinia, setActivePinia } from 'pinia'
import { useProjectStore } from '@/stores/project'
import { nextTick } from 'vue'

describe('ProjectDetail', () => {
  let wrapper
  let store

  const mockProject = {
    id: 1,
    name: 'Test Project',
    slug: 'test-project',
    description: 'Test description',
    status: 'implementation',
    deadline: '2025-06-30',
    tasks: [
      { id: 1, title: 'Task 1', status: 'new' },
      { id: 2, title: 'Task 2', status: 'completed' }
    ],
    roles: [
      { user: { full_name: 'User 1' }, role: 'leader' }
    ]
  }

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useProjectStore()
    store.currentProject = mockProject

    wrapper = mount(ProjectDetail, {
      global: {
        stubs: ['TaskList', 'GanttChart', 'YandexCalendar', 'ProjectMembers', 'ProjectExportButton']
      }
    })
  })

  it('renders project name', () => {
    expect(wrapper.text()).toContain('Test Project')
  })

  it('displays project status', () => {
    expect(wrapper.text()).toContain('Status: implementation')
  })

  it('shows correct deadline', () => {
    expect(wrapper.text()).toContain('Deadline: 30.06.2025')
  })

  it('switches between tabs', async () => {
    expect(wrapper.text()).toContain('Tasks') // Default tab

    const ganttTab = wrapper.findAll('button').find(b => b.text() === 'Gantt Chart')
    await ganttTab.trigger('click')

    expect(wrapper.text()).toContain('Project Timeline')
  })

  it('displays loading state', async () => {
    store.currentProject = null
    await nextTick()

    expect(wrapper.text()).toContain('Loading...')
  })
})