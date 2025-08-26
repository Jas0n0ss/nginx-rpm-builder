Name:           tengine-custom
Version:        3.1.0
Release:        1%{?dist}
Summary:        Tengine with GeoIP2, VTS, Lua
License:        BSD
URL:            https://tengine.taobao.org/
Source0:        tengine-%{version}.tar.gz
BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel, luajit-devel, perl-ExtUtils-Embed
Requires:       pcre, zlib, openssl, libmaxminddb, luajit

%description
Custom Tengine with dynamic modules and Lua support.

%prep
%setup -n tengine-%{version}

%build
./configure \
    --prefix=/etc/tengine \
    --sbin-path=/usr/sbin/tengine \
    --modules-path=/usr/lib64/tengine/modules \
    --conf-path=/etc/tengine/nginx.conf \
    --pid-path=/var/run/tengine.pid \
    --user=nginx \
    --group=nginx \
    --with-compat \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --add-dynamic-module=%{MODULES}/ngx_http_geoip2_module \
    --add-dynamic-module=%{MODULES}/nginx-module-vts \
    --add-dynamic-module=%{MODULES}/ngx_devel_kit \
    --add-dynamic-module=%{MODULES}/lua-nginx-module
make modules

%install
mkdir -p %{buildroot}/usr/lib64/tengine/modules
cp objs/*.so %{buildroot}/usr/lib64/tengine/modules/

%post
cat << 'EOF'
💡 模块启用提示：
请在 /etc/tengine/nginx.conf 中添加：
    load_module modules/ngx_http_geoip2_module.so;
    load_module modules/ngx_http_vhost_traffic_status_module.so;
    load_module modules/ndk_http_module.so;
    load_module modules/ngx_http_lua_module.so;
EOF

%files
/usr/lib64/tengine/modules/ngx_http_geoip2_module.so
/usr/lib64/tengine/modules/ngx_http_vhost_traffic_status_module.so
/usr/lib64/tengine/modules/ndk_http_module.so
/usr/lib64/tengine/modules/ngx_http_lua_module.so

%changelog
* Sun Apr 05 2025 Builder <ci@example.com> - %{version}-1
- Auto-built with dynamic modules
