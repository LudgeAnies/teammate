import { mount } from '@vue/test-utils'
import Register from '@/views/Register.vue'
import axios from 'axios'

jest.mock('axios')

describe('Register.vue', () => {
  it('Проверка совпадения паролей', async () => {
    const wrapper = mount(Register)
    await wrapper.find('input[placeholder="Email"]').setValue('test@example.com')
    await wrapper.find('input[placeholder="Имя пользователя"]').setValue('user')
    await wrapper.find('input[placeholder="Имя"]').setValue('Тест')
    await wrapper.find('input[placeholder="Фамилия"]').setValue('Тестов')
    await wrapper.find('input[placeholder="Пароль"]').setValue('Ks5#Mz4#Pw4%')
    await wrapper.find('input[placeholder="Подтвердить пароль"]').setValue('Ks#Mz4#Pw4%')
    await wrapper.find('form').trigger('submit.prevent')
    expect(wrapper.text()).toContain('Пароли не совпадают')
  })

  it('Успешная регистрация редиректит', async () => {
    axios.post.mockResolvedValue({})
    const routerPush = jest.fn()
    const wrapper = mount(Register, {
      global: { mocks: { $router: { push: routerPush } } }
    })
    await wrapper.find('input[placeholder="Email"]').setValue('test@example.com')
    await wrapper.find('input[placeholder="Имя пользователя"]').setValue('user')
    await wrapper.find('input[placeholder="Имя"]').setValue('Тест')
    await wrapper.find('input[placeholder="Фамилия"]').setValue('Тестов')
    await wrapper.find('input[placeholder="Пароль"]').setValue('Ks5#Mz4#Pw4%')
    await wrapper.find('input[placeholder="Подтвердить пароль"]').setValue('Ks5#Mz4#Pw4%')
    await wrapper.find('form').trigger('submit.prevent')
    expect(axios.post).toHaveBeenCalled()
  })
})
