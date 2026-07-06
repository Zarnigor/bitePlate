import { useState } from 'react'
import { Grid3X3, Users, Plus } from 'lucide-react'
import { Badge, PageHeader, Modal } from '../components/ui/index'
import { mockTables } from '../services/mockData'
import clsx from 'clsx'

const STATUS_BG = {
  free:          'border-emerald-300 bg-emerald-50 hover:bg-emerald-100',
  reserved:      'border-amber-300  bg-amber-50  hover:bg-amber-100',
  occupied:      'border-blue-300   bg-blue-50   hover:bg-blue-100',
  awaiting_bill: 'border-purple-300 bg-purple-50 hover:bg-purple-100',
  cleared:       'border-slate-200  bg-slate-50  hover:bg-slate-100',
}

const ACTIONS = {
  free:          ['reserve', 'seat'],
  reserved:      ['seat', 'clear'],
  occupied:      ['request_bill', 'clear'],
  awaiting_bill: ['clear'],
  cleared:       ['free'],
}

const ACTION_LABELS = {
  reserve:      { label: 'Reserve',      color: 'btn-secondary' },
  seat:         { label: 'Seat Guests',  color: 'btn-primary' },
  request_bill: { label: 'Request Bill', color: 'btn-secondary' },
  clear:        { label: 'Clear Table',  color: 'btn-secondary' },
  free:         { label: 'Mark Free',    color: 'btn-secondary' },
}

export default function Tables() {
  const [tables, setTables]   = useState(mockTables)
  const [selected, setSelected] = useState(null)
  const [showAdd, setShowAdd]   = useState(false)
  const [newTable, setNewTable] = useState({ number: '', capacity: 4, location: '' })

  const counts = {
    free:     tables.filter(t => t.status === 'free').length,
    occupied: tables.filter(t => t.status === 'occupied').length,
    reserved: tables.filter(t => t.status === 'reserved').length,
  }

  function handleAction(tableId, action) {
    const next = {
      reserve: 'reserved', seat: 'occupied',
      request_bill: 'awaiting_bill', clear: 'free', free: 'free',
    }
    setTables(ts => ts.map(t => t.id === tableId ? { ...t, status: next[action] || t.status } : t))
    setSelected(null)
  }

  function handleAdd() {
    if (!newTable.number) return
    setTables(ts => [...ts, { ...newTable, id: Date.now().toString(), status: 'free' }])
    setNewTable({ number: '', capacity: 4, location: '' })
    setShowAdd(false)
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Tables"
        subtitle={`${counts.free} free · ${counts.occupied} occupied · ${counts.reserved} reserved`}
        action={
          <button onClick={() => setShowAdd(true)} className="btn-primary">
            <Plus size={15} /> Add Table
          </button>
        }
      />

      {/* Summary */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: 'Free',     count: counts.free,     color: 'bg-emerald-500' },
          { label: 'Occupied', count: counts.occupied, color: 'bg-blue-500' },
          { label: 'Reserved', count: counts.reserved, color: 'bg-amber-500' },
        ].map(s => (
          <div key={s.label} className="card px-4 py-3 flex items-center gap-3">
            <div className={clsx('w-3 h-3 rounded-full', s.color)} />
            <span className="text-sm text-slate-600">{s.label}</span>
            <span className="ml-auto font-bold text-slate-900">{s.count}</span>
          </div>
        ))}
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {tables.map(t => (
          <button
            key={t.id}
            onClick={() => setSelected(t)}
            className={clsx(
              'card p-4 text-left border-2 cursor-pointer transition-all duration-150 hover:shadow-card-hover',
              STATUS_BG[t.status] || 'border-slate-200 bg-white hover:bg-slate-50'
            )}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="w-10 h-10 rounded-xl bg-white/70 border border-white/50 flex items-center justify-center shadow-sm">
                <Grid3X3 size={18} className="text-slate-600" />
              </div>
              <Badge status={t.status} />
            </div>
            <p className="font-display text-2xl text-slate-900">{t.number}</p>
            <div className="flex items-center gap-1 mt-1 text-xs text-slate-500">
              <Users size={11} /> {t.capacity} seats · {t.location}
            </div>
          </button>
        ))}
      </div>

      {/* Table detail modal */}
      <Modal
        open={!!selected}
        onClose={() => setSelected(null)}
        title={`Table ${selected?.number}`}
        footer={
          <button onClick={() => setSelected(null)} className="btn-secondary">Close</button>
        }
      >
        {selected && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-50">
              <Users size={16} className="text-slate-500" />
              <span className="text-sm text-slate-700">{selected.capacity} seats · {selected.location}</span>
              <Badge status={selected.status} className="ml-auto" />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Actions</p>
              <div className="flex flex-wrap gap-2">
                {(ACTIONS[selected.status] || []).map(a => (
                  <button
                    key={a}
                    onClick={() => handleAction(selected.id, a)}
                    className={ACTION_LABELS[a]?.color || 'btn-secondary'}
                  >
                    {ACTION_LABELS[a]?.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </Modal>

      {/* Add table modal */}
      <Modal
        open={showAdd}
        onClose={() => setShowAdd(false)}
        title="Add New Table"
        footer={
          <>
            <button onClick={() => setShowAdd(false)} className="btn-secondary">Cancel</button>
            <button onClick={handleAdd} className="btn-primary">Add Table</button>
          </>
        }
      >
        <div className="space-y-3">
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Table Number</label>
            <input className="input mt-1" type="number" placeholder="e.g. 9"
              value={newTable.number} onChange={e => setNewTable(n => ({ ...n, number: e.target.value }))} />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Capacity</label>
            <select className="select mt-1"
              value={newTable.capacity} onChange={e => setNewTable(n => ({ ...n, capacity: +e.target.value }))}>
              {[2,4,6,8,10].map(c => <option key={c} value={c}>{c} seats</option>)}
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Location</label>
            <input className="input mt-1" placeholder="e.g. Window, Terrace"
              value={newTable.location} onChange={e => setNewTable(n => ({ ...n, location: e.target.value }))} />
          </div>
        </div>
      </Modal>
    </div>
  )
}
