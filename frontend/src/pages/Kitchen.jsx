import { useState } from 'react'
import { ChefHat, Clock, CheckCircle, XCircle, RotateCcw, Flame } from 'lucide-react'
import { Badge, PageHeader, EmptyState } from '../components/ui/index'
import { mockKitchenTickets } from '../services/mockData'
import clsx from 'clsx'

const STATION_COLORS = {
  hot_kitchen:  'bg-red-100 text-red-700 border-red-200',
  cold_kitchen: 'bg-sky-100 text-sky-700 border-sky-200',
  pizza_oven:   'bg-orange-100 text-orange-700 border-orange-200',
  bar:          'bg-purple-100 text-purple-700 border-purple-200',
  pastry:       'bg-pink-100 text-pink-700 border-pink-200',
  grill:        'bg-amber-100 text-amber-700 border-amber-200',
}

export default function Kitchen() {
  const [tickets, setTickets] = useState(mockKitchenTickets)
  const [history, setHistory] = useState([])

  function execute(id, action) {
    const next = { prepare: 'preparing', ready: 'ready', cancel: 'cancelled' }
    setTickets(ts => {
      const ticket = ts.find(t => t.id === id)
      if (ticket) setHistory(h => [{ ...ticket, prevStatus: ticket.status }, ...h])
      return ts.map(t => t.id === id ? { ...t, status: next[action] || t.status } : t)
    })
  }

  function undoLast() {
    if (!history.length) return
    const last = history[0]
    setTickets(ts => ts.map(t => t.id === last.id ? { ...t, status: last.prevStatus } : t))
    setHistory(h => h.slice(1))
  }

  const grouped = {
    queued:    tickets.filter(t => t.status === 'queued'),
    preparing: tickets.filter(t => t.status === 'preparing'),
    ready:     tickets.filter(t => t.status === 'ready'),
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Kitchen Queue"
        subtitle={`${grouped.queued.length} queued · ${grouped.preparing.length} preparing · ${grouped.ready.length} ready`}
        action={
          <button onClick={undoLast} disabled={!history.length}
            className={clsx('btn-secondary', !history.length && 'opacity-40 cursor-not-allowed')}>
            <RotateCcw size={14} /> Undo Last
          </button>
        }
      />

      {/* Command Pattern note */}
      <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-700 flex items-center gap-2">
        <Flame size={13} />
        <span><strong>Command Pattern:</strong> Each action (Prepare, Ready, Cancel) is a Command with execute() + undo() support.</span>
      </div>

      {/* Kanban columns */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { key: 'queued',    label: 'Queued',    color: 'border-slate-300',  badge: 'bg-slate-100 text-slate-600' },
          { key: 'preparing', label: 'Preparing', color: 'border-orange-300', badge: 'bg-orange-100 text-orange-700' },
          { key: 'ready',     label: 'Ready',     color: 'border-emerald-300',badge: 'bg-emerald-100 text-emerald-700' },
        ].map(col => (
          <div key={col.key} className={clsx('card border-t-4', col.color)}>
            <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
              <h3 className="font-semibold text-slate-700 text-sm">{col.label}</h3>
              <span className={clsx('badge', col.badge)}>{grouped[col.key].length}</span>
            </div>
            <div className="p-3 space-y-3 min-h-32">
              {grouped[col.key].length === 0 && (
                <p className="text-xs text-slate-400 text-center py-4">No tickets</p>
              )}
              {grouped[col.key].map(t => (
                <TicketCard key={t.id} ticket={t} onAction={execute} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function TicketCard({ ticket: t, onAction }) {
  const elapsed = Math.round((Date.now() - new Date(t.created_at)) / 60000)
  const urgent  = elapsed > 15

  return (
    <div className={clsx(
      'rounded-xl border p-3 bg-white transition-all hover:shadow-md',
      urgent ? 'border-red-200' : 'border-slate-200'
    )}>
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <p className="font-semibold text-slate-800 text-sm">{t.item_name}</p>
          <p className="text-xs text-slate-400">×{t.quantity} · Order #{t.order_id.slice(-3)}</p>
        </div>
        <span className={clsx(
          'badge border text-xs capitalize',
          STATION_COLORS[t.station] || 'bg-slate-100 text-slate-600 border-slate-200'
        )}>
          {t.station.replace('_', ' ')}
        </span>
      </div>

      {t.special_notes && (
        <p className="text-xs text-amber-700 bg-amber-50 rounded px-2 py-1 mb-2">
          📝 {t.special_notes}
        </p>
      )}

      <div className="flex items-center justify-between">
        <span className={clsx('flex items-center gap-1 text-xs', urgent ? 'text-red-500 font-semibold' : 'text-slate-400')}>
          <Clock size={11} /> {elapsed}m {urgent && '⚠️'}
        </span>
        <div className="flex gap-1">
          {t.status === 'queued' && (
            <button onClick={() => onAction(t.id, 'prepare')}
              className="px-2 py-1 rounded-lg bg-orange-100 text-orange-700 text-xs font-semibold hover:bg-orange-200 transition-colors">
              Prepare
            </button>
          )}
          {t.status === 'preparing' && (
            <button onClick={() => onAction(t.id, 'ready')}
              className="px-2 py-1 rounded-lg bg-emerald-100 text-emerald-700 text-xs font-semibold hover:bg-emerald-200 transition-colors">
              Ready ✓
            </button>
          )}
          {['queued','preparing'].includes(t.status) && (
            <button onClick={() => onAction(t.id, 'cancel')}
              className="px-2 py-1 rounded-lg bg-red-50 text-red-600 text-xs font-semibold hover:bg-red-100 transition-colors">
              ✕
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
