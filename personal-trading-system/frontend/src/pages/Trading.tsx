import { useState } from 'react'
import { Card, Tabs, Button, Input, Select, Form, message, Alert } from 'antd'
import { 
  ShoppingCartOutlined, 
  LineChartOutlined,
  HistoryOutlined,
  PlusOutlined,
  MinusOutlined,
} from '@ant-design/icons'

const { TabPane } = Tabs
const { Option } = Select

interface OrderForm {
  symbol: string
  side: 'BUY' | 'SELL'
  type: 'MARKET' | 'LIMIT'
  amount: number
  price?: number
}

export default function Trading() {
  const [form] = Form.useForm<OrderForm>()
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('manual')

  const symbols = [
    'BTC/USDT',
    'ETH/USDT',
    'BNB/USDT',
    'SOL/USDT',
    'XRP/USDT',
  ]

  const onFinish = async (values: OrderForm) => {
    setLoading(true)
    try {
      // 这里调用下单API
      console.log('下单参数:', values)
      message.success('订单已提交')
      form.resetFields()
    } catch (error) {
      message.error('下单失败')
    } finally {
      setLoading(false)
    }
  }

  const quickAction = (side: 'BUY' | 'SELL', amount: number) => {
    form.setFieldsValue({
      side,
      amount,
      type: 'MARKET',
    })
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">交易</h1>
        <p className="text-gray-600">手动交易和订单管理</p>
      </div>

      <Alert
        message="注意"
        description="实盘交易前请确保已充分测试，并设置好止损。"
        type="warning"
        showIcon
        className="mb-4"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 左侧：交易表单 */}
        <div className="lg:col-span-2">
          <Card>
            <Tabs activeKey={activeTab} onChange={setActiveTab}>
              <TabPane tab="手动交易" key="manual">
                <Form
                  form={form}
                  layout="vertical"
                  onFinish={onFinish}
                  initialValues={{
                    symbol: 'BTC/USDT',
                    side: 'BUY',
                    type: 'MARKET',
                    amount: 0.01,
                  }}
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Form.Item
                      label="交易对"
                      name="symbol"
                      rules={[{ required: true, message: '请选择交易对' }]}
                    >
                      <Select>
                        {symbols.map(symbol => (
                          <Option key={symbol} value={symbol}>
                            {symbol}
                          </Option>
                        ))}
                      </Select>
                    </Form.Item>

                    <Form.Item
                      label="方向"
                      name="side"
                      rules={[{ required: true, message: '请选择方向' }]}
                    >
                      <Select>
                        <Option value="BUY">
                          <span className="text-success-600">买入</span>
                        </Option>
                        <Option value="SELL">
                          <span className="text-danger-600">卖出</span>
                        </Option>
                      </Select>
                    </Form.Item>

                    <Form.Item
                      label="类型"
                      name="type"
                      rules={[{ required: true, message: '请选择订单类型' }]}
                    >
                      <Select>
                        <Option value="MARKET">市价单</Option>
                        <Option value="LIMIT">限价单</Option>
                      </Select>
                    </Form.Item>

                    <Form.Item
                      label="数量"
                      name="amount"
                      rules={[
                        { required: true, message: '请输入数量' },
                        { type: 'number', min: 0.0001, message: '数量必须大于0' },
                      ]}
                    >
                      <Input type="number" step="0.0001" />
                    </Form.Item>

                    <Form.Item
                      noStyle
                      shouldUpdate={(prevValues, currentValues) => 
                        prevValues.type !== currentValues.type
                      }
                    >
                      {({ getFieldValue }) =>
                        getFieldValue('type') === 'LIMIT' && (
                          <Form.Item
                            label="价格"
                            name="price"
                            rules={[
                              { required: true, message: '请输入价格' },
                              { type: 'number', min: 0.01, message: '价格必须大于0' },
                            ]}
                          >
                            <Input type="number" step="0.01" prefix="$" />
                          </Form.Item>
                        )
                      }
                    </Form.Item>
                  </div>

                  <div className="mt-6 space-y-4">
                    <div className="flex space-x-2">
                      <Button
                        type="primary"
                        icon={<ShoppingCartOutlined />}
                        htmlType="submit"
                        loading={loading}
                        className="flex-1"
                      >
                        提交订单
                      </Button>
                    </div>

                    <div className="flex space-x-2">
                      <Button
                        type="default"
                        icon={<PlusOutlined />}
                        onClick={() => quickAction('BUY', 0.01)}
                        className="flex-1"
                      >
                        快速买入 0.01
                      </Button>
                      <Button
                        type="default"
                        icon={<MinusOutlined />}
                        onClick={() => quickAction('SELL', 0.01)}
                        className="flex-1"
                      >
                        快速卖出 0.01
                      </Button>
                    </div>
                  </div>
                </Form>
              </TabPane>

              <TabPane tab="批量操作" key="batch">
                <div className="text-center py-8">
                  <LineChartOutlined className="text-4xl text-gray-300 mb-4" />
                  <p className="text-gray-500">批量交易功能开发中</p>
                </div>
              </TabPane>

              <TabPane tab="订单管理" key="orders">
                <div className="text-center py-8">
                  <HistoryOutlined className="text-4xl text-gray-300 mb-4" />
                  <p className="text-gray-500">订单管理功能开发中</p>
                </div>
              </TabPane>
            </Tabs>
          </Card>
        </div>

        {/* 右侧：市场信息和快速操作 */}
        <div className="space-y-6">
          <Card title="市场信息">
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">BTC/USDT</span>
                <span className="font-mono">$45,230.50</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">24h涨跌</span>
                <span className="text-success-600">+2.34%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">24h成交量</span>
                <span className="font-mono">$28.5B</span>
              </div>
            </div>
          </Card>

          <Card title="账户概览">
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">总资产</span>
                <span className="font-mono">$10,325.75</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">可用余额</span>
                <span className="font-mono">$7,228.03</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">持仓价值</span>
                <span className="font-mono">$3,097.72</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">今日盈亏</span>
                <span className="text-success-600">+$125.50</span>
              </div>
            </div>
          </Card>

          <Card title="快速操作">
            <div className="space-y-2">
              <Button
                type="primary"
                block
                onClick={() => setActiveTab('manual')}
              >
                新建订单
              </Button>
              <Button block>查看持仓</Button>
              <Button block>资金划转</Button>
              <Button block danger>一键平仓</Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}