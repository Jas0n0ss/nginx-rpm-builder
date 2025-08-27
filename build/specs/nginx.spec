%{!?nginx_version: %global nginx_version 1.25.0}

Name:           nginx-custom
Version:        %{nginx_version}
Release:        1%{?dist}
Summary:        NGINX with dynamic modules (local dirs)
License:        BSD
URL:            https://nginx.org/
Source0:        https://nginx.org/download/nginx-%{nginx_version}.tar.gz
Source1:        nginx.service

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel, luajit-devel, perl-ExtUtils-Embed
Requires:       pcre, zlib, openssl, libmaxminddb, luajit

%description
NGINX with modules from pre-extracted directories.

%prep
%setup -n nginx-%{nginx_version}

# 直接使用已解压的模块目录（从 rpmbuild/SOURCES/plugins/ 复制）
cp -r %{_sourcedir}/plugins/ngx_http_geoip2_module-%{geoip2_version} ngx_http_geoip2_module
cp -r %{_sourcedir}/plugins/nginx-module-vts-%{vts_version} nginx-module-vts
cp -r %{_sourcedir}/plugins/ngx_devel_kit-%{devel_kit_version} ngx_devel_kit
cp -r %{_sourcedir}/plugins/lua-nginx-module-%{lua_nginx_version} lua-nginx-module

# 安装 service 文件
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/nginx.service

%build
export LUAJIT_LIB=/usr/lib64
export LUAJIT_INC=/usr/include/luajit-2.1

./configure \
    --prefix=%{_prefix}/nginx \
    --sbin-path=%{_sbindir}/nginx \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf \
    --pid-path=%{_rundir}/nginx.pid \
    --lock-path=%{_localstatedir}/lock/nginx.lock \
    --http-log-path=%{_localstatedir}/log/nginx/access.log \
    --error-log-path=%{_localstatedir}/log/nginx/error.log \
    --user=nginx \
    --group=nginx \
    --modules-path=%{_prefix}/nginx/modules \
    --with-compat \
    --add-dynamic-module=ngx_http_geoip2_module \
    --add-dynamic-module=nginx-module-vts \
    --add-dynamic-module=ngx_devel_kit \
    --add-dynamic-module=lua-nginx-module
make modules

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_localstatedir}/lock
install -d %{buildroot}%{_rundir}
install -d %{buildroot}%{_sysconfdir}/nginx
install -d %{buildroot}%{_sysconfdir}/systemd/system
install -d %{buildroot}%{_prefix}/nginx/modules
install -d %{buildroot}%{_localstatedir}/log/nginx
install -d %{buildroot}%{_localstatedir}/run

make install DESTDIR=%{buildroot}

install -m 644 conf/nginx.conf %{buildroot}%{_sysconfdir}/nginx/nginx.conf
install -m 644 conf/mime.types %{buildroot}%{_sysconfdir}/nginx/mime.types

%files
%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/systemd/system/nginx.service
%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/systemd/system
%dir %{_localstatedir}/log/nginx
%dir %{_localstatedir}/run
%dir %{_prefix}/nginx
%dir %{_prefix}/nginx/modules
%{_sbindir}/nginx
%{_prefix}/nginx/modules/*.so
%{_prefix}/nginx/html/*

%pre
getent group nginx >/dev/null || groupadd -r nginx
getent passwd nginx >/dev/null || useradd -r -g nginx -s /sbin/nologin -c "nginx user" nginx

%post
%systemd_post nginx.service

%postun
%systemd_postun nginx.service

%preun
%systemd_preun nginx.service

%changelog
* Mon Apr 07 2025 Builder <ci@example.com> - %{nginx_version}-1
- Built with pre-extracted modules from local directories
