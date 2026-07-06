export const mockTables = [
  { id: '1', number: 1, capacity: 2, status: 'free',     location: 'Window' },
  { id: '2', number: 2, capacity: 4, status: 'occupied', location: 'Window' },
  { id: '3', number: 3, capacity: 4, status: 'reserved', location: 'Center' },
  { id: '4', number: 4, capacity: 6, status: 'free',     location: 'Center' },
  { id: '5', number: 5, capacity: 8, status: 'awaiting_bill', location: 'Terrace' },
  { id: '6', number: 6, capacity: 2, status: 'free',     location: 'Bar' },
  { id: '7', number: 7, capacity: 4, status: 'occupied', location: 'Center' },
  { id: '8', number: 8, capacity: 4, status: 'free',     location: 'Terrace' },
]

export const mockOrders = [
  { id: 'ord-001', table_id: '2', status: 'in_kitchen',  subtotal: 67.50, created_at: new Date(Date.now()-1800000).toISOString(), items: [{ menu_item_name: 'Grilled Salmon', quantity: 2, line_total: 44.00 }, { menu_item_name: 'Caesar Salad', quantity: 1, line_total: 9.00 }] },
  { id: 'ord-002', table_id: '5', status: 'awaiting_bill', subtotal: 112.00, created_at: new Date(Date.now()-3600000).toISOString(), items: [{ menu_item_name: 'Beef Burger', quantity: 3, line_total: 55.50 }, { menu_item_name: 'Fresh OJ', quantity: 4, line_total: 20.00 }] },
  { id: 'ord-003', table_id: '7', status: 'confirmed',   subtotal: 34.00, created_at: new Date(Date.now()-600000).toISOString(),  items: [{ menu_item_name: 'Margherita Pizza', quantity: 2, line_total: 32.00 }] },
]

export const mockKitchenTickets = [
  { id: 'kt-001', order_id: 'ord-001', item_name: 'Grilled Salmon', quantity: 2, station: 'hot_kitchen', status: 'preparing', created_at: new Date(Date.now()-900000).toISOString(), special_notes: 'Medium rare' },
  { id: 'kt-002', order_id: 'ord-001', item_name: 'Caesar Salad',   quantity: 1, station: 'cold_kitchen', status: 'queued',    created_at: new Date(Date.now()-900000).toISOString(), special_notes: '' },
  { id: 'kt-003', order_id: 'ord-003', item_name: 'Margherita Pizza', quantity: 2, station: 'pizza_oven', status: 'queued',   created_at: new Date(Date.now()-300000).toISOString(), special_notes: 'Extra basil' },
]

export const mockMenuItems = [
  { id: 'm-001', name: 'Tomato Bruschetta',  category: 'starter',  base_price: 7.50,  is_available: true, allergens: ['gluten'] },
  { id: 'm-002', name: 'Caesar Salad',       category: 'starter',  base_price: 9.00,  is_available: true, allergens: ['dairy','gluten'] },
  { id: 'm-003', name: 'Grilled Salmon',     category: 'main',     base_price: 22.00, is_available: true, allergens: ['fish'] },
  { id: 'm-004', name: 'Beef Burger',        category: 'main',     base_price: 18.50, is_available: true, allergens: ['gluten','dairy'] },
  { id: 'm-005', name: 'Margherita Pizza',   category: 'main',     base_price: 16.00, is_available: true, allergens: ['gluten','dairy'] },
  { id: 'm-006', name: 'Choco Lava Cake',    category: 'dessert',  base_price: 8.50,  is_available: true, allergens: ['dairy','eggs'] },
  { id: 'm-007', name: 'Still Water 500ml',  category: 'beverage', base_price: 2.50,  is_available: true, allergens: [] },
  { id: 'm-008', name: 'Fresh Orange Juice', category: 'beverage', base_price: 5.00,  is_available: true, allergens: [] },
]

export const mockStats = {
  totalRevenue: 4280.50,
  ordersToday:  34,
  tablesOccupied: 3,
  totalTables: 8,
  avgOrderValue: 125.90,
  revenueByHour: [
    { hour: '11:00', revenue: 120 },
    { hour: '12:00', revenue: 480 },
    { hour: '13:00', revenue: 620 },
    { hour: '14:00', revenue: 390 },
    { hour: '15:00', revenue: 210 },
    { hour: '16:00', revenue: 180 },
    { hour: '17:00', revenue: 290 },
    { hour: '18:00', revenue: 540 },
    { hour: '19:00', revenue: 680 },
    { hour: '20:00', revenue: 520 },
    { hour: '21:00', revenue: 250 },
  ],
  ordersByStatus: [
    { status: 'Served',      count: 28 },
    { status: 'In Kitchen',  count: 3  },
    { status: 'Confirmed',   count: 2  },
    { status: 'Cancelled',   count: 1  },
  ],
}
