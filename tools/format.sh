#!/bin/sh
# Format (or check) the C sources with the pinned clang-format version.
#
#   tools/format.sh            # reformat all sources in place
#   tools/format.sh --check    # fail if any file is not formatted (used by CI)
#
# Install the pinned version with:  pip install clang-format==23.1.1
# (or use a virtualenv). Vendored code in third_party/ is never touched.
set -e
VERSION=23.1.1
CF=${CLANG_FORMAT:-clang-format}

have=$($CF --version 2>/dev/null | sed -n 's/.*version \([0-9.]*\).*/\1/p')
if [ "$have" != "$VERSION" ]; then
  echo "tools/format.sh: need clang-format $VERSION, found '${have:-none}'" >&2
  echo "  pip install clang-format==$VERSION   (or set CLANG_FORMAT=/path/to/it)" >&2
  exit 2
fi

cd "$(dirname "$0")/.."
files=$(git ls-files 'src/*.c' 'src/*.h' 'apps/*.c' 'apps/*.h')
if [ "$1" = "--check" ]; then
  # shellcheck disable=SC2086
  $CF --dry-run -Werror $files
  echo "all $(echo "$files" | wc -w) files formatted"
else
  # shellcheck disable=SC2086
  $CF -i $files
fi
