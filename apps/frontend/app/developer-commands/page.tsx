"use client";

import {Card, PageHeader, PageShell} from "@/components/shared/ui";
import {useTranslation} from "@/lib/i18n";

const dockerCommands = [
  "docker compose up --build",
  "docker compose up",
  "docker compose down",
  "docker compose down --volumes",
  "docker compose logs backend",
  "docker compose logs frontend",
  "docker compose logs worker",
  "docker compose exec backend alembic upgrade head",
  "docker compose exec backend pytest"
];

const smokeCommands = [
  "curl http://localhost:8000/health",
  "open http://localhost:3000",
  "open http://localhost:8000/docs"
];

export default function DeveloperCommandsPage() {
  const {t} = useTranslation();
  const checklist = t("developer.checklistItems").split("|");
  const roadmap = [
    [`${t("developer.stage")} 1`, t("developer.stage1")],
    [`${t("developer.stage")} 2`, t("developer.stage2")],
    [`${t("developer.stage")} 3`, t("developer.stage3")],
    [`${t("developer.stage")} 4`, t("developer.stage4")],
    [`${t("developer.stage")} 5`, t("developer.stage5")]
  ];
  return (
    <PageShell>
      <PageHeader title={t("developer.title")} description={t("developer.description")} />
      <section className="mt-6 grid gap-4 lg:grid-cols-2">
        <CommandCard title={t("developer.docker")} commands={dockerCommands} />
        <CommandCard title={t("developer.smoke")} commands={smokeCommands} />
        <Card title={t("developer.checklist")}>
          <ol className="grid gap-2 text-sm">
            {checklist.map((item, index) => <li key={item}>{index + 1}. {item}</li>)}
          </ol>
        </Card>
        <Card title={t("developer.roadmap")}>
          <div className="grid gap-3 text-sm">
            {roadmap.map(([stage, text]) => <p key={stage}><strong>{stage}:</strong> {text}</p>)}
          </div>
        </Card>
      </section>
    </PageShell>
  );
}

function CommandCard({title, commands}: {title: string; commands: string[]}) {
  return (
    <Card title={title}>
      <div className="grid gap-2">
        {commands.map((command) => <code className="rounded-md bg-neutral-950 px-3 py-2 text-sm text-white" key={command}>{command}</code>)}
      </div>
    </Card>
  );
}
