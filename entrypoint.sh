#!/bin/bash

chmod +x alembic.ini
python -m solc.install v0.4.25
cp $HOME/.py-solc/solc-v0.4.25/bin/solc /usr/local/bin/
dumb-init alembic -c alembic.ini upgrade head
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --access-log --log-config src/logging.conf
