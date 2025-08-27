#!/bin/bash
set -euo pipefail

echo "🔧 安装 EPEL 仓库..."
dnf install -y epel-release
# 刷新仓库缓存
dnf makecache

echo "🔧 安装构建依赖..."
dnf install -y \
    rpmdevtools \
    rpm-build \
    wget git unzip jq \
    pcre-devel zlib-devel openssl-devel \
    libmaxminddb-devel \
    luajit luajit-devel \
    perl-ExtUtils-Embed \
    systemd-devel \
    which autoconf automake libtool

# 初始化 rpmbuild 目录结构
echo "🔧 初始化 rpmbuild 目录..."
rpmdev-setuptree || mkdir -p ~/rpmbuild/{SOURCES,SPECS,RPMS,SRPMS,BUILD}

echo "✅ 环境准备完成"
