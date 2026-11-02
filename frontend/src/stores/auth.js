import { defineStore } from 'pinia'
import { auth } from '@/utils/api'

export const useAuthStore = defineStore('auth', 
{
  state: () => (
  {
    token: localStorage.getItem('token'),
    user: null,
  }),
  getters: 
  {
    isLoggedIn: (s) => !!s.token,
  },
  actions: 
  {
    async login(username, password) 
    {
      const { data } = await auth.login(username, password)
      this.token = data.access_token
      localStorage.setItem('token', this.token)
      await this.fetchMe()
    },
    async fetchMe() 
    {
      const { data } = await auth.me()
      this.user = data
      console.log(this.user)
    },
    async logout() 
    {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },
  },
})