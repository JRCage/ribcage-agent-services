"use client";
import { useMemo, useState } from "react";

export interface MenuItem { id: string; name: string; category: string; priceCents: number; available: boolean; }
export interface OrderLine { itemId: string; quantity: number; }
export const SAMPLE_MENU: MenuItem[] = [
  { id: "taco", name: "Street Tacos", category: "Mains", priceCents: 1099, available: true },
  { id: "bowl", name: "Rice Bowl", category: "Mains", priceCents: 1299, available: true },
  { id: "tea", name: "Iced Tea", category: "Drinks", priceCents: 299, available: true },
  { id: "cake", name: "Cake", category: "Desserts", priceCents: 599, available: false },
];
export function orderSubtotal(lines: OrderLine[], menu: MenuItem[]): number {
  return lines.reduce((total, line) => {
    const item = menu.find(entry => entry.id === line.itemId);
    if (!item || !Number.isSafeInteger(line.quantity) || line.quantity < 0) return total;
    return total + item.priceCents * line.quantity;
  }, 0);
}
const money = (cents: number) => (cents / 100).toLocaleString("en-US", { style: "currency", currency: "USD" });
export default function RestaurantPOS({ menu = SAMPLE_MENU }: { menu?: MenuItem[] }) {
  const [category, setCategory] = useState("All");
  const [cart, setCart] = useState<OrderLine[]>([]);
  const [message, setMessage] = useState("");
  const categories = useMemo(() => ["All", ...Array.from(new Set(menu.map(item => item.category)))], [menu]);
  const subtotal = orderSubtotal(cart, menu);
  const update = (id: string, delta: number) => {
    const item = menu.find(entry => entry.id === id);
    if (!item || !item.available) return;
    setCart(old => {
      const quantity = Math.max(0, Math.min(99, (old.find(line => line.itemId === id)?.quantity || 0) + delta));
      return [...old.filter(line => line.itemId !== id), ...(quantity ? [{ itemId: id, quantity }] : [])];
    });
    setMessage("");
  };
  const checkout = () => {
    if (!cart.length) { setMessage("Add an item before placing an order."); return; }
    setMessage("Demo order recorded locally. No payment was processed.");
    setCart([]);
  };
  return <main style={{ background: "#0A0A0A", color: "#F5F5F5", padding: 24, minHeight: "100vh", fontFamily: "Inter, sans-serif" }}>
    <h1>Restaurant POS</h1><p style={{ color: "#9CA3AF" }}>Sample interface — no live payment integration</p>
    <div aria-label="Menu categories" style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
      {categories.map(value => <button key={value} aria-pressed={category === value} onClick={() => setCategory(value)} style={{ padding: 10, background: category === value ? "#D4AF37" : "#141414", color: category === value ? "#0A0A0A" : "#F5F5F5", border: "1px solid #D4AF37", cursor: "pointer" }}>{value}</button>)}
    </div>
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 24, marginTop: 24 }}>
      <section aria-label="Menu"><h2>Menu</h2>{menu.filter(item => category === "All" || item.category === category).map(item =>
        <div key={item.id} style={{ border: "1px solid #2A2A2A", padding: 12, marginBottom: 8 }}>
          <strong>{item.name}</strong><p>{money(item.priceCents)} · {item.available ? "Available" : "Sold out"}</p>
          <button disabled={!item.available} onClick={() => update(item.id, 1)} style={{ padding: 8, cursor: item.available ? "pointer" : "not-allowed" }}>Add to order</button>
        </div>)}</section>
      <section aria-label="Current order"><h2>Current order</h2>
        {cart.length === 0 && <p>No items yet.</p>}
        {cart.map(line => { const item = menu.find(entry => entry.id === line.itemId); return item && <div key={line.itemId} style={{ padding: 8, borderBottom: "1px solid #2A2A2A" }}>
          <strong>{item.name}</strong> × {line.quantity} — {money(item.priceCents * line.quantity)}
          <div><button aria-label={`Remove one ${item.name}`} onClick={() => update(item.id, -1)}>−</button> <button aria-label={`Add one ${item.name}`} onClick={() => update(item.id, 1)}>+</button></div>
        </div>; })}
        <h3>Subtotal: {money(subtotal)}</h3><p>Tax, tips, and payment are not implemented.</p>
        <button onClick={checkout} style={{ padding: 12, background: "#D4AF37", color: "#0A0A0A", border: 0 }}>Record demo order</button>
        <p role="status" aria-live="polite">{message}</p>
      </section>
    </div>
  </main>;
}
