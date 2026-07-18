https://www.youtube.com/watch?v=X0gTMRLRNp0

# Refs
- https://docs.ergogen.xyz/
- [measure your hand](https://pashutk.com/ergopad/)
    - https://github.com/pashutk/ergopad


- flatfootfox but for my usecase:   I'd take a look at the Sweep-like example on https://ergogen.ceoloide.com/ (via the dropdown). It does the sort of direct-pin + GND setup you're looking for;

- Check out my Corney Island (https://github.com/ceoloide/corney-island), it's a 100% replica of the Corne but has support for other switches (I use Lofree switches and I am loving it)

# Similar boards
https://github.com/auryn31/avocado
https://github.com/Narkoleptika/josukey


## [Part 1: Units](https://flatfootfox.com/ergogen-part1-units-points/)
Play around on https://ergogen.ceoloide.com/

## [Part 2: Outlines](https://flatfootfox.com/ergogen-part2-outlines/)
- https://github.com/scipioni/clavis


## [Part 3: PCB](https://flatfootfox.com/ergogen-part3-pcbs/)


## [Part 4: ](https://flatfootfox.com/ergogen-part4-footprints-cases/)

https://github.com/freerouting/freerouting


# ferris reversible examples
https://github.com/davidphilipbarr/Sweep/tree/main/Sweep%20half-swept


# Routing
1. Generate `outputs/pcbs/*.kicad_pcb
2. start kicad (`pcbnew`)
    1. import `.kicad_pcb`
    2. save it to let KiCAD auto-convert the file to the newer kicad sytanx
3. `File > Export > Specctra DSN` to generate a `.dsn` file
    - save at `ergogenesis/ergogen/output/pcbs/shield-pcb.dsn`
4. Start [freerouting](https://github.com/freerouting/freerouting)
    1. run it
6. save output as a Specctra SESSION in GUI `-routed.ses`
7. from kicad, with `.kicad_pcb` from before still open...
    1. `File > Import > Specctra Session`

# 3D models

Component STEP models live in `ergogen/3dmodels/` and are wired into the
footprints in `ergogen/config.yaml` via each footprint's `*_3dmodel_filename`
params. The generated `output/pcbs/shield-pcb.kicad_pcb` references them with
the `${ERGOGEN_3DMODELS}` KiCad path variable.

Models (downloaded from github.com/Andreyod1/Axiom, the ScottoKeebs library):
- `choc_v1.step` — Kailh Choc V1 switch (PG1353)
- `choc_hotswap.step` — Choc hotswap socket
- `choc_keycap_1u.step` — MBK 1u keycap
- `supermini_nrf52840.step` — Nice!Nano V2 STEP as a SuperMini NRF52840
  stand-in (same Pro Micro form factor / USB-C; no public SuperMini STEP
  exists)
- `switch_msk12c02.step` — MSK12C02 / SSSS811101 side slide switch
- `jst_ph_s2b.step` — JST PH 2.0 side-entry battery connector (S2B-PH-K,
  from the KiCad standard library)

To make KiCad's 3D viewer resolve them, add the path variable once:
- KiCad -> Preferences -> Configure Paths... -> Add
  - Name:  `ERGOGEN_3DMODELS`
  - Value:  `<repo>/ergogen/3dmodels`

Then open `ergogen/output/pcbs/shield-pcb.kicad_pcb` -> View -> 3D Viewer.

# Cases & plates

The `cases:` section generates a sandwich case: the PCB sits between a
**stabilization (switch) plate** on top and a **base plate** on the bottom,
held together by M2 screws through the mounting holes.

- `switch_plate` / `switch_plate_ol.dxf` — top plate with Choc cutouts
  (13.8x13.8mm) at each key. The switch snaps into this plate so it can't
  fall out of the hotswap socket. 1.6mm thick (Choc clip engagement).
- `bottom_plate` / `bottom_plate_ol.dxf` — base plate with a clearance slot
  per key for the hotswap socket.

The DXFs (`output/outlines/`) are for laser/waterjet cutting the plates; the
`.jscad` cases (`output/cases/`) are 3D-printable extrusions. Convert jscad to
STL with:
```
just ergogen-stl-from-jscad
# or per file:
npx @jscad/cli@1 output/cases/switch_plate.jscad -of stla -o switch_plate.stl
```
Preview a plate outline:
```
just visualize-dxf ./output/outlines/switch_plate_ol.dxf
```

## Hotswap socket clearance (reversible board)

The Choc hotswap socket bridges the switch's central hole and a side hole on
the north side of each key. On this reversible footprint the socket sits
bottom-west when populated on the front and bottom-east when populated on the
back. Rather than generate two mirrored bases, the base uses one symmetric
12x5mm slot per key that covers **both** positions, so a single base works
for either side (and for both halves of a split where one PCB is flipped).

The slot size/position is controlled by `socket_cutout_w`, `socket_cutout_h`,
and `socket_cutout_y` in the `units:` section. If a socket fouls the base,
widening `socket_cutout_w` or raising `socket_cutout_y` gives more room.

## Notes / known gotchas

- The top-left mounting screw (`mountscrew_top_left`) sits ~2mm from the
  `pinky_top` key, so in the switch plate its hole merges into that key's
  Choc cutout. Move that screw (or the key) if you need a clean separate
  screw hole in the top plate. The base plate is unaffected.
- The case here is a bare sandwich (no walls). Walls can be added later by
  extruding an expanded outline and subtracting the board outline, à la the
  flatfootfox Part 4 case tutorial.

# ZMK
```
warning: Deprecated symbol NRF_STORE_REBOOT_TYPE_GPREGRET is enabled.
```



# Save container history

```
   0 drwxr-xr-x. 1 root   root    20 Jun  5  2024 ../
4.0K -rw-------. 1 ubuntu ubuntu 437 Nov 17 16:43 .bash_history
4.0K -rw-r--r--. 1 ubuntu ubuntu 220 Mar 31  2024 .bash_logout
4.0K -rw-r--r--. 1 root   root   475 Oct  4 14:44 .bashrc
   0 drwxr-xr-x. 5 ubuntu ubuntu  51 Nov 17 16:39 .cache/
   0 drwxr-xr-x. 3 ubuntu ubuntu  22 Nov 17 16:39 .cmake/
   0 drwxr-xr-x. 3 ubuntu ubuntu  20 Nov 17 16:30 .dotnet/
4.0K -rw-r--r--. 1 ubuntu ubuntu 760 Nov 17 16:39 .gitconfig
   0 drwx------. 2 ubuntu ubuntu  80 Nov 17 16:30 .gnupg/
   0 drwxr-xr-x. 1 root   root    17 Nov 17 15:32 .local/
4.0K -rw-r--r--. 1 ubuntu ubuntu 807 Mar 31  2024 .profile
   0 drwxr-xr-x. 2 ubuntu ubuntu  25 Nov 17 16:30 .ssh/
   0 drwxr-xr-x. 1 ubuntu ubuntu  70 Nov 17 16:30 .vscode-server/
   0 drwxr-xr-x. 1 ubuntu ubuntu   6 Nov 17 15:32 project/
```

# Reference

- https://github.com/ceoloide/corney-island
  - build in docker? https://github.com/ceoloide/corney-island/blob/main/build.sh
https://github.com/ceoloide/ergogen-footprints/tree/main
