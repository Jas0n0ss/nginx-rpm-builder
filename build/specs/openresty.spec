Name:           openresty-custom
Version:        1.27.1.2
Release:        1%{?dist}
Summary:        OpenResty with GeoIP2 and VTS modules
License:        BSD
URL:            https://openresty.org/
Source0:        https://openresty.org/download/openresty-%{version}.tar.gz

# 动态模块源码（在线下载）
Source1:        https://github.com/leev/ngx_http_geoip2_module/archive/refs/tags/3.4.tar.gz
Source2:        https://github.com/vozlt/nginx-module-vts/archive/refs/tags/v0.2.2.tar.gz

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel
Requires:       pcre, zlib, openssl, libmaxminddb

%description
OpenResty with additional dynamic modules: GeoIP2, VTS.

%prep
%setup -n openresty-%{version} -a 1 -a 2

# 重命名模块目录为预期名称
mv ngx_http_geoip2_module-3.4 ngx_http_geoip2_module
mv nginx-module-vts-v0.2.2 nginx-module-vts

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
    --add-dynamic-module=ngx_http_geoip2_module \
    --add-dynamic-module=nginx-module-vts
make

%install
mkdir -p %{buildroot}/usr/lib64/openresty/modules
cp build/objs/*.so %{buildroot}/usr/lib64/openresty/modules/ || true

%files
/usr/lib64/openresty/modules/ngx_http_geoip2_module.so
/usr/lib64/openresty/modules/ngx_http_vhost_traffic_status_module.so

%changelog
* 05 Apr 2025 Builder <ci@example.com> - 1.27.1.2-1
- Auto-built with dynamic modules from online sources
