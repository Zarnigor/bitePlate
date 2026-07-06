import { useState } from 'react'
import { Receipt, CreditCard, Split } from 'lucide-react'
import { Badge, PageHeader, Modal } from '../components/ui/index'
import { mockOrders } from '../services/mockData'
import clsx from 'clsx'

const STRATEGIES = [
  { key: 'standard',   label: 'Standard',         desc: 'Full price',          discount: 0    },
  { key: 'happy_hour', label: 'Happy Hour',        desc: '20% off everything',  discount: 20   },
  { key: 'loyalty',    label: 'Loyalty Card',      desc: '10% off + free drink',discount: 10   },
  { key: 'group',      label: 'Group Discount',    desc: '15% off (8+ guests)', discount: 15   },
]

const TAX_RATE = 0.12

export default function Billing() {
  const [billable]   = useState(mockOrders.filter(o => ['served','awaiting_bill'].includes(o.status)))
  const [bills, setBills] = useState([])
  const [selected, setSelected] = useState(null)
  const [config, setConfig]     = useState({ strategy: 'standard', tip: 0, split: 1 })
  const [generated, setGenerated] = useState(null)

  function generateBill(order) {
    const strat = STRATEGIES.find(s => s.key === config.strategy)
    const subtotal  = order.subtotal
    const discounted = subtotal * (1 - strat.discount / 100)
    const tax       = discounted * TAX_RATE
    const tip       = discounted * (config.tip / 100)
    const total     = discounted + tax + tip
    const bill = {
      id: 'bill-' + Date.now(),
      order_id: order.id,
      table_id: order.table_id,
      subtotal,
      discount: subtotal - discounted,
      tax: +tax.toFixed(2),
      tip: +tip.toFixed(2),
      total: +total.toFixed(2),
      per_person: +(total / config.split).toFixed(2),
      strategy: strat.label,
      split: config.split,
      is_paid: false,
    }
    setGenerated(bill)
  }

  function payBill() {
    setBills(bs => [...bs, { ...generated, is_paid: true }])
    setGenerated(null)
    setSelected(null)
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Billing"
        subtitle={`${billable.length} orders ready to bill · ${bills.filter(b=>b.is_paid).length} paid today`}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pending bills */}
        <div className="card p-5">
          <h3 className="font-semibold text-slate-800 mb-4">Ready to Bill</h3>
          <div className="space-y-2">
            {billable.map(o => (
              <button key={o.id} onClick={() => { setSelected(o); setGenerated(null) }}
                className={clsx(
                  'w-full text-left p-3 rounded-xl border transition-all',
                  selected?.id === o.id
                    ? 'border-brand-400 bg-brand-50'
                    : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                )}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-xl bg-brand-100 flex items-center justify-center">
                      <Receipt size={16} className="text-brand-600" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-slate-800">Table {o.table_id}</p>
                      <p className="text-xs text-slate-400">{o.items.length} items · #{o.id.slice(-4)}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-slate-900">${o.subtotal.toFixed(2)}</p>
                    <Badge status={o.status} />
                  </div>
                </div>
              </button>
            ))}
            {billable.length === 0 && (
              <p className="text-sm text-slate-400 text-center py-6">No orders ready to bill</p>
            )}
          </div>
        </div>

        {/* Bill generator */}
        <div className="card p-5">
          <h3 className="font-semibold text-slate-800 mb-4">Bill Generator</h3>
          {!selected ? (
            <p className="text-sm text-slate-400 py-8 text-center">Select an order on the left</p>
          ) : (
            <div className="space-y-4">
              {/* Pricing strategy (Strategy Pattern) */}
              <div>
                <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2 block">
                  Pricing Strategy
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {STRATEGIES.map(s => (
                    <button key={s.key} onClick={() => setConfig(c => ({ ...c, strategy: s.key }))}
                      className={clsx(
                        'p-3 rounded-xl border text-left transition-all',
                        config.strategy === s.key
                          ? 'border-brand-400 bg-brand-50'
                          : 'border-slate-200 hover:border-slate-300'
                      )}>
                      <p className="text-xs font-semibold text-slate-800">{s.label}</p>
                      <p className="text-xs text-slate-500">{s.desc}</p>
                      {s.discount > 0 && (
                        <p className="text-xs font-bold text-emerald-600 mt-0.5">-{s.discount}%</p>
                      )}
                    </button>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Tip (%)</label>
                  <select className="select mt-1" value={config.tip}
                    onChange={e => setConfig(c => ({ ...c, tip: +e.target.value }))}>
                    {[0,5,10,15,20].map(t => <option key={t} value={t}>{t}%</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Split</label>
                  <div className="flex items-center gap-2 mt-1">
                    <Split size={14} className="text-slate-400" />
                    <input className="input py-1.5" type="number" min={1} max={20}
                      value={config.split} onChange={e => setConfig(c => ({ ...c, split: +e.target.value }))} />
                  </div>
                </div>
              </div>

              <button onClick={() => generateBill(selected)} className="btn-primary w-full justify-center">
                <Receipt size={15} /> Generate Bill
              </button>

              {/* Generated bill */}
              {generated && (
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                  <div className="flex justify-between text-sm text-slate-600">
                    <span>Subtotal</span><span>${generated.subtotal.toFixed(2)}</span>
                  </div>
                  {generated.discount > 0 && (
                    <div className="flex justify-between text-sm text-emerald-600">
                      <span>Discount ({generated.strategy})</span><span>-${generated.discount.toFixed(2)}</span>
                    </div>
                  )}
                  <div className="flex justify-between text-sm text-slate-600">
                    <span>Tax (12%)</span><span>${generated.tax.toFixed(2)}</span>
                  </div>
                  {generated.tip > 0 && (
                    <div className="flex justify-between text-sm text-slate-600">
                      <span>Tip ({config.tip}%)</span><span>${generated.tip.toFixed(2)}</span>
                    </div>
                  )}
                  <div className="flex justify-between font-bold text-slate-900 pt-2 border-t border-slate-200">
                    <span>Total</span><span>${generated.total.toFixed(2)}</span>
                  </div>
                  {generated.split > 1 && (
                    <div className="flex justify-between text-sm text-brand-600 font-semibold">
                      <span>Per person (÷{generated.split})</span><span>${generated.per_person.toFixed(2)}</span>
                    </div>
                  )}
                  <button onClick={payBill} className="btn-primary w-full justify-center mt-2">
                    <CreditCard size={15} /> Mark as Paid
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Paid bills history */}
      {bills.length > 0 && (
        <div className="card p-5">
          <h3 className="font-semibold text-slate-800 mb-4">Paid Bills</h3>
          <table className="w-full">
            <thead className="bg-slate-50">
              <tr>
                <th className="table-th">Bill ID</th>
                <th className="table-th">Table</th>
                <th className="table-th">Strategy</th>
                <th className="table-th">Total</th>
                <th className="table-th">Split</th>
                <th className="table-th">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {bills.map(b => (
                <tr key={b.id} className="hover:bg-slate-50">
                  <td className="table-td font-mono text-xs text-slate-500">#{b.id.slice(-6)}</td>
                  <td className="table-td">T{b.table_id}</td>
                  <td className="table-td text-sm">{b.strategy}</td>
                  <td className="table-td font-bold">${b.total.toFixed(2)}</td>
                  <td className="table-td text-slate-500">{b.split > 1 ? `÷${b.split} = $${b.per_person}` : '—'}</td>
                  <td className="table-td"><Badge status="served" label="Paid" /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
