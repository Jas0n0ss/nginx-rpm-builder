#!/bin/bash
set -euo pipefail

# Ensure BUILD_TARGET is set
if [[ -z "${BUILD_TARGET:-}" ]]; then
  echo "❌ Error: BUILD_TARGET is not set"
  exit 1
fi

# Define paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RPMBUILD="/home/builder/rpmbuild"

# Version functions
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
  echo "1.27.1.2"  # From openresty.org
}

# Parse build target
case "${BUILD_TARGET}" in
  nginx-1.25.0)
    VERSION="1.25.0"
    SPEC_FILE="nginx.spec"
    ;;
  nginx-latest)
    VERSION=$(get_nginx_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ Failed to get Nginx stable version"; exit 1; }
    SPEC_FILE="nginx.spec"
    ;;
  tengine-latest)
    VERSION=$(get_tengine_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ Failed to get Tengine stable version"; exit 1; }
    SPEC_FILE="tengine.spec"
    ;;
  openresty-latest)
    VERSION=$(get_openresty_stable_version)
    [[ -z "$VERSION" ]] && { echo "❌ Failed to get OpenResty stable version"; exit 1; }
    SPEC_FILE="openresty.spec"
    ;;
  *)
    echo "❌ Unsupported target: $BUILD_TARGET"
    exit 1
    ;;
esac

echo "🔍 Build Target: $BUILD_TARGET"
echo "📦 Version: $VERSION"
echo "📄 Spec File: $SPEC_FILE"

# Copy and update spec
SPEC_SRC="build/specs/$SPEC_FILE"
SPEC_DST="$RPMBUILD/SPECS/$SPEC_FILE"
mkdir -p "$RPMBUILD/SPECS"

cp "$SPEC_SRC" "$SPEC_DST"

# Update version in spec
sed -i.bak "s/%{!?nginx_version: %global nginx_version .*/%{!?nginx_version: %global nginx_version $VERSION}/" "$SPEC_DST" 2>/dev/null || true
sed -i.bak "s/%{!?tengine_version: %global tengine_version .*/%{!?tengine_version: %global tengine_version $VERSION}/" "$SPEC_DST" 2>/dev/null || true
sed -i.bak "s/Version:.*/Version:        $VERSION/" "$SPEC_DST"
rm -f "$SPEC_DST.bak"

echo "✅ Updated $SPEC_DST with version $VERSION"

# Download main source
SOURCE_URL=$(grep "Source0" "$SPEC_DST" | awk '{print $2}' | \
  sed "s|%{nginx_version}|$VERSION|" | \
  sed "s|%{tengine_version}|$VERSION|" | \
  sed "s|%{version}|$VERSION|")

if [[ -z "$SOURCE_URL" ]]; then
  echo "❌ Failed to extract Source0 from spec"
  exit 1
fi

echo "📥 Downloading source: $SOURCE_URL"
wget -q --show-progress "$SOURCE_URL" -O "$RPMBUILD/SOURCES/$(basename "$SOURCE_URL")"
if [[ $? -ne 0 ]]; then
  echo "❌ Download failed"
  exit 1
fi

# Build RPM
echo "🔧 Building RPM..."
cd "$RPMBUILD"
rpmbuild -ba "SPECS/$SPEC_FILE" || exit 1

echo "🎉 Build completed! RPMs are in: $RPMBUILD/RPMS/x86_64/"
