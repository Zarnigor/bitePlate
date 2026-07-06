import { useState } from 'react'
import { ShoppingCart, Plus, Check, X, Eye } from 'lucide-react'
import { Badge, PageHeader, Modal, EmptyState } from '../components/ui/index'
import { mockOrders, mockMenuItems } from '../services/mockData'
import clsx from 'clsx'

const STATUS_ORDER = ['draft','confirmed','in_kitchen','served','awaiting_bill','closed','cancelled']

export default function Orders() {
  const [orders, setOrders]       = useState(mockOrders)
  const [viewing, setViewing]     = useState(null)
  const [showNew, setShowNew]     = useState(false)
  const [newOrder, setNewOrder]   = useState({ table_id: '', items: [] })
  const [filter, setFilter]       = useState('all')

  const filtered = filter === 'all' ? orders : orders.filter(o => o.status === filter)

  function addItem(item) {
    setNewOrder(n => {
      const exists = n.items.find(i => i.id === item.id)
      if (exists) return { ...n, items: n.items.map(i => i.id === item.id ? { ...i, qty: i.qty + 1 } : i) }
      return { ...n, items: [...n.items, { ...item, qty: 1 }] }
    })
  }

  function submitOrder() {
    if (!newOrder.table_id || !newOrder.items.length) return
    const order = {
      id: 'ord-' + Date.now(),
      table_id: newOrder.table_id,
      status: 'draft',
      subtotal: newOrder.items.reduce((s, i) => s + i.base_price * i.qty, 0),
      created_at: new Date().toISOString(),
      items: newOrder.items.map(i => ({
        menu_item_name: i.name,
        quantity: i.qty,
        line_total: i.base_price * i.qty,
      })),
    }
    setOrders(o => [order, ...o])
    setNewOrder({ table_id: '', items: [] })
    setShowNew(false)
  }

  function confirmOrder(id) {
    setOrders(os => os.map(o => o.id === id ? { ...o, status: 'confirmed' } : o))
  }
  function cancelOrder(id) {
    setOrders(os => os.map(o => o.id === id ? { ...o, status: 'cancelled' } : o))
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Orders"
        subtitle={`${orders.filter(o => ['confirmed','in_kitchen'].includes(o.status)).length} active orders`}
        action={
          <button onClick={() => setShowNew(true)} className="btn-primary">
            <Plus size={15} /> New Order
          </button>
        }
      />

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {['all', 'draft', 'confirmed', 'in_kitchen', 'served', 'awaiting_bill', 'cancelled'].map(s => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={clsx(
              'px-3 py-1.5 rounded-lg text-xs font-semibold transition-all capitalize',
              filter === s
                ? 'bg-brand-500 text-white shadow-sm'
                : 'bg-white text-slate-500 border border-slate-200 hover:bg-slate-50'
            )}
          >
            {s.replace('_', ' ')}
            <span className="ml-1.5 opacity-60">
              {s === 'all' ? orders.length : orders.filter(o => o.status === s).length}
            </span>
          </button>
        ))}
      </div>

      {/* Orders table */}
      {filtered.length === 0 ? (
        <EmptyState icon={ShoppingCart} title="No orders" description="Create a new order to get started." />
      ) : (
        <div className="card overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-100">
              <tr>
                <th className="table-th">Order</th>
                <th className="table-th">Table</th>
                <th className="table-th">Items</th>
                <th className="table-th">Total</th>
                <th className="table-th">Status</th>
                <th className="table-th">Time</th>
                <th className="table-th">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map(o => (
                <tr key={o.id} className="hover:bg-slate-50 transition-colors">
                  <td className="table-td font-mono text-xs text-slate-500">#{o.id.slice(-6)}</td>
                  <td className="table-td font-semibold">T{o.table_id}</td>
                  <td className="table-td text-slate-500">{o.items.length} items</td>
                  <td className="table-td font-semibold">${o.subtotal.toFixed(2)}</td>
                  <td className="table-td"><Badge status={o.status} /></td>
                  <td className="table-td text-slate-400 text-xs">
                    {Math.round((Date.now() - new Date(o.created_at)) / 60000)}m ago
                  </td>
                  <td className="table-td">
                    <div className="flex items-center gap-1">
                      <button onClick={() => setViewing(o)} className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-500 hover:text-slate-700 transition-colors">
                        <Eye size={14} />
                      </button>
                      {o.status === 'draft' && (
                        <>
                          <button onClick={() => confirmOrder(o.id)} className="p-1.5 rounded-lg hover:bg-emerald-50 text-emerald-600 transition-colors">
                            <Check size={14} />
                          </button>
                          <button onClick={() => cancelOrder(o.id)} className="p-1.5 rounded-lg hover:bg-red-50 text-red-500 transition-colors">
                            <X size={14} />
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* View order modal */}
      <Modal open={!!viewing} onClose={() => setViewing(null)} title={`Order #${viewing?.id?.slice(-6)}`}
        footer={<button onClick={() => setViewing(null)} className="btn-secondary">Close</button>}>
        {viewing && (
          <div className="space-y-3">
            <div className="flex gap-3">
              <Badge status={viewing.status} />
              <span className="text-sm text-slate-500">Table {viewing.table_id}</span>
            </div>
            <div className="divide-y divide-slate-100">
              {viewing.items.map((item, i) => (
                <div key={i} className="flex justify-between py-2 text-sm">
                  <span className="text-slate-700">{item.menu_item_name} × {item.quantity}</span>
                  <span className="font-semibold">${item.line_total.toFixed(2)}</span>
                </div>
              ))}
            </div>
            <div className="flex justify-between pt-2 border-t border-slate-200 font-semibold">
              <span>Subtotal</span>
              <span>${viewing.subtotal.toFixed(2)}</span>
            </div>
          </div>
        )}
      </Modal>

      {/* New order modal */}
      <Modal open={showNew} onClose={() => setShowNew(false)} title="New Order"
        footer={
          <>
            <button onClick={() => setShowNew(false)} className="btn-secondary">Cancel</button>
            <button onClick={submitOrder} className="btn-primary" disabled={!newOrder.table_id || !newOrder.items.length}>
              Create Order
            </button>
          </>
        }>
        <div className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Table Number</label>
            <input className="input mt-1" placeholder="e.g. 3" type="number"
              value={newOrder.table_id} onChange={e => setNewOrder(n => ({ ...n, table_id: e.target.value }))} />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2 block">Add Items</label>
            <div className="grid grid-cols-2 gap-2 max-h-52 overflow-y-auto">
              {mockMenuItems.filter(m => m.is_available).map(m => (
                <button key={m.id} onClick={() => addItem(m)}
                  className="text-left p-2.5 rounded-lg border border-slate-200 hover:border-brand-400 hover:bg-brand-50 transition-all">
                  <p className="text-sm font-medium text-slate-800 truncate">{m.name}</p>
                  <p className="text-xs text-brand-600 font-semibold">${m.base_price}</p>
                </button>
              ))}
            </div>
          </div>
          {newOrder.items.length > 0 && (
            <div className="p-3 rounded-lg bg-slate-50 space-y-1">
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Selected</p>
              {newOrder.items.map(i => (
                <div key={i.id} className="flex justify-between text-sm">
                  <span>{i.name} × {i.qty}</span>
                  <span className="font-semibold">${(i.base_price * i.qty).toFixed(2)}</span>
                </div>
              ))}
              <div className="pt-1 border-t border-slate-200 flex justify-between font-semibold text-sm">
                <span>Total</span>
                <span>${newOrder.items.reduce((s,i) => s + i.base_price * i.qty, 0).toFixed(2)}</span>
              </div>
            </div>
          )}
        </div>
      </Modal>
    </div>
  )
}
