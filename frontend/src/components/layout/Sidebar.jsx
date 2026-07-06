import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, Grid3X3, ShoppingCart,
  ChefHat, BookOpen, Receipt, LogOut,
  UtensilsCrossed, Bell,
} from 'lucide-react'
import clsx from 'clsx'

const NAV = [
  { to: '/',            icon: LayoutDashboard, label: 'Dashboard'    },
  { to: '/tables',      icon: Grid3X3,         label: 'Tables'       },
  { to: '/orders',      icon: ShoppingCart,    label: 'Orders'       },
  { to: '/kitchen',     icon: ChefHat,         label: 'Kitchen'      },
  { to: '/menu',        icon: BookOpen,        label: 'Menu'         },
  { to: '/billing',     icon: Receipt,         label: 'Billing'      },
]

export default function Sidebar() {
  const { pathname } = useLocation()

  return (
    <aside className="fixed inset-y-0 left-0 w-56 bg-slate-900 flex flex-col z-30">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-brand-500 flex items-center justify-center shadow-lg">
            <UtensilsCrossed size={18} className="text-white" />
          </div>
          <div>
            <p className="font-display text-white text-lg leading-tight">BitePlate</p>
            <p className="text-slate-500 text-xs">Restaurant OS</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {NAV.map(({ to, icon: Icon, label }) => {
          const active = to === '/' ? pathname === '/' : pathname.startsWith(to)
          return (
            <NavLink
              key={to}
              to={to}
              className={clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150',
                active ? 'nav-item-active' : 'nav-item'
              )}
            >
              <Icon size={17} />
              {label}
            </NavLink>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="px-3 py-4 border-t border-white/10 space-y-1">
        <button className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/10 transition-all">
          <Bell size={17} />
          Notifications
          <span className="ml-auto bg-brand-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">3</span>
        </button>
        <button className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-all">
          <LogOut size={17} />
          Sign Out
        </button>
      </div>
    </aside>
  )
}
