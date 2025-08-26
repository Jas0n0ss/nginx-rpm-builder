Name:           nginx-custom
Version:        1.28.0
Release:        1%{?dist}
Summary:        NGINX with GeoIP2, VTS, Lua, and NDK modules
License:        BSD
URL:            https://nginx.org/
Source0:        nginx-%{version}.tar.gz

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel, luajit-devel, perl-ExtUtils-Embed
Requires:       pcre, zlib, openssl, libmaxminddb, luajit

%description
Custom NGINX build with dynamic modules and Lua support.

%prep
%setup -n nginx-%{version}

%build
./configure \
    --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --modules-path=/usr/lib64/nginx/modules \
    --conf-path=/etc/nginx/nginx.conf \
    --pid-path=/var/run/nginx.pid \
    --user=nginx \
    --group=nginx \
    --with-compat \
    --with-http_ssl_module \
    --add-dynamic-module=%{MODULES}/ngx_http_geoip2_module \
    --add-dynamic-module=%{MODULES}/nginx-module-vts \
    --add-dynamic-module=%{MODULES}/ngx_devel_kit \
    --add-dynamic-module=%{MODULES}/lua-nginx-module
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
- Auto-built with dynamic modules
