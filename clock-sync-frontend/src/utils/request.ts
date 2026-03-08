import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
});

instance.interceptors.response.use(
  (res) => res.data,
  (err) => Promise.reject(err)
);

// 拦截器已返回 res.data，此处直接返回 Promise 结果即可，不要再取 .data
export default {
  get: <T>(url: string, config?: object) => instance.get<T>(url, config) as Promise<T>,
  post: <T>(url: string, data?: object, config?: object) => instance.post<T>(url, data, config) as Promise<T>
};
