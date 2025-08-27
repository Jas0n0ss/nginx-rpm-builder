#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# 仅安装系统依赖和初始化 rpmbuild
dnf update -y
dnf install -y epel-release
dnf config-manager --set-enabled crb
dnf groupinstall -y "Development Tools"
dnf install -y \
    rpm-build wget git unzip jq \
    pcre-devel zlib-devel openssl-devel \
    libmaxminddb-devel \
    luajit luajit-devel \
    perl-ExtUtils-Embed \
    systemd-devel \
    which autoconf automake libtool

# 初始化 rpmbuild 结构
rpmdev-setuptree || mkdir -p ~/rpmbuild/{SOURCES,SPECS,RPMS,SRPMS,BUILD}

echo "✅ 环境准备完成"
