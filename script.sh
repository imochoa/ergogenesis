rm -rf /workspaces/firmware/*.uf2

export Zephyr_DIR="/workspaces/zephyr/share/zephyr-package/cmake"

mkdir -p "/workspaces/.build/left"
west build \
  -p \
  --build-dir "/workspaces/.build/left" \
  --board "nice_nano_v2" \
  --snippet "studio-rpc-usb-uart" \
  "/workspaces/zmk/app" \
  -- \
  -DZMK_CONFIG="/workspaces/config" \
  -DSHIELD="ergogenesis_left" \
  -DCONFIG_ZMK_STUDIO="y"

mkdir -p "firmware"
if [[ -f "/workspaces/.build/left/zephyr/zmk.uf2" ]]; then
  mkdir -p "firmware" && cp "/workspaces/.build/left/zephyr/zmk.uf2" "firmware/zmk_left.uf2"
fi

mkdir -p "/workspaces/.build/right"
west build \
  -p \
  --build-dir "/workspaces/.build/right" \
  --board "nice_nano_v2" \
  --snippet "studio-rpc-usb-uart" \
  "/workspaces/zmk/app" \
  -- \
  -DZMK_CONFIG="/workspaces/config" \
  -DSHIELD="ergogenesis_right" \
  -DCONFIG_ZMK_STUDIO="y"

mkdir -p "firmware"
if [[ -f "/workspaces/.build/right/zephyr/zmk.uf2" ]]; then
  mkdir -p "firmware" && cp "/workspaces/.build/right/zephyr/zmk.uf2" "firmware/zmk_right.uf2"
fi
