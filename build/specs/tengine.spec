%{!?tengine_version: %global tengine_version 3.1.0}
%{!?geoip2_version: %global geoip2_version 3.4}
%{!?vts_version: %global vts_version 0.2.4}
%{!?devel_kit_version: %global devel_kit_version 0.3.4}
%{!?lua_nginx_version: %global lua_nginx_version 0.10.28}

Name:           tengine-custom
Version:        %{tengine_version}
Release:        1%{?dist}
Summary:        Tengine with dynamic modules (local dirs)
License:        BSD
URL:            https://tengine.taobao.org/
Source0:        https://github.com/alibaba/tengine/archive/refs/tags/v%{tengine_version}.tar.gz
Source1:        tengine.service

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel, luajit-devel, perl-ExtUtils-Embed
Requires:       pcre, zlib, openssl, libmaxminddb, luajit

%description
Tengine with modules from pre-extracted directories.

%prep
%setup -n tengine-%{tengine_version}

cp -r %{_sourcedir}/plugins/ngx_http_geoip2_module-%{geoip2_version} ngx_http_geoip2_module
cp -r %{_sourcedir}/plugins/nginx-module-vts-%{vts_version} nginx-module-vts
cp -r %{_sourcedir}/plugins/ngx_devel_kit-%{devel_kit_version} ngx_devel_kit
cp -r %{_sourcedir}/plugins/lua-nginx-module-%{lua_nginx_version} lua-nginx-module

install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/tengine.service

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
    --add-dynamic-module=ngx_http_geoip2_module \
    --add-dynamic-module=nginx-module-vts \
    --add-dynamic-module=ngx_devel_kit \
    --add-dynamic-module=lua-nginx-module
make modules

%install
mkdir -p %{buildroot}/usr/lib64/tengine/modules
cp objs/*.so %{buildroot}/usr/lib64/tengine/modules/

%files
/usr/lib64/tengine/modules/ngx_http_geoip2_module.so
/usr/lib64/tengine/modules/ngx_http_vhost_traffic_status_module.so
/usr/lib64/tengine/modules/ndk_http_module.so
/usr/lib64/tengine/modules/ngx_http_lua_module.so

%changelog
* Mon Apr 07 2025 Builder <ci@example.com> - %{tengine_version}-1
- Built with pre-extracted modules
