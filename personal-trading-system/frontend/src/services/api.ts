import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      // 服务器返回错误
      const { status, data } = error.response
      
      if (status === 401) {
        // 未授权，跳转到登录页
        localStorage.removeItem('auth_token')
        window.location.href = '/login'
      }
      
      return Promise.reject({
        status,
        message: data?.detail || '请求失败',
        data,
      })
    } else if (error.request) {
      // 请求发送失败
      return Promise.reject({
        status: 0,
        message: '网络连接失败，请检查网络设置',
      })
    } else {
      // 其他错误
      return Promise.reject({
        status: -1,
        message: error.message || '未知错误',
      })
    }
  }
)

// 系统API
export const systemApi = {
  // 获取系统状态
  getStatus: () => api.get('/api/v1/status'),
  
  // 启动交易引擎
  startEngine: () => api.post('/api/v1/engine/start'),
  
  // 停止交易引擎
  stopEngine: () => api.post('/api/v1/engine/stop'),
  
  // 健康检查
  healthCheck: () => api.get('/health'),
}

// 交易API
export const tradingApi = {
  // 获取持仓
  getPositions: () => api.get('/api/v1/positions'),
  
  // 获取余额
  getBalance: () => api.get('/api/v1/balance'),
  
  // 获取订单
  getOrders: (params?: any) => api.get('/api/v1/orders', { params }),
  
  // 下单
  placeOrder: (data: any) => api.post('/api/v1/order', data),
  
  // 取消订单
  cancelOrder: (orderId: string) => api.delete(`/api/v1/order/${orderId}`),
  
  // 获取最近交易
  getRecentTrades: () => api.get('/api/v1/trades/recent'),
  
  // 获取行情
  getTicker: (symbol: string) => api.get(`/api/v1/ticker/${symbol}`),
  
  // 获取K线数据
  getOHLCV: (symbol: string, timeframe?: string) => 
    api.get(`/api/v1/ohlcv/${symbol}`, { params: { timeframe } }),
}

// 策略API
export const strategyApi = {
  // 获取策略列表
  getStrategies: () => api.get('/api/v1/strategies'),
  
  // 启用/禁用策略
  toggleStrategy: (strategyName: string, enabled: boolean) =>
    api.post(`/api/v1/strategies/${strategyName}/toggle`, { enabled }),
  
  // 获取策略参数
  getStrategyParams: (strategyName: string) =>
    api.get(`/api/v1/strategies/${strategyName}/params`),
  
  // 更新策略参数
  updateStrategyParams: (strategyName: string, params: any) =>
    api.put(`/api/v1/strategies/${strategyName}/params`, params),
  
  // 运行回测
  runBacktest: (data: any) => api.post('/api/v1/backtest', data),
}

// 风控API
export const riskApi = {
  // 获取风控状态
  getRiskStatus: () => api.get('/api/v1/risk/status'),
  
  // 设置风控级别
  setRiskLevel: (level: number) => api.post('/api/v1/risk/level', { level }),
  
  // 获取风控记录
  getRiskLogs: (params?: any) => api.get('/api/v1/risk/logs', { params }),
}

// 设置API
export const settingsApi = {
  // 获取系统设置
  getSettings: () => api.get('/api/v1/settings'),
  
  // 更新系统设置
  updateSettings: (data: any) => api.put('/api/v1/settings', data),
  
  // 获取交易所配置
  getExchangeConfig: () => api.get('/api/v1/settings/exchange'),
  
  // 更新交易所配置
  updateExchangeConfig: (data: any) => api.put('/api/v1/settings/exchange', data),
  
  // 测试交易所连接
  testExchangeConnection: (exchange: string) =>
    api.post('/api/v1/settings/exchange/test', { exchange }),
}

// AI助手API
export const aiApi = {
  // AI对话
  chat: (message: string) => api.post('/api/v1/ai/chat', { message }),
  
  // 市场分析
  analyzeMarket: (symbol: string) => api.post('/api/v1/ai/analyze', { symbol }),
}

// 通知API
export const notificationApi = {
  // 发送测试通知
  sendTestNotification: (type: string) =>
    api.post('/api/v1/notifications/test', { type }),
  
  // 获取通知设置
  getNotificationSettings: () => api.get('/api/v1/notifications/settings'),
  
  // 更新通知设置
  updateNotificationSettings: (data: any) =>
    api.put('/api/v1/notifications/settings', data),
}

// 数据API
export const dataApi = {
  // 获取市场数据
  getMarketData: (symbol: string, params?: any) =>
    api.get(`/api/v1/data/market/${symbol}`, { params }),
  
  // 导出交易数据
  exportTradingData: (format: string = 'csv') =>
    api.get(`/api/v1/data/export`, { params: { format } }),
  
  // 清理历史数据
  cleanupHistoryData: (days: number) =>
    api.delete('/api/v1/data/history', { params: { days } }),
}

// 默认导出所有API
export default {
  ...systemApi,
  ...tradingApi,
  ...strategyApi,
  ...riskApi,
  ...settingsApi,
  ...aiApi,
  ...notificationApi,
  ...dataApi,
  
  // 原始axios实例
  axios: api,
}