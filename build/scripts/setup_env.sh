#!/bin/bash
set -eux

echo "🔧 Installing dependencies..."

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

# 克隆模块
cd ~/modules || mkdir -p ~/modules && cd ~/modules
declare -A MODS=(
  [ngx_http_geoip2_module]=https://github.com/leev/ngx_http_geoip2_module.git
  [nginx-module-vts]=https://github.com/vozlt/nginx-module-vts.git
  [ngx_devel_kit]=https://github.com/simplresty/ngx_devel_kit.git
  [lua-nginx-module]=https://github.com/openresty/lua-nginx-module.git
)
for name in "${!MODS[@]}"; do
  [[ -d "$name" ]] || git clone "${MODS[$name]}" "$name"
done

# 克隆 Lua 库
cd ~/lualib || mkdir -p ~/lualib && cd ~/lualib
[[ -d "lua-resty-core" ]] || git clone https://github.com/openresty/lua-resty-core.git
[[ -d "lua-resty-lrucache" ]] || git clone https://github.com/openresty/lua-resty-lrucache.git

echo "✅ 环境准备完成"
