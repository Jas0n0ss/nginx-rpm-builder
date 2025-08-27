#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

get_nginx_stable_version() {
  curl -s https://nginx.org/ \
    | grep -o 'nginx-[0-9]*\.[0-9]*\.[0-9]*' \
    | grep -o '[0-9]*\.[0-9]*\.[0-9]*' \
    | awk -F. '$2 % 2 == 0' | sort -V | tail -1
}

get_tengine_stable_version() {
  curl -s https://api.github.com/repos/alibaba/tengine/releases \
    | jq -r 'map(select(.prerelease==false and .draft==false)) | sort_by(.tag_name | split(".") | map(tonumber)) | last.tag_name' \
    | sed 's/^v//'
}

get_openresty_stable_version() {
  curl -s https://openresty.org/en/download.html \
    | grep -o 'openresty-[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\.tar\.gz' \
    | grep -v 'beta\|rc' \
    | sed 's/openresty-\(.*\)\.tar\.gz/\1/' \
    | sort -V | tail -1
}

case ${BUILD_TARGET:-} in
  nginx-1.25.0)
    VERSION="1.25.0"
    SPEC_FILE="nginx.spec"
    ;;
  nginx-latest)
    VERSION=$(get_nginx_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ 无法获取 Nginx 稳定版"; exit 1; }
    SPEC_FILE="nginx.spec"
    ;;
  tengine-latest)
    VERSION=$(get_tengine_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ 无法获取 Tengine 稳定版"; exit 1; }
    SPEC_FILE="tengine.spec"
    ;;
  openresty-latest)
    VERSION=$(get_openresty_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ 无法获取 OpenResty 稳定版"; exit 1; }
    SPEC_FILE="openresty.spec"
    ;;
  *)
    echo "❌ 不支持的目标: $BUILD_TARGET"
    exit 1
    ;;
esac

echo "🔍 构建目标: $BUILD_TARGET"
echo "📦 版本: $VERSION"

SPEC_SRC="build/specs/$SPEC_FILE"
SPEC_DST="$RPMBUILD/SPECS/$SPEC_FILE"

cp "$SPEC_SRC" "$SPEC_DST"

# 动态更新版本
sed -i.bak "s/%{!?nginx_version: %global nginx_version .*/%{!?nginx_version: %global nginx_version $VERSION}/" "$SPEC_DST" 2>/dev/null || true
sed -i.bak "s/%{!?tengine_version: %global tengine_version .*/%{!?tengine_version: %global tengine_version $VERSION}/" "$SPEC_DST" 2>/dev/null || true
sed -i.bak "s/Version:.*/Version:        $VERSION/" "$SPEC_DST"
rm -f "$SPEC_DST.bak"

echo "✅ 已更新 $SPEC_DST 中的版本为 $VERSION"

# 下载主源码
SOURCE_URL=$(grep "Source0" "$SPEC_DST" | awk '{print $2}' | sed "s|%{nginx_version}|$VERSION|" | sed "s|%{tengine_version}|$VERSION|" | sed "s|%{version}|$VERSION|")
echo "📥 下载源码: $SOURCE_URL"
wget -q --show-progress "$SOURCE_URL" -O "$RPMBUILD/SOURCES/$(basename "$SOURCE_URL")"

echo "🔧 开始构建 RPM..."
cd "$RPMBUILD"
rpmbuild -ba "SPECS/$SPEC_FILE"

echo "🎉 构建完成！RPM 位于: $RPMBUILD/RPMS/x86_64/"
