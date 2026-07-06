import clsx from 'clsx'

// ── Badge ─────────────────────────────────────────────────────
const STATUS_STYLES = {
  free:          'bg-emerald-100 text-emerald-700',
  reserved:      'bg-amber-100  text-amber-700',
  occupied:      'bg-blue-100   text-blue-700',
  awaiting_bill: 'bg-purple-100 text-purple-700',
  cleared:       'bg-slate-100  text-slate-500',
  draft:         'bg-slate-100  text-slate-500',
  confirmed:     'bg-sky-100    text-sky-700',
  in_kitchen:    'bg-orange-100 text-orange-700',
  served:        'bg-emerald-100 text-emerald-700',
  cancelled:     'bg-red-100    text-red-600',
  closed:        'bg-slate-100  text-slate-400',
  queued:        'bg-slate-100  text-slate-600',
  preparing:     'bg-orange-100 text-orange-700',
  ready:         'bg-emerald-100 text-emerald-700',
  starter:       'bg-sky-100    text-sky-700',
  main:          'bg-blue-100   text-blue-700',
  dessert:       'bg-pink-100   text-pink-700',
  beverage:      'bg-teal-100   text-teal-700',
}

export function Badge({ status, label, className }) {
  const text = label || status?.replace('_', ' ')
  return (
    <span className={clsx('badge capitalize', STATUS_STYLES[status] || 'bg-slate-100 text-slate-600', className)}>
      {text}
    </span>
  )
}

// ── Stat Card ─────────────────────────────────────────────────
export function StatCard({ title, value, subtitle, icon: Icon, color = 'brand', trend }) {
  const colorMap = {
    brand:   'from-brand-500 to-brand-400',
    green:   'from-emerald-500 to-emerald-400',
    blue:    'from-blue-500 to-blue-400',
    purple:  'from-violet-500 to-violet-400',
    amber:   'from-amber-500 to-amber-400',
  }
  return (
    <div className="card p-5 hover:shadow-card-hover transition-shadow duration-200">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</p>
          <p className="mt-1.5 text-2xl font-bold text-slate-900 font-mono">{value}</p>
          {subtitle && <p className="mt-0.5 text-xs text-slate-400">{subtitle}</p>}
          {trend && (
            <p className={clsx('mt-1 text-xs font-medium', trend > 0 ? 'text-emerald-600' : 'text-red-500')}>
              {trend > 0 ? '▲' : '▼'} {Math.abs(trend)}% vs yesterday
            </p>
          )}
        </div>
        {Icon && (
          <div className={clsx('w-10 h-10 rounded-xl bg-gradient-to-br flex items-center justify-center shadow-sm', colorMap[color])}>
            <Icon size={18} className="text-white" />
          </div>
        )}
      </div>
    </div>
  )
}

// ── Empty State ────────────────────────────────────────────────
export function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      {Icon && (
        <div className="w-14 h-14 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
          <Icon size={26} className="text-slate-400" />
        </div>
      )}
      <h3 className="text-slate-700 font-semibold text-base">{title}</h3>
      {description && <p className="text-slate-400 text-sm mt-1 max-w-xs">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}

// ── Modal ─────────────────────────────────────────────────────
export function Modal({ open, onClose, title, children, footer }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg animate-slide-up">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
          <h2 className="font-display text-lg text-slate-900">{title}</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 text-xl leading-none">×</button>
        </div>
        <div className="px-6 py-4">{children}</div>
        {footer && <div className="px-6 py-4 border-t border-slate-100 flex justify-end gap-3">{footer}</div>}
      </div>
    </div>
  )
}

// ── Loading Spinner ────────────────────────────────────────────
export function Spinner({ size = 5 }) {
  return (
    <div className={clsx(`w-${size} h-${size} border-2 border-slate-200 border-t-brand-500 rounded-full animate-spin`)} />
  )
}

// ── Page Header ────────────────────────────────────────────────
export function PageHeader({ title, subtitle, action }) {
  return (
    <div className="flex items-center justify-between mb-6">
      <div>
        <h2 className="text-2xl font-display text-slate-900">{title}</h2>
        {subtitle && <p className="text-sm text-slate-500 mt-0.5">{subtitle}</p>}
      </div>
      {action}
    </div>
  )
}
