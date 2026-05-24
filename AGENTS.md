# smsbridge Agent Instructions

- Preserve wallet transaction integrity. Balance and held balance must never go negative.
- Every money movement must create a `WalletTransaction`.
- Holds are created when an order is bought. Successful orders capture the hold. Cancelled or expired orders refund the hold.
- Capture and refund paths must remain idempotent.
- Do not implement fraud, spam, phishing, ban bypass, fake identity, mass account abuse or other illegal-use features.
- Always add or update tests for order lifecycle and wallet changes.
- Keep provider adapters isolated under `apps/backend/app/providers`.
- Prefer small, reviewable changes.
- Never store raw API keys, provider API keys or passwords.
- Update `README.md` when adding features, setup steps or operational assumptions.
- Keep RU/EN localization keys organized.
- Do not break Docker Compose startup.

