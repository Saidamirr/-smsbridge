"use client";

import {EmptyState} from "@/components/shared/ui";
import {useTranslation} from "@/lib/i18n";

export type Column<T> = {
  key: string;
  header: string;
  render?: (row: T) => React.ReactNode;
  className?: string;
};

export function DataTable<T extends Record<string, unknown>>({
  rows,
  columns,
  emptyTitle = "No data yet.",
  emptyDescription
}: {
  rows: T[];
  columns: Column<T>[];
  emptyTitle?: string;
  emptyDescription?: string;
}) {
  const {t} = useTranslation();
  if (!rows.length) return <EmptyState title={emptyTitle === "No data yet." ? t("common.noData") : emptyTitle} description={emptyDescription} />;
  return (
    <div className="overflow-x-auto rounded-md border border-line bg-white">
      <table className="w-full min-w-[860px] border-collapse text-left text-sm">
        <thead className="bg-panel">
          <tr>
            {columns.map((column) => (
              <th className={`border-b border-line px-3 py-2 font-medium text-neutral-700 ${column.className || ""}`} key={column.key}>
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr className="border-b border-line last:border-0 hover:bg-panel/60" key={String(row.id ?? row.public_id ?? index)}>
              {columns.map((column) => (
                <td className={`px-3 py-2 align-top text-neutral-700 ${column.className || ""}`} key={column.key}>
                  {column.render ? column.render(row) : String(row[column.key] ?? "-")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
