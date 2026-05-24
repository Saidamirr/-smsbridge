"use client";

import {Card, PageShell} from "@/components/shared/ui";
import {useTranslation} from "@/lib/i18n";

export default function TermsPage() {
  const {t} = useTranslation();
  return (
    <PageShell>
      <Card title={t("legal.terms")}>
        <p className="leading-7 text-neutral-700">{t("legal.termsText")}</p>
      </Card>
    </PageShell>
  );
}
