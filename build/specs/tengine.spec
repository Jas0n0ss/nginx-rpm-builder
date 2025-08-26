Name:           tengine-custom
Version:        3.1.0
Release:        1%{?dist}
Summary:        Tengine with GeoIP2, VTS, Lua, and NDK modules
License:        BSD
URL:            https://tengine.taobao.org/
Source0:        https://github.com/alibaba/tengine/archive/refs/tags/v%{version}.tar.gz

# 动态模块源码（在线下载）
Source1:        https://github.com/leev/ngx_http_geoip2_module/archive/refs/tags/3.4.tar.gz
Source2:        https://github.com/vozlt/nginx-module-vts/archive/refs/tags/v0.2.2.tar.gz
Source3:        https://github.com/simplresty/ngx_devel_kit/archive/v0.3.4.tar.gz
Source4:        https://github.com/openresty/lua-nginx-module/archive/v0.10.28.tar.gz

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, libmaxminddb-devel, luajit luajit-devel, perl-ExtUtils-Embed
Requires:       pcre, zlib, openssl, libmaxminddb, luajit

%description
Custom Tengine build with dynamic modules:
- ngx_http_geoip2_module (GeoIP2)
- nginx-module-vts (traffic monitoring)
- ngx_devel_kit (NDK)
- lua-nginx-module (Lua scripting)

%prep
%setup -n tengine-%{version} -a 1 -a 2 -a 3 -a 4

# 重命名模块目录为预期名称
mv ngx_http_geoip2_module-3.4 ngx_http_geoip2_module
mv nginx-module-vts-v0.2.2 nginx-module-vts
mv ngx_devel_kit-v0.3.4 ngx_devel_kit
mv lua-nginx-module-v0.10.28 lua-nginx-module

%build
./configure \
    --prefix=/etc/tengine \
    --sbin-path=/usr/sbin/tengine \
    --modules-path=/usr/lib64/tengine/modules \
    --conf-path=/etc/tengine/nginx.conf \
    --error-log-path=/var/log/tengine/error.log \
    --http-log-path=/var/log/tengine/access.log \
    --pid-path=/var/run/tengine.pid \
    --lock-path=/var/run/tengine.lock \
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
* 05 Apr 2025 Builder <ci@example.com> - 3.1.0-1
- Auto-built with dynamic modules from online sources
