"use client";

import Link from "next/link";
import {ArrowRight, CheckCircle2, Code2, Globe2, ShieldCheck, Signal, Terminal, WalletCards} from "lucide-react";
import {Card, CopyButton} from "@/components/shared/ui";
import {useTranslation} from "@/lib/i18n";

export default function Home() {
  const {t} = useTranslation();
  const curl = `curl -H "Authorization: Bearer $SMSBRIDGE_API_KEY" \\
  "http://localhost:8000/api/v1/prices?service_code=telegram&country_iso2=ID"`;
  const stats = [
    {label: t("landing.services"), value: "6", helper: t("landing.statsServicesDesc")},
    {label: t("landing.countries"), value: "7", helper: t("landing.statsCountriesDesc")},
    {label: t("landing.mockActive"), value: "1", helper: t("landing.statsProviderDesc")},
    {label: t("landing.apiReady"), value: "OpenAPI", helper: t("landing.statsApiDesc")}
  ];
  const features = [
    {icon: ShieldCheck, title: t("landing.featureCompliance"), body: t("landing.featureComplianceText")},
    {icon: WalletCards, title: t("landing.featureWallet"), body: t("landing.featureWalletText")},
    {icon: Terminal, title: t("landing.featureProvider"), body: t("landing.featureProviderText")}
  ];
  const flow = [
    [t("landing.chooseService"), t("landing.flowChooseService")],
    [t("landing.chooseCountry"), t("landing.flowChooseCountry")],
    [t("landing.buyNumber"), t("landing.flowBuyNumber")],
    [t("landing.receiveSms"), t("landing.flowReceiveSms")],
    [t("landing.finishOrder"), t("landing.flowFinishOrder")]
  ];

  return (
    <main className="bg-white">
      <section className="border-b border-line bg-[radial-gradient(circle_at_top_left,#dbeafe,transparent_34%),linear-gradient(180deg,#ffffff,#f6f8fb)]">
        <div className="mx-auto grid max-w-7xl gap-10 px-4 py-16 lg:grid-cols-[1.08fr_0.92fr] lg:py-20">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-blue-100 bg-white px-3 py-1 text-xs font-medium text-accent shadow-sm">
              <Signal size={14} />
              {t("landing.apiReady")}
            </div>
            <h1 className="mt-6 text-4xl font-semibold tracking-normal text-ink md:text-6xl">{t("landing.title")}</h1>
            <p className="mt-5 text-xl leading-8 text-neutral-700">{t("landing.hero")}</p>
            <p className="mt-3 max-w-2xl text-base leading-7 text-neutral-600">{t("landing.subhero")}</p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link className="btn btn-primary" href="/register">{t("landing.getStarted")}<ArrowRight size={16} /></Link>
              <Link className="btn btn-secondary" href="/buy">{t("landing.viewPrices")}</Link>
              <Link className="btn btn-secondary" href="/api-docs">{t("landing.apiDocs")}</Link>
            </div>
          </div>
          <div className="grid gap-4 self-center">
            {features.map(({icon: Icon, title, body}) => (
              <div className="panel" key={title}>
                <div className="flex items-start gap-3">
                  <Icon className="mt-1 text-accent" size={21} />
                  <div>
                    <h2 className="font-medium">{title}</h2>
                    <p className="mt-1 text-sm leading-6 text-neutral-600">{body}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-4 px-4 py-10 md:grid-cols-4">
        {stats.map((item) => (
          <Card key={item.label} className="p-4">
            <p className="text-sm text-neutral-500">{item.label}</p>
            <p className="mt-2 text-2xl font-semibold">{item.value}</p>
            <p className="mt-2 text-xs leading-5 text-neutral-500">{item.helper}</p>
          </Card>
        ))}
      </section>

      <section className="border-y border-line bg-slate-50">
        <div className="mx-auto grid max-w-7xl gap-6 px-4 py-12 lg:grid-cols-[0.7fr_1.3fr]">
          <div>
            <h2 className="text-2xl font-semibold">{t("landing.productFlow")}</h2>
            <p className="mt-3 text-sm leading-6 text-neutral-600">{t("landing.complianceText")}</p>
          </div>
          <div className="grid gap-3 md:grid-cols-5">
            {flow.map(([title, body], index) => (
              <div className="rounded-lg border border-line bg-white p-4 shadow-sm" key={title}>
                <span className="grid h-8 w-8 place-items-center rounded-full bg-blue-50 text-sm font-semibold text-accent">{index + 1}</span>
                <h3 className="mt-4 text-sm font-semibold">{title}</h3>
                <p className="mt-2 text-xs leading-5 text-neutral-600">{body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-12 lg:grid-cols-2">
        <Card title={t("landing.developerApi")} description={t("landing.apiText")}>
          <div className="mb-2 flex justify-end"><CopyButton value={curl} /></div>
          <pre className="overflow-auto rounded-lg bg-neutral-950 p-4 text-sm text-white">{curl}</pre>
        </Card>
        <Card title={t("landing.compliance")} description={t("landing.complianceText")}>
          <div className="grid gap-3 text-sm text-neutral-700">
            <p className="flex items-start gap-2"><CheckCircle2 size={17} className="mt-0.5 text-accent" />{t("legal.aupText")}</p>
            <p className="flex items-start gap-2"><Code2 size={17} className="mt-0.5 text-accent" />{t("landing.apiText")}</p>
            <p className="flex items-start gap-2"><Globe2 size={17} className="mt-0.5 text-accent" />{t("landing.statsCountriesDesc")}</p>
          </div>
        </Card>
      </section>

      <footer className="border-t border-line bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-8 text-sm text-neutral-600 md:flex-row md:items-center md:justify-between">
          <p>smsbridge</p>
          <div className="flex flex-wrap gap-4">
            <Link href="/terms">{t("landing.footerTerms")}</Link>
            <Link href="/privacy">{t("landing.footerPrivacy")}</Link>
            <Link href="/acceptable-use">{t("landing.footerAup")}</Link>
            <Link href="/abuse">{t("landing.footerAbuse")}</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
