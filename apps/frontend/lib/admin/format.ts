import type {Order, User} from "@/lib/shared/types";

export function userRow(user: User): Record<string, unknown> {
  return {
    id: user.id,
    email: user.email,
    role: user.role,
    status: user.status,
    tier: user.tier,
    locale: user.locale,
    max_orders_per_minute: user.limit?.max_orders_per_minute ?? "-",
    max_orders_per_day: user.limit?.max_orders_per_day ?? "-",
    max_active_orders: user.limit?.max_active_orders ?? "-",
    max_daily_spend: user.limit?.max_daily_spend ?? "-",
    balance: user.wallet?.balance ?? "0.0000",
    held_balance: user.wallet?.held_balance ?? "0.0000",
    currency: user.wallet?.currency ?? "USD",
    api_key_status: user.api_key_enabled ? "enabled" : "not generated",
    created_at: user.created_at
  };
}

export function orderProfit(order: Order) {
  return Number(order.price || 0) - Number(order.provider_cost || 0);
}
