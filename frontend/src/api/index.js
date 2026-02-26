import axios from 'axios'

const service = axios.create({
  baseURL: 'https://jia123hh.pythonanywhere.com/',
  timeout: 10000
})

export default service
