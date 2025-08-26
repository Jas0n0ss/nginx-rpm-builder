Name:           nginx-custom
Version:        1.28.0
Release:        1%{?dist}
Summary:        NGINX with GeoIP2, VTS, Lua, and NDK modules
License:        BSD
URL:            https://nginx.org/
Source0:        http://nginx.org/download/nginx-%{version}.tar.gz

# 动态模块源码（在线下载）
Source1:        https://github.com/leev/ngx_http_geoip2_module/archive/refs/tags/3.4.tar.gz
Source2:        https://github.com/vozlt/nginx-module-vts/archive/refs/tags/v0.2.2.tar.gz
Source3:        https://github.com/simplresty/ngx_devel_kit/archive/v0.3.4.tar.gz
Source4:        https://github.com/openresty/lua-nginx-module/archive/v0.10.28.tar.gz

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel, luajit-devel, perl-ExtUtils-Embed
Requires:       pcre, zlib, openssl, libmaxminddb, luajit

%description
Custom NGINX build with dynamic modules and Lua support.

%prep
%setup -n nginx-%{version} -a 1 -a 2 -a 3 -a 4

# 重命名解压后的模块目录为预期名称
mv ngx_http_geoip2_module-3.4 ngx_http_geoip2_module
mv nginx-module-vts-v0.2.2 nginx-module-vts
mv ngx_devel_kit-v0.3.4 ngx_devel_kit
mv lua-nginx-module-v0.10.28 lua-nginx-module

%build
./configure \
    --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --modules-path=/usr/lib64/nginx/modules \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/run/nginx.lock \
    --user=nginx \
    --group=nginx \
    --with-compat \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-http_stub_status_module \
    --with-stream \
    --with-stream_ssl_module \
    --add-dynamic-module=ngx_http_geoip2_module \
    --add-dynamic-module=nginx-module-vts \
    --add-dynamic-module=ngx_devel_kit \
    --add-dynamic-module=lua-nginx-module
make modules

%install
mkdir -p %{buildroot}/usr/lib64/nginx/modules
cp objs/*.so %{buildroot}/usr/lib64/nginx/modules/

%files
/usr/lib64/nginx/modules/ngx_http_geoip2_module.so
/usr/lib64/nginx/modules/ngx_http_vhost_traffic_status_module.so
/usr/lib64/nginx/modules/ndk_http_module.so
/usr/lib64/nginx/modules/ngx_http_lua_module.so

%changelog
* 05 Apr 2025 Builder <ci@example.com> - 1.28.0-1
- Auto-built with dynamic modules from online sources
