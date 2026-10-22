import { orderSubtotal, SAMPLE_MENU } from "./RestaurantPOS";
import type { MenuItem } from "./RestaurantPOS";

function assertEqual(actual: number, expected: number, label: string): void {
  if (actual !== expected) throw new Error(`${label}: expected ${expected}, received ${actual}`);
}

export function runRestaurantPOSTests(): void {
  assertEqual(orderSubtotal([], SAMPLE_MENU), 0, "empty order");
  assertEqual(orderSubtotal([{ itemId: "taco", quantity: 2 }, { itemId: "tea", quantity: 1 }], SAMPLE_MENU), 2497, "multi-item order");
  assertEqual(orderSubtotal([{ itemId: "missing", quantity: 5 }], SAMPLE_MENU), 0, "unknown item");
  assertEqual(orderSubtotal([{ itemId: "taco", quantity: -1 }], SAMPLE_MENU), 0, "negative quantity");
  assertEqual(orderSubtotal([{ itemId: "taco", quantity: 1.5 }], SAMPLE_MENU), 0, "fractional quantity");
  const expensive: MenuItem[] = [{ id: "x", name: "Item", category: "Test", priceCents: 1999, available: true }];
  assertEqual(orderSubtotal([{ itemId: "x", quantity: 3 }], expensive), 5997, "integer cents");
}
