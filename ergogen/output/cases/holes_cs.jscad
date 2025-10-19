function _holes_ol_extrude_4_outline_fn(){
    return CAG.circle({"center":[232.1053723,-155.4946055],"radius":1.5})
.union(
    CAG.circle({"center":[212.1053723,-125.9946056],"radius":1.5})
).union(
    CAG.circle({"center":[212.1053723,-108.9946056],"radius":1.5})
).union(
    CAG.circle({"center":[155.9903988,-129.646251],"radius":1.5})
).union(
    CAG.circle({"center":[154.3182281,-111.7333352],"radius":1.5})
).extrude({ offset: [0, 0, 4] });
}




                function holes_cs_case_fn() {
                    

                // creating part 0 of case holes_cs
                let holes_cs__part_0 = _holes_ol_extrude_4_outline_fn();

                // make sure that rotations are relative
                let holes_cs__part_0_bounds = holes_cs__part_0.getBounds();
                let holes_cs__part_0_x = holes_cs__part_0_bounds[0].x + (holes_cs__part_0_bounds[1].x - holes_cs__part_0_bounds[0].x) / 2
                let holes_cs__part_0_y = holes_cs__part_0_bounds[0].y + (holes_cs__part_0_bounds[1].y - holes_cs__part_0_bounds[0].y) / 2
                holes_cs__part_0 = translate([-holes_cs__part_0_x, -holes_cs__part_0_y, 0], holes_cs__part_0);
                holes_cs__part_0 = rotate([0,0,0], holes_cs__part_0);
                holes_cs__part_0 = translate([holes_cs__part_0_x, holes_cs__part_0_y, 0], holes_cs__part_0);

                holes_cs__part_0 = translate([0,0,0], holes_cs__part_0);
                let result = holes_cs__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return holes_cs_case_fn();
            }

        