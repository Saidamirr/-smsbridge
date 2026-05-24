"use client";

import {useEffect, useState} from "react";
import {currentUser} from "@/lib/shared/api";
import type {User} from "@/lib/shared/types";
import {Alert, PageShell} from "@/components/shared/ui";
import {useTranslation} from "@/lib/i18n";

export function AdminGuard({children}: {children: (user: User) => React.ReactNode}) {
  const {t} = useTranslation();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    currentUser()
      .then((me) => {
        if (me.role !== "admin") {
          setError(t("admin.denied"));
          return;
        }
        setUser(me);
      })
      .catch((err) => setError(err instanceof Error ? err.message : t("common.sessionExpired")))
      .finally(() => setLoading(false));
  }, [t]);

  if (loading) {
    return (
      <PageShell>
        <Alert>{t("admin.checking")}</Alert>
      </PageShell>
    );
  }

  if (error || !user) {
    return (
      <PageShell>
        <h1 className="text-2xl font-semibold">{t("admin.title")}</h1>
        <div className="mt-4">
          <Alert type="error">{error || t("common.accessDenied")}</Alert>
        </div>
      </PageShell>
    );
  }

  return <>{children(user)}</>;
}
