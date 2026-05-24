"use client";

import {CheckCircle2} from "lucide-react";
import {useTranslation} from "@/lib/i18n";

export function OnboardingChecklist({role}: {role?: string}) {
  const {t} = useTranslation();
  const admin = t("dashboard.checklistAdmin").split("|");
  const user = t("dashboard.checklistUser").split("|");
  const items = role === "admin" ? admin : user;
  return (
    <ol className="grid gap-2">
      {items.map((item, index) => (
        <li className="flex items-center gap-2 text-sm text-neutral-700" key={item}>
          <CheckCircle2 size={16} className="text-accent" />
          <span>{index + 1}. {item}</span>
        </li>
      ))}
    </ol>
  );
}
