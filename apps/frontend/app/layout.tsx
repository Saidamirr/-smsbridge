import type {Metadata} from "next";
import "./globals.css";
import {Nav} from "@/components/shared/nav";
import {I18nProvider} from "@/lib/i18n";

export const metadata: Metadata = {
  title: "smsbridge",
  description: "Compliant SMS verification API for developers and QA teams"
};

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="en">
      <body>
        <I18nProvider>
          <Nav>{children}</Nav>
        </I18nProvider>
      </body>
    </html>
  );
}
