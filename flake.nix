{
  inputs = {
    # nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

    zmk-nix = {
      url = "github:lilyinstarlight/zmk-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    # This pins requirements.txt provided by zephyr-nix.pythonEnv.
    zephyr = {
      url = "github:zmkfirmware/zephyr/v3.5.0+zmk-fixes";
      flake = false;
    };
    # Zephyr sdk and toolchain.
    zephyr-nix = {
      url = "github:urob/zephyr-nix";
      inputs = {
        zephyr.follows = "zephyr";
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      zmk-nix,
      ...
    }:
    let
      forAllSystems = nixpkgs.lib.genAttrs (nixpkgs.lib.attrNames zmk-nix.packages);
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        rec {
          # default = firmware;

          # firmware = pkgs.callPackage ./nix/lilyinstarlight-zmk-package.nix {
          #   inherit
          #     system
          #     self
          #     zmk-nix
          #     ;
          #   # board = "nice_nano_v2";
          #   # shield = "cradio_%PART%";
          # };

          # flash = zmk-nix.packages.${system}.flash.override { inherit firmware; };

          # layoutImage = pkgs.callPackage ./nix/layout-img-package.nix { };
        }
      );
      devShells = forAllSystems (
        system:
        let
          pkgs = inputs.nixpkgs.legacyPackages.${system};
          zephyr = inputs.zephyr-nix.packages.${system};
          # keymap_drawer = pkgs.python3Packages.callPackage ./nix/keymap-drawer.nix { };
        in
        {
          zmk-nix-shell = zmk-nix.devShells.${system}.default;
          default = pkgs.mkShellNoCC {
            packages = [
              zephyr.pythonEnv
              (zephyr.sdk-0_16.override { targets = [ "arm-zephyr-eabi" ]; })

              pkgs.cmake
              pkgs.dtc
              pkgs.gcc
              pkgs.ninja

              pkgs.just
              pkgs.yq # Make sure yq resolves to python-yq.

              # keymap_drawer

              # -- Used by just_recipes and west_commands. Most systems already have them. --
              # pkgs.gawk
              # pkgs.unixtools.column
              # pkgs.coreutils # cp, cut, echo, mkdir, sort, tail, tee, uniq, wc
              # pkgs.diffutils
              # pkgs.findutils # find, xargs
              # pkgs.gnugrep
              # pkgs.gnused

              # nix
              pkgs.nixd
              pkgs.nixfmt-rfc-style
            ];

            shellHook = ''
              export ZMK_BUILD_DIR=$(pwd)/.build;
              export ZMK_SRC_DIR=$(pwd)/zmk/app;
            '';
          };
        }
      );

    };
}
