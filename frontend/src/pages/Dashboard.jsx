import { useState, useEffect } from 'react'
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from 'recharts'
import {
  DollarSign, ShoppingCart, Grid3X3, TrendingUp,
  ChefHat, Clock,
} from 'lucide-react'
import { StatCard, Badge } from '../components/ui/index'
import { mockStats, mockOrders, mockKitchenTickets } from '../services/mockData'

const PIE_COLORS = ['#10b981', '#f97316', '#3b82f6', '#ef4444']

export default function Dashboard() {
  const [stats] = useState(mockStats)
  const [orders] = useState(mockOrders)
  const [tickets] = useState(mockKitchenTickets)

  const occupied = mockStats.tablesOccupied
  const total    = mockStats.totalTables

  return (
    <div className="space-y-6 animate-slide-up">
      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Today's Revenue"
          value={`$${stats.totalRevenue.toLocaleString()}`}
          subtitle="All payments received"
          icon={DollarSign} color="brand" trend={12}
        />
        <StatCard
          title="Orders Today"
          value={stats.ordersToday}
          subtitle="3 currently active"
          icon={ShoppingCart} color="blue" trend={8}
        />
        <StatCard
          title="Tables Occupied"
          value={`${occupied} / ${total}`}
          subtitle={`${total - occupied} tables free`}
          icon={Grid3X3} color="green"
        />
        <StatCard
          title="Avg Order Value"
          value={`$${stats.avgOrderValue}`}
          subtitle="Per table session"
          icon={TrendingUp} color="purple" trend={-3}
        />
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Revenue by hour */}
        <div className="card p-5 lg:col-span-2">
          <h3 className="font-semibold text-slate-800 mb-4">Revenue by Hour</h3>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={stats.revenueByHour}>
              <defs>
                <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#d4601a" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#d4601a" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="hour" tick={{ fontSize: 11, fill: '#94a3b8' }} />
              <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgb(0 0 0 / 0.1)', fontSize: 12 }}
                formatter={(v) => [`$${v}`, 'Revenue']}
              />
              <Area type="monotone" dataKey="revenue" stroke="#d4601a" strokeWidth={2}
                    fill="url(#revGrad)" dot={false} activeDot={{ r: 4 }} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Orders by status pie */}
        <div className="card p-5">
          <h3 className="font-semibold text-slate-800 mb-4">Orders by Status</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={stats.ordersByStatus} dataKey="count" nameKey="status"
                   cx="50%" cy="50%" innerRadius={50} outerRadius={75} paddingAngle={3}>
                {stats.ordersByStatus.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(v, n) => [v, n]} />
              <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 11 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Bottom row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Active orders */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-slate-800">Active Orders</h3>
            <span className="badge bg-brand-100 text-brand-700">{orders.length} active</span>
          </div>
          <div className="space-y-2">
            {orders.map(o => (
              <div key={o.id} className="flex items-center justify-between py-2.5 px-3 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-brand-100 flex items-center justify-center">
                    <ShoppingCart size={14} className="text-brand-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-800">Table {o.table_id} — #{o.id.slice(-3)}</p>
                    <p className="text-xs text-slate-400">{o.items.length} items · ${o.subtotal}</p>
                  </div>
                </div>
                <Badge status={o.status} />
              </div>
            ))}
          </div>
        </div>

        {/* Kitchen queue */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-slate-800">Kitchen Queue</h3>
            <span className="badge bg-orange-100 text-orange-700">{tickets.length} tickets</span>
          </div>
          <div className="space-y-2">
            {tickets.map(t => (
              <div key={t.id} className="flex items-center justify-between py-2.5 px-3 rounded-lg bg-slate-50">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-orange-100 flex items-center justify-center">
                    <ChefHat size={14} className="text-orange-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-800">{t.item_name} ×{t.quantity}</p>
                    <p className="text-xs text-slate-400 capitalize">{t.station.replace('_', ' ')}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge status={t.status} />
                  <span className="flex items-center gap-1 text-xs text-slate-400">
                    <Clock size={11} />
                    {Math.round((Date.now() - new Date(t.created_at)) / 60000)}m
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
