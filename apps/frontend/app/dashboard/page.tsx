"use client";

import Link from "next/link";
import {useEffect, useState} from "react";
import {DataTable} from "@/components/shared/data-table";
import {ActionLink, Alert, Card, MetricCard, PageHeader, PageShell, StatusBadge} from "@/components/shared/ui";
import {OnboardingChecklist} from "@/components/client/onboarding-checklist";
import {getBalance, getLimits, listOrders} from "@/lib/client/api";
import {currentUser} from "@/lib/shared/api";
import {dateTime, money} from "@/lib/shared/format";
import type {Order, User, UserLimit, Wallet} from "@/lib/shared/types";
import {useTranslation} from "@/lib/i18n";

export default function DashboardPage() {
  const {t} = useTranslation();
  const [user, setUser] = useState<User | null>(null);
  const [balance, setBalance] = useState<Wallet | null>(null);
  const [limits, setLimits] = useState<UserLimit | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    Promise.all([
      currentUser(),
      getBalance(),
      getLimits(),
      listOrders()
    ])
      .then(([userData, balanceData, limitsData, orderData]) => {
        setUser(userData);
        setBalance(balanceData);
        setLimits(limitsData);
        setOrders(orderData);
      })
      .catch((err) => setError(err instanceof Error ? err.message : t("buy.loadFailed")));
  }

  useEffect(() => {
    load();
    window.addEventListener("smsbridge-data-changed", load);
    return () => window.removeEventListener("smsbridge-data-changed", load);
  }, []);

  const activeOrders = orders.filter((order) => ["created", "reserved", "waiting_sms", "sms_received"].includes(order.status)).length;
  const completedOrders = orders.filter((order) => order.status === "completed").length;

  return (
    <PageShell>
      <PageHeader
        title={t("dashboard.title")}
        description={t("dashboard.description")}
        actions={<><Link className="btn btn-primary" href="/buy">{t("dashboard.buyNumber")}</Link><ActionLink href="/orders">{t("dashboard.viewOrders")}</ActionLink></>}
      />
      {error && <div className="mt-4"><Alert type="error">{error}</Alert></div>}
      <section className="mt-6 grid gap-4 md:grid-cols-3 xl:grid-cols-6">
        <MetricCard label={t("common.availableBalance")} value={money(balance?.balance, balance?.currency)} helper={t("dashboard.availableHelper")} />
        <MetricCard label={t("common.heldBalance")} value={money(balance?.held_balance, balance?.currency)} helper={t("dashboard.heldHelper")} />
        <MetricCard label={t("dashboard.accountTier")} value={user?.tier || "-"} helper={t("settings.limitsDesc")} />
        <MetricCard label={t("dashboard.dailyLimit")} value={limits?.max_orders_per_day ?? "-"} helper={t("dashboard.maxOrdersDay")} />
        <MetricCard label={t("dashboard.activeOrders")} value={activeOrders} helper={t("status.waiting_sms")} />
        <MetricCard label={t("dashboard.completed")} value={completedOrders} helper={t("dashboard.recentHistory")} />
      </section>

      <section className="mt-6 grid gap-4 lg:grid-cols-[0.8fr_1.2fr]">
        <Card title={t("dashboard.checklist")} description={user?.role === "admin" ? t("dashboard.adminChecklistDesc") : t("dashboard.userChecklistDesc")}>
          <OnboardingChecklist role={user?.role} />
        </Card>
        <Card title={t("dashboard.quickActions")} description={t("dashboard.quickActionsDesc")}>
          <div className="flex flex-wrap gap-2">
            <Link className="btn btn-primary" href="/buy">{t("dashboard.buyNumber")}</Link>
            <Link className="btn btn-secondary" href="/orders">{t("dashboard.viewOrders")}</Link>
            <Link className="btn btn-secondary" href="/api-docs">{t("nav.api")}</Link>
            <Link className="btn btn-secondary" href="/settings">{t("nav.settings")}</Link>
          </div>
        </Card>
      </section>

      <section className="mt-8">
        <Card title={t("dashboard.recentOrders")} description={t("dashboard.recentOrdersDesc")}>
          <DataTable
            rows={orders.slice(0, 5) as unknown as Record<string, unknown>[]}
            emptyTitle={t("dashboard.noOrders")}
            emptyDescription={t("dashboard.noOrdersDesc")}
            columns={[
              {key: "public_id", header: t("common.order"), render: (row) => <Link className="text-accent" href={`/orders/${row.public_id}`}>{String(row.public_id).slice(0, 8)}</Link>},
              {key: "service_code", header: t("common.service")},
              {key: "country_iso2", header: t("common.country")},
              {key: "status", header: t("common.status"), render: (row) => <StatusBadge status={String(row.status)} />},
              {key: "price", header: t("common.price"), render: (row) => money(row.price)},
              {key: "created_at", header: t("common.created"), render: (row) => dateTime(row.created_at)}
            ]}
          />
        </Card>
      </section>
    </PageShell>
  );
}
