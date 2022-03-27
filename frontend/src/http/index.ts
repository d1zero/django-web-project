import axios, { AxiosInstance } from 'axios'

export const API_URL = import.meta.env.VITE_API_URL

const $api: AxiosInstance = axios.create({ baseURL: API_URL })

export default $api