function _min_ol_extrude_3_outline_fn(){
    return new CSG.Path2D([[140.5683688,-161.9287188],[161.000367,-159.0571887]]).appendArc([161.7220668,-159.0874844],{"radius":2,"clockwise":true,"large":false}).appendPoint([191.8864879,-165.9448459]).appendArc([192.3298415,-165.9946055],{"radius":2,"clockwise":false,"large":false}).appendPoint([227.1053723,-165.9946055]).appendArc([228.1053723,-166.9946055],{"radius":1,"clockwise":true,"large":false}).appendPoint([228.1053723,-174.9946055]).appendArc([229.1053723,-175.9946055],{"radius":1,"clockwise":false,"large":false}).appendPoint([249.1053723,-175.9946055]).appendArc([250.1053723,-174.9946055],{"radius":1,"clockwise":false,"large":false}).appendPoint([250.1053723,-173.995238]).appendPoint([250.1053724,-91.9946056]).appendArc([248.1053724,-89.9946056],{"radius":2,"clockwise":false,"large":false}).appendPoint([197.1053724,-89.9946055]).appendArc([196.1053724,-88.9946055],{"radius":1,"clockwise":true,"large":false}).appendPoint([196.1053724,-86.2316055]).appendArc([195.1053724,-85.2316055],{"radius":1,"clockwise":false,"large":false}).appendPoint([175.1053724,-85.2316055]).appendArc([174.1053724,-86.2316055],{"radius":1,"clockwise":false,"large":false}).appendPoint([174.1053724,-89.7342516]).appendArc([173.1751289,-90.7318156],{"radius":1,"clockwise":true,"large":false}).appendPoint([153.4041018,-92.1143406]).appendArc([152.4762943,-93.1816612],{"radius":1,"clockwise":false,"large":false}).appendPoint([153.209862,-103.6721707]).appendArc([152.351471,-104.7321953],{"radius":1,"clockwise":true,"large":false}).appendPoint([132.9138483,-107.463975]).appendArc([132.0627533,-108.5934162],{"radius":1,"clockwise":false,"large":false}).appendPoint([139.4389276,-161.0776238]).appendArc([140.5683688,-161.9287188],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 3] });
}


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




                function bottom_cs_case_fn() {
                    

                // creating part 0 of case bottom_cs
                let bottom_cs__part_0 = _min_ol_extrude_3_outline_fn();

                // make sure that rotations are relative
                let bottom_cs__part_0_bounds = bottom_cs__part_0.getBounds();
                let bottom_cs__part_0_x = bottom_cs__part_0_bounds[0].x + (bottom_cs__part_0_bounds[1].x - bottom_cs__part_0_bounds[0].x) / 2
                let bottom_cs__part_0_y = bottom_cs__part_0_bounds[0].y + (bottom_cs__part_0_bounds[1].y - bottom_cs__part_0_bounds[0].y) / 2
                bottom_cs__part_0 = translate([-bottom_cs__part_0_x, -bottom_cs__part_0_y, 0], bottom_cs__part_0);
                bottom_cs__part_0 = rotate([0,0,0], bottom_cs__part_0);
                bottom_cs__part_0 = translate([bottom_cs__part_0_x, bottom_cs__part_0_y, 0], bottom_cs__part_0);

                bottom_cs__part_0 = translate([0,0,0], bottom_cs__part_0);
                let result = bottom_cs__part_0;
                
            
                    return result;
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
            
            

                function case_cs_case_fn() {
                    

                // creating part 0 of case case_cs
                let case_cs__part_0 = bottom_cs_case_fn();

                // make sure that rotations are relative
                let case_cs__part_0_bounds = case_cs__part_0.getBounds();
                let case_cs__part_0_x = case_cs__part_0_bounds[0].x + (case_cs__part_0_bounds[1].x - case_cs__part_0_bounds[0].x) / 2
                let case_cs__part_0_y = case_cs__part_0_bounds[0].y + (case_cs__part_0_bounds[1].y - case_cs__part_0_bounds[0].y) / 2
                case_cs__part_0 = translate([-case_cs__part_0_x, -case_cs__part_0_y, 0], case_cs__part_0);
                case_cs__part_0 = rotate([0,0,0], case_cs__part_0);
                case_cs__part_0 = translate([case_cs__part_0_x, case_cs__part_0_y, 0], case_cs__part_0);

                case_cs__part_0 = translate([0,0,0], case_cs__part_0);
                let result = case_cs__part_0;
                
            

                // creating part 1 of case case_cs
                let case_cs__part_1 = standoff_cs_case_fn();

                // make sure that rotations are relative
                let case_cs__part_1_bounds = case_cs__part_1.getBounds();
                let case_cs__part_1_x = case_cs__part_1_bounds[0].x + (case_cs__part_1_bounds[1].x - case_cs__part_1_bounds[0].x) / 2
                let case_cs__part_1_y = case_cs__part_1_bounds[0].y + (case_cs__part_1_bounds[1].y - case_cs__part_1_bounds[0].y) / 2
                case_cs__part_1 = translate([-case_cs__part_1_x, -case_cs__part_1_y, 0], case_cs__part_1);
                case_cs__part_1 = rotate([0,0,0], case_cs__part_1);
                case_cs__part_1 = translate([case_cs__part_1_x, case_cs__part_1_y, 0], case_cs__part_1);

                case_cs__part_1 = translate([0,0,0], case_cs__part_1);
                result = result.union(case_cs__part_1);
                
            

                // creating part 2 of case case_cs
                let case_cs__part_2 = holes_cs_case_fn();

                // make sure that rotations are relative
                let case_cs__part_2_bounds = case_cs__part_2.getBounds();
                let case_cs__part_2_x = case_cs__part_2_bounds[0].x + (case_cs__part_2_bounds[1].x - case_cs__part_2_bounds[0].x) / 2
                let case_cs__part_2_y = case_cs__part_2_bounds[0].y + (case_cs__part_2_bounds[1].y - case_cs__part_2_bounds[0].y) / 2
                case_cs__part_2 = translate([-case_cs__part_2_x, -case_cs__part_2_y, 0], case_cs__part_2);
                case_cs__part_2 = rotate([0,0,0], case_cs__part_2);
                case_cs__part_2 = translate([case_cs__part_2_x, case_cs__part_2_y, 0], case_cs__part_2);

                case_cs__part_2 = translate([0,0,0], case_cs__part_2);
                result = result.subtract(case_cs__part_2);
                
            
                    return result;
                }
            
            
        
            function main() {
                return case_cs_case_fn();
            }

        