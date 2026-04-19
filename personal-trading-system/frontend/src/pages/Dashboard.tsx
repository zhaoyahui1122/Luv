import { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Table, Tag, Progress, Alert } from 'antd'
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  DollarOutlined,
  PieChartOutlined,
  LineChartOutlined,
  SafetyOutlined,
} from '@ant-design/icons'
import { useQuery } from 'react-query'
import api from '@/services/api'

interface DashboardStats {
  totalBalance: number
  totalPnl: number
  pnlPercentage: number
  activePositions: number
  winRate: number
  dailyVolume: number
}

interface RecentTrade {
  id: string
  symbol: string
  side: 'BUY' | 'SELL'
  amount: number
  price: number
  pnl: number
  timestamp: string
}

interface Position {
  symbol: string
  amount: number
  entryPrice: number
  currentPrice: number
  pnl: number
  pnlPercentage: number
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalBalance: 10000,
    totalPnl: 325.75,
    pnlPercentage: 3.26,
    activePositions: 3,
    winRate: 65.2,
    dailyVolume: 12500,
  })

  const { data: recentTrades = [], isLoading: tradesLoading } = useQuery(
    'recentTrades',
    () => api.getRecentTrades(),
    {
      refetchInterval: 10000, // 10秒刷新一次
    }
  )

  const { data: positions = [], isLoading: positionsLoading } = useQuery(
    'positions',
    () => api.getPositions(),
    {
      refetchInterval: 5000, // 5秒刷新一次
    }
  )

  const columns = [
    {
      title: '交易对',
      dataIndex: 'symbol',
      key: 'symbol',
      render: (symbol: string) => <span className="font-mono">{symbol}</span>,
    },
    {
      title: '方向',
      dataIndex: 'side',
      key: 'side',
      render: (side: 'BUY' | 'SELL') => (
        <Tag color={side === 'BUY' ? 'success' : 'error'}>
          {side === 'BUY' ? '买入' : '卖出'}
        </Tag>
      ),
    },
    {
      title: '数量',
      dataIndex: 'amount',
      key: 'amount',
      render: (amount: number) => amount.toFixed(4),
    },
    {
      title: '价格',
      dataIndex: 'price',
      key: 'price',
      render: (price: number) => `$${price.toFixed(2)}`,
    },
    {
      title: '盈亏',
      dataIndex: 'pnl',
      key: 'pnl',
      render: (pnl: number) => (
        <span className={pnl >= 0 ? 'profit' : 'loss'}>
          ${pnl.toFixed(2)}
        </span>
      ),
    },
    {
      title: '时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
      render: (timestamp: string) => new Date(timestamp).toLocaleTimeString(),
    },
  ]

  const positionColumns = [
    {
      title: '交易对',
      dataIndex: 'symbol',
      key: 'symbol',
      render: (symbol: string) => <span className="font-mono">{symbol}</span>,
    },
    {
      title: '持仓数量',
      dataIndex: 'amount',
      key: 'amount',
      render: (amount: number) => amount.toFixed(4),
    },
    {
      title: '入场价格',
      dataIndex: 'entryPrice',
      key: 'entryPrice',
      render: (price: number) => `$${price.toFixed(2)}`,
    },
    {
      title: '当前价格',
      dataIndex: 'currentPrice',
      key: 'currentPrice',
      render: (price: number) => `$${price.toFixed(2)}`,
    },
    {
      title: '盈亏',
      dataIndex: 'pnl',
      key: 'pnl',
      render: (pnl: number) => (
        <span className={pnl >= 0 ? 'profit' : 'loss'}>
          ${pnl.toFixed(2)}
        </span>
      ),
    },
    {
      title: '盈亏率',
      dataIndex: 'pnlPercentage',
      key: 'pnlPercentage',
      render: (percentage: number) => (
        <span className={percentage >= 0 ? 'profit' : 'loss'}>
          {percentage >= 0 ? '+' : ''}{percentage.toFixed(2)}%
        </span>
      ),
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">仪表盘</h1>
        <p className="text-gray-600">系统概览和实时交易数据</p>
      </div>

      <Alert
        message="模拟交易模式"
        description="当前处于模拟交易模式，所有交易均为模拟操作。"
        type="info"
        showIcon
        className="mb-4"
      />

      {/* 统计卡片 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总资产"
              value={stats.totalBalance}
              prefix={<DollarOutlined />}
              suffix="USD"
              valueStyle={{ color: '#3f8600' }}
            />
            <div className="mt-2 text-sm text-gray-500">
              可用余额: ${(stats.totalBalance * 0.7).toFixed(2)}
            </div>
          </Card>
        </Col>
        
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总盈亏"
              value={stats.totalPnl}
              prefix={stats.pnlPercentage >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
              suffix="USD"
              valueStyle={{ color: stats.pnlPercentage >= 0 ? '#3f8600' : '#cf1322' }}
            />
            <div className="mt-2 text-sm text-gray-500">
              {stats.pnlPercentage >= 0 ? '+' : ''}{stats.pnlPercentage}%
            </div>
          </Card>
        </Col>
        
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="活跃仓位"
              value={stats.activePositions}
              prefix={<PieChartOutlined />}
              suffix="个"
            />
            <div className="mt-2">
              <Progress percent={65} size="small" />
            </div>
          </Card>
        </Col>
        
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="胜率"
              value={stats.winRate}
              prefix={<SafetyOutlined />}
              suffix="%"
            />
            <div className="mt-2 text-sm text-gray-500">
              今日交易: 8笔
            </div>
          </Card>
        </Col>
      </Row>

      {/* 持仓和交易记录 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card
            title={
              <div className="flex items-center">
                <LineChartOutlined className="mr-2" />
                当前持仓
              </div>
            }
            className="h-full"
          >
            <Table
              dataSource={positions}
              columns={positionColumns}
              rowKey="symbol"
              loading={positionsLoading}
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
        
        <Col xs={24} lg={12}>
          <Card
            title="最近交易"
            className="h-full"
          >
            <Table
              dataSource={recentTrades}
              columns={columns}
              rowKey="id"
              loading={tradesLoading}
              pagination={{ pageSize: 5 }}
              size="small"
            />
          </Card>
        </Col>
      </Row>

      {/* 系统状态 */}
      <Card title="系统状态">
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={8}>
            <div className="text-center">
              <div className="text-2xl font-bold text-success-600">正常</div>
              <div className="text-gray-600">交易引擎</div>
            </div>
          </Col>
          <Col xs={24} sm={8}>
            <div className="text-center">
              <div className="text-2xl font-bold text-success-600">在线</div>
              <div className="text-gray-600">交易所连接</div>
            </div>
          </Col>
          <Col xs={24} sm={8}>
            <div className="text-center">
              <div className="text-2xl font-bold text-warning-600">监控中</div>
              <div className="text-gray-600">风控系统</div>
            </div>
          </Col>
        </Row>
      </Card>
    </div>
  )
}