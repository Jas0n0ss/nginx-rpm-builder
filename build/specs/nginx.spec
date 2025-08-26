Name:           nginx-custom
Version:        1.25.0
Release:        1%{?dist}
Summary:        NGINX with GeoIP2, VTS, Lua, LuaJIT
License:        BSD
URL:            https://nginx.org/
Source0:        nginx-%{version}.tar.gz
BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel, luajit-devel, perl-ExtUtils-Embed
Requires:       pcre, zlib, openssl, libmaxminddb, luajit

%description
Custom NGINX with dynamic modules and Lua support.

%prep
%setup -n nginx-%{version}

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
    --add-dynamic-module=%{MODULES}/ngx_http_geoip2_module \
    --add-dynamic-module=%{MODULES}/nginx-module-vts \
    --add-dynamic-module=%{MODULES}/ngx_devel_kit \
    --add-dynamic-module=%{MODULES}/lua-nginx-module
make modules

%install
mkdir -p %{buildroot}/usr/lib64/nginx/modules
cp objs/*.so %{buildroot}/usr/lib64/nginx/modules/

%post
cat << 'EOF'
💡 模块启用提示：
请在 /etc/nginx/nginx.conf 中添加：
    load_module modules/ngx_http_geoip2_module.so;
    load_module modules/ngx_http_vhost_traffic_status_module.so;
    load_module modules/ndk_http_module.so;
    load_module modules/ngx_http_lua_module.so;
EOF

%files
/usr/lib64/nginx/modules/ngx_http_geoip2_module.so
/usr/lib64/nginx/modules/ngx_http_vhost_traffic_status_module.so
/usr/lib64/nginx/modules/ndk_http_module.so
/usr/lib64/nginx/modules/ngx_http_lua_module.so

%changelog
* Sun Apr 05 2025 Builder <ci@example.com> - %{version}-1
- Auto-built with dynamic modules and LuaJIT
