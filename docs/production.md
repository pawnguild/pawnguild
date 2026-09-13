# Production deployment after the shared Nginx migration

Production uses **only** `docker-compose.prod.yml`, a standalone configuration.
The base `docker-compose.yml` remains for development/test use; combining it with
production would reintroduce the old Nginx service and its public port bindings.

The shared Nginx deployment is managed separately at
`/home/david/shared-web-infrastructure`. PawnGuild must not stop, recreate, or
configure it. The external `shared_web_frontend` network connects the app using
alias `pawnguild-app`; PostgreSQL remains on `pawnguild_default` only.

`./scripts/deploy-production.sh` validates existing infrastructure and updates only
`web`. It reuses the installed runtime image, collects static assets, and reloads
Gunicorn. PostgreSQL and its existing data volume are left running. The production
command runs Gunicorn directly: it does not call the development `start.sh` or run
`makemigrations`, `migrate`, or `createsuperuser`. Intentional schema changes require
a separately prepared migration and a fresh verified backup. This release has none.

All existing production data volumes are declared external. Never run volume
pruning, `down -v`, restore tests, or destructive historical debugging recipes on
this host. Protect `/var/backups/db_backups` and the migration recovery directory
`/home/david/pawnguild-migration-20260913`.

The production GitHub workflow no longer builds on the droplet or runs Compose
`down`. Dependency/Dockerfile changes cause it to stop before updating the checkout,
so a compatible image can be prepared separately. App/template changes use the
existing bind-mounted source and runtime. A production push still deploys the app;
do not push a change until it is ready for production.

## Pawn activity filter

Public lists now offer Currently active (the existing default), Updated within the
last year (365 days by last update), and All time. This changes reads/display only;
older pawns are neither modified nor deleted. Both the combined page and each
platform page have bounded pagination (50 per platform) and preserve filter values.
The API and account-management behavior are unchanged.
