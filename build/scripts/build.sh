#!/bin/bash
set -euo pipefail

# 使用绝对路径，避免 source 失败
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# ========================
# 版本获取函数
# ========================

get_nginx_stable_version() {
  curl -s http://nginx.org/download/ \
    | grep -o 'nginx-[0-9]*\.[0-9]*\.[0-9]*\.tar\.gz' \
    | sed 's/nginx-\(.*\)\.tar\.gz/\1/' \
    | awk -F. '$2 % 2 == 0' | sort -V | tail -1
}

get_tengine_stable_version() {
  curl -s https://api.github.com/repos/alibaba/tengine/releases \
    | jq -r 'map(select(.prerelease==false and .draft==false)) | sort_by(.tag_name | split(".") | map(tonumber)) | last.tag_name' \
    | sed 's/^v//'
}

get_openresty_stable_version() {
  curl -s https://openresty.org/en/download.html \
    | grep -o 'openresty-[0-9]*\.[0-9]*\.[0-9]*\.tar\.gz' \
    | grep -v 'beta\|rc' \
    | sed 's/openresty-\(.*\)\.tar\.gz/\1/' \
    | sort -V | tail -1
}

# ========================
# 构建目标解析
# ========================

# 确保 BUILD_TARGET 已定义
if [[ -z "${BUILD_TARGET:-}" ]]; then
  echo "❌ 错误：必须设置 BUILD_TARGET"
  echo "可用值: nginx-1.25.0, nginx-latest, tengine-latest, openresty-latest"
  exit 1
fi

case $BUILD_TARGET in
  nginx-1.25.0)
    VERSION="1.25.0"
    SOURCE_URL="http://nginx.org/download/nginx-$VERSION.tar.gz"
    SOURCE_FILE="nginx-$VERSION.tar.gz"
    SPEC_FILE="nginx.spec"
    ;;
  nginx-latest)
    VERSION=$(get_nginx_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ 无法获取 Nginx 稳定版"; exit 1; }
    SOURCE_URL="http://nginx.org/download/nginx-$VERSION.tar.gz"
    SOURCE_FILE="nginx-$VERSION.tar.gz"
    SPEC_FILE="nginx.spec"
    ;;
  tengine-latest)
    VERSION=$(get_tengine_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ 无法获取 Tengine 稳定版"; exit 1; }
    TAG="v$VERSION"
    # ✅ 修复：移除多余空格
    SOURCE_URL="https://github.com/alibaba/tengine/archive/refs/tags/$TAG.tar.gz"
    SOURCE_FILE="tengine-$VERSION.tar.gz"
    SPEC_FILE="tengine.spec"
    ;;
  openresty-latest)
    VERSION=$(get_openresty_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ 无法获取 OpenResty 稳定版"; exit 1; }
    # ✅ 修复：移除多余空格
    SOURCE_URL="https://openresty.org/download/openresty-$VERSION.tar.gz"
    SOURCE_FILE="openresty-$VERSION.tar.gz"
    SPEC_FILE="openresty.spec"
    ;;
  *)
    echo "❌ 不支持的目标: $BUILD_TARGET"
    echo "可用: nginx-1.25.0, nginx-latest, tengine-latest, openresty-latest"
    exit 1
    ;;
esac

echo "🔍 构建目标: $BUILD_TARGET"
echo "📦 版本: $VERSION"
echo "🌐 源码: $SOURCE_URL"

# ========================
# 动态更新 SPEC 文件
# ========================

SPEC_SRC="build/specs/$SPEC_FILE"
SPEC_DST="$RPMBUILD/SPECS/$SPEC_FILE"

cp "$SPEC_SRC" "$SPEC_DST"
sed -i.bak "s/^\(Version:[[:space:]]*\).*/\1$VERSION/" "$SPEC_DST" && rm -f "$SPEC_DST.bak"
echo "✅ 已更新 $SPEC_DST 中的 Version 为 $VERSION"

# ========================
# 下载源码
# ========================

echo "📥 下载源码: $SOURCE_FILE"
wget -q --show-progress "$SOURCE_URL" -O "$RPMBUILD/SOURCES/$SOURCE_FILE"
if [[ $? -ne 0 ]]; then
  echo "❌ 下载失败: $SOURCE_URL"
  exit 1
fi

# ========================
# 构建 RPM
# ========================

echo "🔧 开始构建 RPM..."
cd "$RPMBUILD"
rpmbuild -ba "SPECS/$SPEC_FILE"

echo "🎉 构建完成！RPM 位于: $RPMBUILD/RPMS/x86_64/"
