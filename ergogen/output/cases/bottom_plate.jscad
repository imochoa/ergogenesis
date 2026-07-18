function bottom_plate_ol_extrude_2_outline_fn(){
    return new CSG.Path2D([[140.5,-160],[182.5,-160]]).appendArc([184.5,-162],{"radius":2,"clockwise":true,"large":false}).appendPoint([184.5,-165.955]).appendArc([185.5,-166.955],{"radius":1,"clockwise":false,"large":false}).appendPoint([203.8042028,-166.955]).appendArc([204.0630218,-166.9890742],{"radius":1,"clockwise":true,"large":false}).appendPoint([220.5658791,-171.4110015]).appendArc([220.8070601,-171.5109019],{"radius":1,"clockwise":true,"large":false}).appendPoint([237.115022,-180.9263081]).appendArc([238.4810474,-180.5602827],{"radius":1,"clockwise":false,"large":false}).appendPoint([247.9595719,-164.1429967]).appendArc([248.0040989,-164.0695613],{"radius":2,"clockwise":true,"large":false}).appendPoint([254.1875238,-154.3487369]).appendArc([254.5,-153.2753015],{"radius":2,"clockwise":false,"large":false}).appendPoint([254.5,-105.8575]).appendArc([252.5,-103.8575],{"radius":2,"clockwise":false,"large":false}).appendPoint([234.5,-103.8575]).appendArc([232.5,-101.8575],{"radius":2,"clockwise":true,"large":false}).appendPoint([232.5,-95.8575]).appendArc([231.5,-94.8575],{"radius":1,"clockwise":false,"large":false}).appendPoint([215.5,-94.8575]).appendArc([214.5,-93.8575],{"radius":1,"clockwise":true,"large":false}).appendPoint([214.5,-93]).appendArc([213.5,-92],{"radius":1,"clockwise":false,"large":false}).appendPoint([197.5,-92]).appendArc([196.5,-91],{"radius":1,"clockwise":true,"large":false}).appendPoint([196.5,-88.2375]).appendArc([195.5,-87.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([176.5,-87.2375]).appendArc([175.5,-88.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([175.5,-91]).appendArc([174.5,-92],{"radius":1,"clockwise":true,"large":false}).appendPoint([158.5,-92]).appendArc([157.5,-93],{"radius":1,"clockwise":false,"large":false}).appendPoint([157.5,-105]).appendArc([156.5,-106],{"radius":1,"clockwise":true,"large":false}).appendPoint([140.5,-106]).appendArc([139.5,-107],{"radius":1,"clockwise":false,"large":false}).appendPoint([139.5,-159]).appendArc([140.5,-160],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    CAG.circle({"center":[234.9371581,-154.6627042],"radius":1.5})
.union(
    CAG.circle({"center":[172.5,-152],"radius":1.5})
).union(
    CAG.circle({"center":[160,-108.5333333],"radius":1.5})
).union(
    new CSG.Path2D([[229.8666283,-162.4808944],[240.2589331,-168.4808944]]).appendPoint([242.7589331,-164.1507674]).appendPoint([232.3666283,-158.1507674]).appendPoint([229.8666283,-162.4808944]).close().innerToCAG()
).union(
    new CSG.Path2D([[209.9680885,-155.7856712],[221.5591984,-158.8914997]]).appendPoint([222.8532937,-154.0618706]).appendPoint([211.2621838,-150.9560421]).appendPoint([209.9680885,-155.7856712]).close().innerToCAG()
).union(
    new CSG.Path2D([[189,-154.605],[201,-154.605]]).appendPoint([201,-149.605]).appendPoint([189,-149.605]).appendPoint([189,-154.605]).close().innerToCAG()
).union(
    new CSG.Path2D([[216,-102.5075],[228,-102.5075]]).appendPoint([228,-97.5075]).appendPoint([216,-97.5075]).appendPoint([216,-102.5075]).close().innerToCAG()
).union(
    new CSG.Path2D([[216,-119.5075],[228,-119.5075]]).appendPoint([228,-114.5075]).appendPoint([216,-114.5075]).appendPoint([216,-119.5075]).close().innerToCAG()
).union(
    new CSG.Path2D([[216,-136.5075],[228,-136.5075]]).appendPoint([228,-131.5075]).appendPoint([216,-131.5075]).appendPoint([216,-136.5075]).close().innerToCAG()
).union(
    new CSG.Path2D([[198,-99.65],[210,-99.65]]).appendPoint([210,-94.65]).appendPoint([198,-94.65]).appendPoint([198,-99.65]).close().innerToCAG()
).union(
    new CSG.Path2D([[198,-116.65],[210,-116.65]]).appendPoint([210,-111.65]).appendPoint([198,-111.65]).appendPoint([198,-116.65]).close().innerToCAG()
).union(
    new CSG.Path2D([[198,-133.65],[210,-133.65]]).appendPoint([210,-128.65]).appendPoint([198,-128.65]).appendPoint([198,-133.65]).close().innerToCAG()
).union(
    new CSG.Path2D([[180,-94.8875],[192,-94.8875]]).appendPoint([192,-89.8875]).appendPoint([180,-89.8875]).appendPoint([180,-94.8875]).close().innerToCAG()
).union(
    new CSG.Path2D([[180,-111.8875],[192,-111.8875]]).appendPoint([192,-106.8875]).appendPoint([180,-106.8875]).appendPoint([180,-111.8875]).close().innerToCAG()
).union(
    new CSG.Path2D([[180,-128.8875],[192,-128.8875]]).appendPoint([192,-123.8875]).appendPoint([180,-123.8875]).appendPoint([180,-128.8875]).close().innerToCAG()
).union(
    new CSG.Path2D([[162,-99.65],[174,-99.65]]).appendPoint([174,-94.65]).appendPoint([162,-94.65]).appendPoint([162,-99.65]).close().innerToCAG()
).union(
    new CSG.Path2D([[162,-116.65],[174,-116.65]]).appendPoint([174,-111.65]).appendPoint([162,-111.65]).appendPoint([162,-116.65]).close().innerToCAG()
).union(
    new CSG.Path2D([[162,-133.65],[174,-133.65]]).appendPoint([174,-128.65]).appendPoint([162,-128.65]).appendPoint([162,-133.65]).close().innerToCAG()
).union(
    new CSG.Path2D([[144,-113.65],[156,-113.65]]).appendPoint([156,-108.65]).appendPoint([144,-108.65]).appendPoint([144,-113.65]).close().innerToCAG()
).union(
    new CSG.Path2D([[144,-130.65],[156,-130.65]]).appendPoint([156,-125.65]).appendPoint([144,-125.65]).appendPoint([144,-130.65]).close().innerToCAG()
).union(
    new CSG.Path2D([[144,-147.65],[156,-147.65]]).appendPoint([156,-142.65]).appendPoint([144,-142.65]).appendPoint([144,-147.65]).close().innerToCAG()
)).extrude({ offset: [0, 0, 2] });
}




                function bottom_plate_case_fn() {
                    

                // creating part 0 of case bottom_plate
                let bottom_plate__part_0 = bottom_plate_ol_extrude_2_outline_fn();

                // make sure that rotations are relative
                let bottom_plate__part_0_bounds = bottom_plate__part_0.getBounds();
                let bottom_plate__part_0_x = bottom_plate__part_0_bounds[0].x + (bottom_plate__part_0_bounds[1].x - bottom_plate__part_0_bounds[0].x) / 2
                let bottom_plate__part_0_y = bottom_plate__part_0_bounds[0].y + (bottom_plate__part_0_bounds[1].y - bottom_plate__part_0_bounds[0].y) / 2
                bottom_plate__part_0 = translate([-bottom_plate__part_0_x, -bottom_plate__part_0_y, 0], bottom_plate__part_0);
                bottom_plate__part_0 = rotate([0,0,0], bottom_plate__part_0);
                bottom_plate__part_0 = translate([bottom_plate__part_0_x, bottom_plate__part_0_y, 0], bottom_plate__part_0);

                bottom_plate__part_0 = translate([0,0,0], bottom_plate__part_0);
                let result = bottom_plate__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return bottom_plate_case_fn();
            }

        