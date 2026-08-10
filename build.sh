#!/usr/bin/env bash
# JuneGiri Farms — inline the shared partials into every page.
#
# The site has no build step, but shipping the header/footer as a client-side
# fetch() left crawlers with zero internal links (they only saw the empty
# <div data-include="header"></div> slot). This script bakes partials/*.html
# straight into the HTML so the nav and footer are in the server response.
#
# Edit partials/header.html or partials/footer.html, then run ./build.sh.
set -euo pipefail
cd "$(dirname "$0")"
python3 tools/inline-partials.py "$@"
python3 tools/add-schema.py
python3 tools/add-analytics.py "$@"
python3 tools/gen-sitemap.py
