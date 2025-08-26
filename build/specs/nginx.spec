%{!?nginx_version: %global nginx_version 1.25.0}
%{!?geoip2_version: %global geoip2_version 3.4}
%{!?vts_version: %global vts_version 0.2.4}
%{!?devel_kit_version: %global devel_kit_version 0.3.4}
%{!?lua_nginx_version: %global lua_nginx_version 0.10.28}
%{!?lua_resty_core_version: %global lua_resty_core_version 0.1.31}
%{!?lua_resty_lrucache_version: %global lua_resty_lrucache_version 0.15}

%global _lockdir %{_localstatedir}/lock

Name:           nginx-custom
Version:        %{nginx_version}
Release:        1%{?dist}
Summary:        NGINX with Lua and dynamic module support
License:        BSD
URL:            https://nginx.org/
Source0:        https://nginx.org/download/nginx-%{nginx_version}.tar.gz
Source1:        nginx.service

# 动态模块源码
Source2:        https://github.com/leev/ngx_http_geoip2_module/archive/refs/tags/%{geoip2_version}.tar.gz
Source3:        https://github.com/vozlt/nginx-module-vts/archive/refs/tags/v%{vts_version}.tar.gz
Source4:        https://github.com/vision5/ngx_devel_kit/archive/refs/tags/v%{devel_kit_version}.tar.gz
Source5:        https://github.com/openresty/lua-nginx-module/archive/refs/tags/v%{lua_nginx_version}.tar.gz
Source6:        https://github.com/openresty/lua-resty-core/archive/refs/tags/v%{lua_resty_core_version}.tar.gz
Source7:        https://github.com/openresty/lua-resty-lrucache/archive/refs/tags/v%{lua_resty_lrucache_version}.tar.gz

BuildArch:      x86_64
BuildRequires:  gcc, make, automake, autoconf, libtool
BuildRequires:  pcre-devel, zlib-devel, openssl-devel
BuildRequires:  systemd-devel, git, which
BuildRequires:  readline-devel, perl-ExtUtils-Embed
BuildRequires:  luajit-devel
Requires:       pcre, zlib, openssl, systemd
Requires:       luajit

%description
NGINX %{nginx_version} with systemd and dynamic module support.
Included dynamic modules:
- ngx_http_geoip2
- nginx-module-vts
- ngx_devel_kit
- lua-nginx-module
Bundled with lua-resty-core and lua-resty-lrucache for Lua support.

%prep
%setup -n nginx-%{nginx_version} -a 2 -a 3 -a 4 -a 5 -a 6 -a 7

# 重命名模块目录
mv ngx_http_geoip2_module-%{geoip2_version} ngx_http_geoip2_module
mv nginx-module-vts-v%{vts_version} nginx-module-vts
mv ngx_devel_kit-v%{devel_kit_version} ngx_devel_kit
mv lua-nginx-module-v%{lua_nginx_version} lua-nginx-module
mv lua-resty-core-v%{lua_resty_core_version} lua-resty-core
mv lua-resty-lrucache-v%{lua_resty_lrucache_version} lua-resty-lrucache

# 安装 systemd 服务文件
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/nginx.service

%build
export LUAJIT_LIB=/usr/lib64
export LUAJIT_INC=/usr/include/luajit-2.1

./configure \
    --prefix=%{_prefix}/nginx \
    --sbin-path=%{_sbindir}/nginx \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf \
    --pid-path=%{_rundir}/nginx.pid \
    --lock-path=%{_lockdir}/nginx.lock \
    --http-log-path=%{_localstatedir}/log/nginx/access.log \
    --error-log-path=%{_localstatedir}/log/nginx/error.log \
    --user=nginx \
    --group=nginx \
    --modules-path=%{_prefix}/nginx/modules \
    --with-compat \
    --with-file-aio \
    --with-threads \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_mp4_module \
    --with-http_random_index_module \
    --with-http_realip_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-stream \
    --with-stream_realip_module \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-google_perftools_module \
    --with-debug \
    --with-cc-opt="-DNGX_HTTP_HEADERS -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC" \
    --with-ld-opt="-Wl,-z,relro -Wl,-z,now -pie -Wl,--disable-new-dtags" \
    --add-dynamic-module=ngx_http_geoip2_module \
    --add-dynamic-module=nginx-module-vts \
    --add-dynamic-module=ngx_devel_kit \
    --add-dynamic-module=lua-nginx-module
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

# 创建目录
install -d %{buildroot}%{_lockdir}
install -d %{buildroot}%{_rundir}
install -d %{buildroot}%{_sysconfdir}/nginx
install -d %{buildroot}%{_sysconfdir}/systemd/system
install -d %{buildroot}%{_prefix}/nginx/modules
install -d %{buildroot}%{_prefix}/nginx/lib/lua
install -d %{buildroot}%{_localstatedir}/log/nginx
install -d %{buildroot}%{_localstatedir}/run

# 安装 Nginx
make install DESTDIR=%{buildroot}

# 安装配置文件
install -m 644 conf/nginx.conf %{buildroot}%{_sysconfdir}/nginx/nginx.conf
install -m 644 conf/mime.types %{buildroot}%{_sysconfdir}/nginx/mime.types

# 安装 Lua 库
cp -a lua-resty-core/lib/resty %{buildroot}%{_prefix}/nginx/lib/lua/
cp -a lua-resty-lrucache/lib/resty %{buildroot}%{_prefix}/nginx/lib/lua/

%files
%defattr(-,root,root,-)
%{_sbindir}/nginx
%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/systemd/system/nginx.service

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/systemd/system
%dir %{_localstatedir}/log/nginx
%dir %{_localstatedir}/run
%dir %{_prefix}/nginx
%dir %{_prefix}/nginx/modules
%dir %{_prefix}/nginx/lib/lua

%{_prefix}/nginx/modules/*.so
%{_prefix}/nginx/html/*
%{_prefix}/nginx/lib/lua/resty/*

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
- Auto-built with dynamic modules from online sources
- Modules: GeoIP2-%{geoip2_version}, VTS-%{vts_version}, NDK-%{devel_kit_version}, Lua-%{lua_nginx_version}
- Lua libraries: resty-core-%{lua_resty_core_version}, lrucache-%{lua_resty_lrucache_version}
