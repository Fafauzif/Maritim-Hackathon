#!/bin/sh
# Montserrat (SIL OFL 1.1) from the official repository
set -e
cd "$(dirname "$0")/.." && mkdir -p fonts/montserrat
for w in ExtraLight Light Regular Medium SemiBold Bold LightItalic ExtraLightItalic; do
  curl -sfL -o fonts/montserrat/Montserrat-$w.ttf https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-$w.ttf
done
echo "fonts ok"
