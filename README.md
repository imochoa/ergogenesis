https://www.youtube.com/watch?v=X0gTMRLRNp0

# Refs
- https://docs.ergogen.xyz/
- [measure your hand](https://pashutk.com/ergopad/)
    - https://github.com/pashutk/ergopad

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
4. Start [freerouting](https://github.com/freerouting/freerouting)
    1. run it
6. save output as a Specctra SESSION in GUI `-routed.ses`
7. from kicad, with `.kicad_pcb` from before still open...
    1. `File > Import > Specctra Session`