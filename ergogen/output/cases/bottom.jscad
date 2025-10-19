function min-ol_extrude_3_outline_fn(){
    return new CSG.Path2D([[140.5683688,-161.9287188],[161.000367,-159.0571887]]).appendArc([161.7220668,-159.0874844],{"radius":2,"clockwise":true,"large":false}).appendPoint([191.8864879,-165.9448459]).appendArc([192.3298415,-165.9946055],{"radius":2,"clockwise":false,"large":false}).appendPoint([227.1053723,-165.9946055]).appendArc([228.1053723,-166.9946055],{"radius":1,"clockwise":true,"large":false}).appendPoint([228.1053723,-174.9946055]).appendArc([229.1053723,-175.9946055],{"radius":1,"clockwise":false,"large":false}).appendPoint([249.1053723,-175.9946055]).appendArc([250.1053723,-174.9946055],{"radius":1,"clockwise":false,"large":false}).appendPoint([250.1053723,-173.995238]).appendPoint([250.1053724,-91.9946056]).appendArc([248.1053724,-89.9946056],{"radius":2,"clockwise":false,"large":false}).appendPoint([197.1053724,-89.9946055]).appendArc([196.1053724,-88.9946055],{"radius":1,"clockwise":true,"large":false}).appendPoint([196.1053724,-86.2316055]).appendArc([195.1053724,-85.2316055],{"radius":1,"clockwise":false,"large":false}).appendPoint([175.1053724,-85.2316055]).appendArc([174.1053724,-86.2316055],{"radius":1,"clockwise":false,"large":false}).appendPoint([174.1053724,-89.7342516]).appendArc([173.1751289,-90.7318156],{"radius":1,"clockwise":true,"large":false}).appendPoint([153.4041018,-92.1143406]).appendArc([152.4762943,-93.1816612],{"radius":1,"clockwise":false,"large":false}).appendPoint([153.209862,-103.6721707]).appendArc([152.351471,-104.7321953],{"radius":1,"clockwise":true,"large":false}).appendPoint([132.9138483,-107.463975]).appendArc([132.0627533,-108.5934162],{"radius":1,"clockwise":false,"large":false}).appendPoint([139.4389276,-161.0776238]).appendArc([140.5683688,-161.9287188],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 3] });
}




                function bottom_case_fn() {
                    

                // creating part 0 of case bottom
                let bottom__part_0 = min-ol_extrude_3_outline_fn();

                // make sure that rotations are relative
                let bottom__part_0_bounds = bottom__part_0.getBounds();
                let bottom__part_0_x = bottom__part_0_bounds[0].x + (bottom__part_0_bounds[1].x - bottom__part_0_bounds[0].x) / 2
                let bottom__part_0_y = bottom__part_0_bounds[0].y + (bottom__part_0_bounds[1].y - bottom__part_0_bounds[0].y) / 2
                bottom__part_0 = translate([-bottom__part_0_x, -bottom__part_0_y, 0], bottom__part_0);
                bottom__part_0 = rotate([0,0,0], bottom__part_0);
                bottom__part_0 = translate([bottom__part_0_x, bottom__part_0_y, 0], bottom__part_0);

                bottom__part_0 = translate([0,0,0], bottom__part_0);
                let result = bottom__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return bottom_case_fn();
            }

        