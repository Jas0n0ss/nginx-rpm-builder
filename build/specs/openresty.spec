Name:           openresty-custom
Version:        1.25.3.1
Release:        1%{?dist}
Summary:        OpenResty with GeoIP2 and VTS modules
License:        BSD
URL:            https://openresty.org/
Source0:        openresty-%{version}.tar.gz
BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel
Requires:       pcre, zlib, openssl, libmaxminddb

%description
OpenResty with additional dynamic modules: GeoIP2, VTS.

%prep
%setup -n openresty-%{version}

%build
./configure \
    --prefix=/etc/openresty \
    --sbin-path=/usr/sbin/openresty \
    --modules-path=/usr/lib64/openresty/modules \
    --conf-path=/etc/openresty/nginx.conf \
    --pid-path=/var/run/openresty.pid \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-compat \
    --add-dynamic-module=%{MODULES}/ngx_http_geoip2_module \
    --add-dynamic-module=%{MODULES}/nginx-module-vts
make

%install
mkdir -p %{buildroot}/usr/lib64/openresty/modules
cp build/objs/*.so %{buildroot}/usr/lib64/openresty/modules/ || true

%post
cat << 'EOF'
💡 模块启用提示：
请在 /etc/openresty/nginx.conf 中添加：
    load_module modules/ngx_http_geoip2_module.so;
    load_module modules/ngx_http_vhost_traffic_status_module.so;
EOF

%files
/usr/lib64/openresty/modules/ngx_http_geoip2_module.so
/usr/lib64/openresty/modules/ngx_http_vhost_traffic_status_module.so

%changelog
* Sun Apr 05 2025 Builder <ci@example.com> - %{version}-1
- Auto-built with dynamic modules
