import { useState } from 'react'
import { BookOpen, Plus, ToggleLeft, ToggleRight, Search } from 'lucide-react'
import { Badge, PageHeader, Modal, EmptyState } from '../components/ui/index'
import { mockMenuItems } from '../services/mockData'
import clsx from 'clsx'

const CATEGORIES = ['all', 'starter', 'main', 'dessert', 'beverage']

export default function Menu() {
  const [items, setItems]     = useState(mockMenuItems)
  const [cat, setCat]         = useState('all')
  const [search, setSearch]   = useState('')
  const [showAdd, setShowAdd] = useState(false)
  const [newItem, setNewItem] = useState({ name:'', category:'main', base_price:'', description:'' })

  const filtered = items.filter(i =>
    (cat === 'all' || i.category === cat) &&
    i.name.toLowerCase().includes(search.toLowerCase())
  )

  function toggleAvail(id) {
    setItems(is => is.map(i => i.id === id ? { ...i, is_available: !i.is_available } : i))
  }

  function addItem() {
    if (!newItem.name || !newItem.base_price) return
    setItems(is => [...is, { ...newItem, id: 'm-' + Date.now(), is_available: true, allergens: [], base_price: +newItem.base_price }])
    setNewItem({ name:'', category:'main', base_price:'', description:'' })
    setShowAdd(false)
  }

  const counts = Object.fromEntries(
    ['starter','main','dessert','beverage'].map(c => [c, items.filter(i => i.category === c).length])
  )

  return (
    <div className="space-y-6">
      <PageHeader
        title="Menu"
        subtitle={`${items.filter(i=>i.is_available).length} available items`}
        action={
          <button onClick={() => setShowAdd(true)} className="btn-primary">
            <Plus size={15} /> Add Item
          </button>
        }
      />

      {/* Category tabs */}
      <div className="flex items-center gap-3 flex-wrap">
        <div className="relative">
          <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input className="input pl-8 w-44 py-1.5" placeholder="Search menu…"
            value={search} onChange={e => setSearch(e.target.value)} />
        </div>
        {CATEGORIES.map(c => (
          <button key={c} onClick={() => setCat(c)}
            className={clsx(
              'px-3 py-1.5 rounded-lg text-xs font-semibold capitalize transition-all',
              cat === c ? 'bg-brand-500 text-white' : 'bg-white text-slate-500 border border-slate-200 hover:bg-slate-50'
            )}>
            {c}{c !== 'all' && <span className="ml-1 opacity-60">{counts[c]}</span>}
          </button>
        ))}
      </div>

      {/* Items grid */}
      {filtered.length === 0 ? (
        <EmptyState icon={BookOpen} title="No items found" description="Try changing the filter or search." />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map(item => (
            <div key={item.id}
              className={clsx('card p-4 transition-all hover:shadow-card-hover', !item.is_available && 'opacity-60')}>
              {/* Category color bar */}
              <div className={clsx('h-1 rounded-full mb-3', {
                'bg-sky-400': item.category === 'starter',
                'bg-blue-500': item.category === 'main',
                'bg-pink-400': item.category === 'dessert',
                'bg-teal-400': item.category === 'beverage',
              })} />
              <div className="flex items-start justify-between gap-2 mb-2">
                <h4 className="font-semibold text-slate-800 text-sm leading-snug">{item.name}</h4>
                <Badge status={item.category} />
              </div>
              <p className="text-xl font-bold text-brand-600 font-mono mb-2">${item.base_price.toFixed(2)}</p>
              {item.allergens.length > 0 && (
                <div className="flex flex-wrap gap-1 mb-3">
                  {item.allergens.map(a => (
                    <span key={a} className="text-xs bg-amber-50 text-amber-700 border border-amber-200 rounded px-1.5 py-0.5">
                      ⚠️ {a}
                    </span>
                  ))}
                </div>
              )}
              <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                <span className={clsx('text-xs font-medium', item.is_available ? 'text-emerald-600' : 'text-slate-400')}>
                  {item.is_available ? 'Available' : 'Unavailable'}
                </span>
                <button onClick={() => toggleAvail(item.id)} className="text-slate-400 hover:text-brand-500 transition-colors">
                  {item.is_available ? <ToggleRight size={22} className="text-emerald-500" /> : <ToggleLeft size={22} />}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add item modal */}
      <Modal open={showAdd} onClose={() => setShowAdd(false)} title="Add Menu Item"
        footer={
          <>
            <button onClick={() => setShowAdd(false)} className="btn-secondary">Cancel</button>
            <button onClick={addItem} className="btn-primary">Add Item</button>
          </>
        }>
        <div className="space-y-3">
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Name</label>
            <input className="input mt-1" placeholder="e.g. Grilled Salmon"
              value={newItem.name} onChange={e => setNewItem(n => ({ ...n, name: e.target.value }))} />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Category</label>
            <select className="select mt-1" value={newItem.category}
              onChange={e => setNewItem(n => ({ ...n, category: e.target.value }))}>
              {['starter','main','dessert','beverage'].map(c => (
                <option key={c} value={c} className="capitalize">{c.charAt(0).toUpperCase()+c.slice(1)}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Price ($)</label>
            <input className="input mt-1" type="number" step="0.50" placeholder="0.00"
              value={newItem.base_price} onChange={e => setNewItem(n => ({ ...n, base_price: e.target.value }))} />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Description</label>
            <input className="input mt-1" placeholder="Short description…"
              value={newItem.description} onChange={e => setNewItem(n => ({ ...n, description: e.target.value }))} />
          </div>
        </div>
      </Modal>
    </div>
  )
}
