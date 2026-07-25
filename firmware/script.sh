# https://www.reddit.com/r/ErgoMechKeyboards/comments/1hkhyht/guide_building_zmk_firmware_locally_with_only_a/

# that you may need to run west update a few times for everything to be fetched.
# west init -l config && west update

# Export cmake prefix path
# export "CMAKE_PREFIX_PATH=/zmk-urchin/zephyr:$CMAKE_PREFIX_PATH"

rm -rf /workspaces/ergogenesis/firmware/*.uf2


# says to call it from zmk/app...

# redo init if the paths change..., call it multiple times

export Zephyr_DIR="/workspaces/ergogenesis/zephyr/share/zephyr-package/cmake"

mkdir -p "/workspaces/ergogenesis/.build/left"
CMAKE_PREFIX_PATH=/workspaces/ergogenesis/zephyr:$CMAKE_PREFIX_PATH west build \
  --pristine \
  --build-dir "/workspaces/ergogenesis/.build/left" \
  --board "nice_nano_v2" \
  --snippet "studio-rpc-usb-uart" \
  "/workspaces/ergogenesis/zmk/app" \
  -- \
  -DZMK_CONFIG="/workspaces/ergogenesis/config" \
  -DSHIELD="ergogenesis_left" \
  -DCONFIG_ZMK_STUDIO="y"

# west build -d /build/left -p -b "nice_nano_v2" \ -s /zmk-urchin/zmk/app \
# -- -DSHIELD="urchin_left nice_view_adapter nice_view" \ -DZMK_CONFIG="/zmk-urchin/config" \
# -DZMK_EXTRA_MODULES="/zmk-urchin/urchin-zmk-module"

# -DZMK_EXTRA_MODULES="/zmk-urchin/urchin-zmk-module"

# ZMK studio support
# I won't go into details here. But you'd need the following extra flags in appropriate places to build a studio-compatible firmware. -S studio-rpc-usb-uart \ -DCONFIG_ZMK_STUDIO=y \

mkdir -p "firmware"
if [[ -f "/workspaces/ergogenesis/.build/left/zephyr/zmk.uf2" ]]; then
  mkdir -p "firmware" && cp "/workspaces/ergogenesis/.build/left/zephyr/zmk.uf2" "firmware/zmk_left.uf2"
fi

mkdir -p "/workspaces/ergogenesis/.build/right"
west build \
  -p \
  --build-dir "/workspaces/ergogenesis/.build/right" \
  --board "nice_nano_v2" \
  --snippet "studio-rpc-usb-uart" \
  "/workspaces/ergogenesis/zmk/app" \
  -- \
  -DZMK_CONFIG="/workspaces/ergogenesis/config" \
  -DSHIELD="ergogenesis_right" \
  -DCONFIG_ZMK_STUDIO="y"

mkdir -p "firmware"
if [[ -f "/workspaces/ergogenesis/.build/right/zephyr/zmk.uf2" ]]; then
  mkdir -p "firmware" && cp "/workspaces/ergogenesis/.build/right/zephyr/zmk.uf2" "firmware/zmk_right.uf2"
fi
