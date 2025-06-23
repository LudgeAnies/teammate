import { setActivePinia, createPinia } from 'pinia'
import { useProjectStore } from '@/stores/project'
import { describe, beforeEach, it, expect, vi } from 'vitest'

describe('Project Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('fetches project data', async () => {
    const mockProject = {
      id: 1,
      name: 'Test Project',
      slug: 'test-project',
      tasks: []
    }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockProject)
      })
    )

    const store = useProjectStore()
    await store.fetchProject('test-org', 'test-project')

    expect(fetch).toHaveBeenCalledWith(
      '/api/organizations/test-org/projects/test-project/'
    )
    expect(store.currentProject).toEqual(mockProject)
  })

  it('handles fetch errors', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        status: 404
      })
    )

    const store = useProjectStore()

    await expect(
      store.fetchProject('test-org', 'invalid-project')
    ).rejects.toThrow()
  })
})