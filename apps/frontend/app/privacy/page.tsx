"use client";

import {Card, PageShell} from "@/components/shared/ui";
import {useTranslation} from "@/lib/i18n";

export default function PrivacyPage() {
  const {t} = useTranslation();
  return (
    <PageShell>
      <Card title={t("legal.privacy")}>
        <p className="leading-7 text-neutral-700">{t("legal.privacyText")}</p>
      </Card>
    </PageShell>
  );
}
