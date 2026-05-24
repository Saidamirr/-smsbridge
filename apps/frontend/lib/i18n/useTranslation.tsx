"use client";

import {createContext, useContext, useEffect, useMemo, useState} from "react";
import {Locale, translate} from "@/lib/i18n/translations";

type I18nContextValue = {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: string, vars?: Record<string, string | number>) => string;
};

const I18nContext = createContext<I18nContextValue | null>(null);

export function I18nProvider({children}: {children: React.ReactNode}) {
  const [locale, setLocaleState] = useState<Locale>("en");

  useEffect(() => {
    const stored = localStorage.getItem("locale");
    if (stored === "ru" || stored === "en") {
      setLocaleState(stored);
      document.documentElement.lang = stored;
    }
  }, []);

  function setLocale(next: Locale) {
    setLocaleState(next);
    localStorage.setItem("locale", next);
    document.documentElement.lang = next;
    window.dispatchEvent(new Event("smsbridge-locale-changed"));
  }

  const value = useMemo<I18nContextValue>(() => ({
    locale,
    setLocale,
    t: (key, vars) => translate(locale, key, vars)
  }), [locale]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useTranslation() {
  const context = useContext(I18nContext);
  if (!context) {
    return {
      locale: "en" as Locale,
      setLocale: () => undefined,
      t: (key: string, vars?: Record<string, string | number>) => translate("en", key, vars)
    };
  }
  return context;
}

