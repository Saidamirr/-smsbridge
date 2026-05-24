"use client";

import {useState} from "react";
import {Alert, Card, CopyButton, PageHeader, PageShell, Toast} from "@/components/shared/ui";
import {regenerateApiKey} from "@/lib/client/api";
import {useTranslation} from "@/lib/i18n";

const examples = {
  balance: `curl -H "Authorization: Bearer $SMSBRIDGE_API_KEY" \\
  http://localhost:8000/api/v1/balance`,
  prices: `curl -H "Authorization: Bearer $SMSBRIDGE_API_KEY" \\
  "http://localhost:8000/api/v1/prices?service_code=telegram&country_iso2=ID"`,
  create: `curl -X POST http://localhost:8000/api/v1/orders \\
  -H "Authorization: Bearer $SMSBRIDGE_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"service_code":"telegram","country_iso2":"ID"}'`,
  getOrder: `curl -H "Authorization: Bearer $SMSBRIDGE_API_KEY" \\
  http://localhost:8000/api/v1/orders/$ORDER_PUBLIC_ID`,
  cancel: `curl -X POST -H "Authorization: Bearer $SMSBRIDGE_API_KEY" \\
  http://localhost:8000/api/v1/orders/$ORDER_PUBLIC_ID/cancel`,
  finish: `curl -X POST -H "Authorization: Bearer $SMSBRIDGE_API_KEY" \\
  http://localhost:8000/api/v1/orders/$ORDER_PUBLIC_ID/finish`
};

export default function ApiDocsPage() {
  const {t} = useTranslation();
  const [apiKey, setApiKey] = useState("");
  const [toast, setToast] = useState<{type: "success" | "error"; message: string}>({type: "success", message: ""});

  async function regenerate() {
    setToast({type: "success", message: ""});
    try {
      const response = await regenerateApiKey();
      setApiKey(response.api_key);
      setToast({type: "success", message: t("api.generatedToast")});
    } catch (err) {
      setToast({type: "error", message: err instanceof Error ? err.message : t("api.generateFailed")});
    }
  }

  return (
    <PageShell>
      <Toast type={toast.type} message={toast.message} />
      <PageHeader
        title={t("api.title")}
        description={t("api.description")}
      />

      <section className="mt-6 grid gap-4 lg:grid-cols-[0.8fr_1.2fr]">
        <Card title={t("api.keyStatus")} description={t("api.keyStatusDesc")}>
          <button className="btn btn-primary" onClick={regenerate}>{t("api.regenerate")}</button>
          {apiKey ? (
            <div className="mt-4 rounded-md border border-line bg-panel p-3">
              <p className="text-sm font-medium">{t("api.shownOnce")}</p>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <code className="break-all text-sm">{apiKey}</code>
                <CopyButton value={apiKey} />
              </div>
            </div>
          ) : (
            <div className="mt-4"><Alert>{t("api.generateReady")}</Alert></div>
          )}
        </Card>
        <Card title={t("api.authTitle")} description={t("api.authDesc")}>
          <pre className="overflow-auto rounded-md bg-neutral-950 p-4 text-sm text-white">Authorization: Bearer $SMSBRIDGE_API_KEY</pre>
        </Card>
      </section>

      <section className="mt-6 grid gap-4">
        {[
          ["exampleBalance", examples.balance],
          ["examplePrices", examples.prices],
          ["exampleCreate", examples.create],
          ["exampleGetOrder", examples.getOrder],
          ["exampleCancel", examples.cancel],
          ["exampleFinish", examples.finish]
        ].map(([name, code]) => (
          <Card key={name} title={t(`api.${name}`)}>
            <div className="mb-2 flex justify-end"><CopyButton value={code} /></div>
            <pre className="overflow-auto rounded-md bg-neutral-950 p-4 text-sm text-white">{code}</pre>
          </Card>
        ))}
      </section>

      <section className="mt-6 grid gap-4 lg:grid-cols-2">
        <Card title={t("api.nodeExample")}>
          <pre className="overflow-auto rounded-md bg-neutral-950 p-4 text-sm text-white">{`const res = await fetch("http://localhost:8000/api/v1/prices?service_code=telegram", {
  headers: { Authorization: \`Bearer \${process.env.SMSBRIDGE_API_KEY}\` }
});
console.log(await res.json());`}</pre>
        </Card>
        <Card title={t("api.pythonExample")}>
          <pre className="overflow-auto rounded-md bg-neutral-950 p-4 text-sm text-white">{`import os
import requests

headers = {"Authorization": f"Bearer {os.environ['SMSBRIDGE_API_KEY']}"}
order = requests.post(
    "http://localhost:8000/api/v1/orders",
    json={"service_code": "telegram", "country_iso2": "ID"},
    headers=headers,
)
print(order.json())`}</pre>
        </Card>
      </section>

      <section className="mt-6 grid gap-4 lg:grid-cols-2">
        <Card title={t("api.balanceResponse")}>
          <pre className="overflow-auto rounded-md bg-panel p-4 text-sm">{`{
  "balance": "25.0000",
  "held_balance": "0.0000",
  "currency": "USD"
}`}</pre>
        </Card>
        <Card title={t("api.orderResponse")}>
          <pre className="overflow-auto rounded-md bg-panel p-4 text-sm">{`{
  "public_id": "order-uuid",
  "service_code": "telegram",
  "country_iso2": "ID",
  "phone_number": "+628123456789",
  "status": "waiting_sms",
  "price": "0.5625"
}`}</pre>
        </Card>
      </section>
    </PageShell>
  );
}
