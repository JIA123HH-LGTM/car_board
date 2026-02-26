import axios from 'axios'

const service = axios.create({
  baseURL: 'https://jia123hh.pythonanywhere.com/myApp/',
  timeout: 10000
})

export default service
