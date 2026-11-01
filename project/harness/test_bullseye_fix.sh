#!/bin/bash
set -e
cat > /etc/apt/sources.list <<'EOF'
deb http://archive.debian.org/debian bullseye main
deb http://archive.debian.org/debian-security bullseye-security main
EOF
apt-get -o Acquire::Check-Valid-Until=false update >/dev/null 2>&1
apt-get install -y apache2 libapache2-mod-wsgi-py3 python3 python3-pip curl >/dev/null 2>&1
echo "INSTALL_EXIT=$?"
apache2 -v | head -1
python3 --version
