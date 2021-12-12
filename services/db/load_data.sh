#!/bin/bash

psql -d pawnguild -W < /docker-entrypoint-initdb.d/db.sqlite3-2021-12-11
