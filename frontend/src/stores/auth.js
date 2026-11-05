import { defineStore } from 'pinia'
import { auth } from '../utils/api'
import { OnyksToastContainer } from 'onyks-web-ui'

let refreshPromise = null

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
    hasRank: (s) => (...ranks) => ranks.includes(s.user?.rank),
  },
  actions: 
  {
    async init() 
    {
      if (this.token) 
      {
        await this.fetch_me()
      }
    },
    async login(username, password) 
    {
      const { data } = await auth.login(username, password)
      this.token = data.access_token
      localStorage.setItem('token', this.token)
      await this.fetch_me()
      OnyksToastContainer.success('Logged in successfully.')
    },
    async fetch_me() 
    {
      const { data } = await auth.me()
      this.user = data
    },
    refresh() 
    {
      if (!refreshPromise) 
      {
        refreshPromise = auth.refresh().then(({ data }) => 
        {
            this.token = data.access_token
            localStorage.setItem('token', this.token)
        }).finally(() => { refreshPromise = null })
      }
      return refreshPromise
    },

    clear() 
    {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },

    async logout() 
    {
      try 
      { 
        OnyksToastContainer.info('Logging out...')
        await auth.logout()
      } 
      catch {}
      this.clear()
    },
  },
})