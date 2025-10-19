function _standoff_ol_extrude_4_outline_fn(){
    return CAG.circle({"center":[232.1053723,-155.4946055],"radius":2.5})
.union(
    CAG.circle({"center":[212.1053723,-125.9946056],"radius":2.5})
).union(
    CAG.circle({"center":[212.1053723,-108.9946056],"radius":2.5})
).union(
    CAG.circle({"center":[155.9903988,-129.646251],"radius":2.5})
).union(
    CAG.circle({"center":[154.3182281,-111.7333352],"radius":2.5})
).extrude({ offset: [0, 0, 4] });
}




                function standoff_cs_case_fn() {
                    

                // creating part 0 of case standoff_cs
                let standoff_cs__part_0 = _standoff_ol_extrude_4_outline_fn();

                // make sure that rotations are relative
                let standoff_cs__part_0_bounds = standoff_cs__part_0.getBounds();
                let standoff_cs__part_0_x = standoff_cs__part_0_bounds[0].x + (standoff_cs__part_0_bounds[1].x - standoff_cs__part_0_bounds[0].x) / 2
                let standoff_cs__part_0_y = standoff_cs__part_0_bounds[0].y + (standoff_cs__part_0_bounds[1].y - standoff_cs__part_0_bounds[0].y) / 2
                standoff_cs__part_0 = translate([-standoff_cs__part_0_x, -standoff_cs__part_0_y, 0], standoff_cs__part_0);
                standoff_cs__part_0 = rotate([0,0,0], standoff_cs__part_0);
                standoff_cs__part_0 = translate([standoff_cs__part_0_x, standoff_cs__part_0_y, 0], standoff_cs__part_0);

                standoff_cs__part_0 = translate([0,0,0], standoff_cs__part_0);
                let result = standoff_cs__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return standoff_cs_case_fn();
            }

        