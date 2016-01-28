#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

chmod 755 cg
chmod 755 dramatica_templates
chmod 755 nxcg
chmod 755 playout
chmod 755 worker
chmod 755 fix_permissions.sh

chmod 644 cg/*.py
chmod 644 dramatica_templates/*.py
chmod 644 nxcg/*.py
chmod 644 playout/*.py
chmod 644 worker/*.py
