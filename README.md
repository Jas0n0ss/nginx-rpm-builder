# NGINX / Tengine / OpenResty RPM Builder

Automated RPM build system for RHEL9 with dynamic modules and Lua support.

## 🚀 Features
- 4 build targets: nginx-1.25.0, nginx-latest, tengine-latest, openresty-latest
- Dynamic modules: GeoIP2, VTS, NDK, Lua
- Built with LuaJIT
- CI/CD: Weekly auto-build at 04:00 UTC
- Manual trigger with target selection

## 📦 Build Locally
```bash
export BUILD_TARGET=nginx-latest
./build/scripts/build.sh
