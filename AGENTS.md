# PawnGuild production safeguards

Use rtk for local shell commands per /Users/davidjaybrady/.codex/RTK.md where available.
Read docs/production.md before deployment. This repository does not own the shared
public Nginx deployment after the September 13, 2026 migration; shared infrastructure
lives at /home/david/shared-web-infrastructure on david@137.184.81.130.

The owner prioritizes preserving player data and existing database backups. Protect
container postgres, volume pawnguild_postgres_data, uploaded media, and all files
under /var/backups/db_backups and /home/david/pawnguild-migration-20260913. Existing
untracked db_snapshot.json files in the production checkout are private data: do
not delete, print, stage, or commit them. Never use git clean, volume pruning,
Compose down -v, fixture loading, or restore tests in production.

Production uses only docker-compose.prod.yml, which is standalone; do not merge it
with the development base file. Deploy only web using scripts/deploy-production.sh.
Production startup intentionally runs Gunicorn directly and does not run automatic
migrations or superuser creation. Schema changes require a separate reviewed plan.

The owner already warned the player base and authorized downtime today for the
Nginx separation and pawn-history filter. Do not ask again during this authorized
work. Future expected outages need advance notice so players can be warned.
Off-droplet backup and OS upgrade projects are not prerequisites; preserve existing
data and take a fresh verified local dump before changes with data impact.

The historical-pawn feature is read-only: Currently active remains the default,
with Updated within the last year (365 days) and All time, using last_modified.
No record deletion, timestamp rewriting, or schema migration is part of the feature.
Run synthetic local/CI tests; never point test settings at production data. Keep
large lists paginated. Keep runtime dependency upgrades out of this change.

Every push to production triggers app deployment. Work on a feature branch until
review and validation are complete. Preserve unrelated work and data snapshots.
