import { useLocation } from 'react-router-dom'
import { Search, User } from 'lucide-react'

const TITLES = {
  '/':         'Dashboard',
  '/tables':   'Tables',
  '/orders':   'Orders',
  '/kitchen':  'Kitchen Queue',
  '/menu':     'Menu',
  '/billing':  'Billing',
}

export default function Topbar() {
  const { pathname } = useLocation()
  const key = Object.keys(TITLES).filter(k => k !== '/').find(k => pathname.startsWith(k)) || '/'
  const title = TITLES[key]
  const now = new Date().toLocaleDateString('en-GB', { weekday:'long', day:'numeric', month:'long' })

  return (
    <header className="h-14 bg-white border-b border-slate-200 flex items-center px-6 gap-4 sticky top-0 z-20">
      <div className="flex-1">
        <h1 className="font-display text-slate-900 text-xl leading-none">{title}</h1>
        <p className="text-slate-400 text-xs mt-0.5">{now}</p>
      </div>

      {/* Search */}
      <div className="relative hidden sm:block">
        <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          type="text"
          placeholder="Search…"
          className="pl-8 pr-4 py-1.5 rounded-lg border border-slate-200 text-sm bg-slate-50 
                     focus:outline-none focus:ring-2 focus:ring-brand-400 focus:bg-white w-52 transition-all"
        />
      </div>

      {/* Avatar */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-full bg-brand-500 flex items-center justify-center">
          <User size={14} className="text-white" />
        </div>
        <div className="hidden sm:block">
          <p className="text-xs font-semibold text-slate-800 leading-none">Manager</p>
          <p className="text-xs text-slate-400 mt-0.5">Admin</p>
        </div>
      </div>
    </header>
  )
}
