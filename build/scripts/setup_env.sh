#!/bin/bash
set -euo pipefail

dnf update -y
dnf install -y \
    epel-release \
    rpmdevtools \
    rpm-build \
    wget git unzip jq \
    pcre-devel zlib-devel openssl-devel \
    libmaxminddb-devel \
    luajit luajit-devel \
    perl-ExtUtils-Embed \
    systemd-devel \
    which autoconf automake libtool

# 初始化 rpmbuild
rpmdev-setuptree || mkdir -p ~/rpmbuild/{SOURCES,SPECS,RPMS,SRPMS,BUILD}

echo "✅ 环境准备完成"
