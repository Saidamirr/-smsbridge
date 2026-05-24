"use client";

import {Card, PageShell} from "@/components/shared/ui";
import {useTranslation} from "@/lib/i18n";

export default function AcceptableUsePage() {
  const {t} = useTranslation();
  return (
    <PageShell>
      <Card title={t("legal.acceptableUse")}>
        <p className="leading-7 text-neutral-700">{t("legal.aupText")}</p>
        <p className="mt-4 leading-7 text-neutral-700">{t("legal.placeholder")}</p>
      </Card>
    </PageShell>
  );
}
