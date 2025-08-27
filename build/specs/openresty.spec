%{!?version: %global version 1.27.1.2}
%{!?geoip2_version: %global geoip2_version 3.4}
%{!?vts_version: %global vts_version 0.2.4}

Name:           openresty-custom
Version:        %{version}
Release:        1%{?dist}
Summary:        OpenResty with dynamic modules (local dirs)
License:        BSD
URL:            https://openresty.org/
Source0:        https://openresty.org/download/openresty-%{version}.tar.gz

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel
Requires:       pcre, zlib, openssl, libmaxminddb

%description
OpenResty with modules from pre-extracted directories.

%prep
%setup -n openresty-%{version}

cp -r %{_sourcedir}/plugins/ngx_http_geoip2_module-%{geoip2_version} ngx_http_geoip2_module
cp -r %{_sourcedir}/plugins/nginx-module-vts-%{vts_version} nginx-module-vts

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
* Mon Apr 07 2025 Builder <ci@example.com> - %{version}-1
- Built with pre-extracted modules
