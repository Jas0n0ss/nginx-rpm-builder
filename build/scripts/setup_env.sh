#!/bin/bash
set -eux

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

# 初始化 rpmbuild
rpmdev-setuptree || mkdir -p ~/rpmbuild/{SOURCES,SPECS,RPMS,SRPMS,BUILD}

echo "✅ 环境准备完成（模块将在 .spec 中自动下载）"
