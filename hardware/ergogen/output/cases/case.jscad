function _case_base_ol_extrude_2_outline_fn(){
    return new CSG.Path2D([[140.5,-160],[182.5,-160]]).appendArc([184.5,-162],{"radius":2,"clockwise":true,"large":false}).appendPoint([184.5,-165.955]).appendArc([185.5,-166.955],{"radius":1,"clockwise":false,"large":false}).appendPoint([203.8042028,-166.955]).appendArc([204.0630218,-166.9890742],{"radius":1,"clockwise":true,"large":false}).appendPoint([220.5658791,-171.4110015]).appendArc([220.8070601,-171.5109019],{"radius":1,"clockwise":true,"large":false}).appendPoint([237.115022,-180.9263081]).appendArc([238.4810474,-180.5602827],{"radius":1,"clockwise":false,"large":false}).appendPoint([247.9595719,-164.1429967]).appendArc([248.0040989,-164.0695613],{"radius":2,"clockwise":true,"large":false}).appendPoint([254.1875238,-154.3487369]).appendArc([254.5,-153.2753015],{"radius":2,"clockwise":false,"large":false}).appendPoint([254.5,-105.8575]).appendArc([252.5,-103.8575],{"radius":2,"clockwise":false,"large":false}).appendPoint([234.5,-103.8575]).appendArc([232.5,-101.8575],{"radius":2,"clockwise":true,"large":false}).appendPoint([232.5,-95.8575]).appendArc([231.5,-94.8575],{"radius":1,"clockwise":false,"large":false}).appendPoint([215.5,-94.8575]).appendArc([214.5,-93.8575],{"radius":1,"clockwise":true,"large":false}).appendPoint([214.5,-93]).appendArc([213.5,-92],{"radius":1,"clockwise":false,"large":false}).appendPoint([197.5,-92]).appendArc([196.5,-91],{"radius":1,"clockwise":true,"large":false}).appendPoint([196.5,-88.2375]).appendArc([195.5,-87.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([176.5,-87.2375]).appendArc([175.5,-88.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([175.5,-91]).appendArc([174.5,-92],{"radius":1,"clockwise":true,"large":false}).appendPoint([158.5,-92]).appendArc([157.5,-93],{"radius":1,"clockwise":false,"large":false}).appendPoint([157.5,-105]).appendArc([156.5,-106],{"radius":1,"clockwise":true,"large":false}).appendPoint([140.5,-106]).appendArc([139.5,-107],{"radius":1,"clockwise":false,"large":false}).appendPoint([139.5,-159]).appendArc([140.5,-160],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    CAG.circle({"center":[234.9371581,-154.6627043],"radius":1.5})
.union(
    CAG.circle({"center":[232,-113.3575],"radius":1.5})
).union(
    CAG.circle({"center":[172.5,-152],"radius":1.5})
).union(
    CAG.circle({"center":[160,-108.5333333],"radius":1.5})
)).extrude({ offset: [0, 0, 2] });
}


function _wall_ring_ol_extrude_9_outline_fn(){
    return new CSG.Path2D([[137.5,-162],[178.5,-162]]).appendArc([182.5,-166],{"radius":4,"clockwise":true,"large":false}).appendPoint([182.5,-167.955]).appendArc([183.5,-168.955],{"radius":1,"clockwise":false,"large":false}).appendPoint([203.5408976,-168.955]).appendArc([203.7997166,-168.9890742],{"radius":1,"clockwise":true,"large":false}).appendPoint([219.7939081,-173.2747049]).appendArc([220.0350891,-173.3746053],{"radius":1,"clockwise":true,"large":false}).appendPoint([237.8470728,-183.6583589]).appendArc([239.2130982,-183.2923335],{"radius":1,"clockwise":false,"large":false}).appendPoint([250.7130982,-163.3737493]).appendPoint([255.6694418,-156.9362608]).appendArc([256.5,-154.4960478],{"radius":4,"clockwise":false,"large":false}).appendPoint([256.5,-101.8575]).appendPoint([238.5,-101.8575]).appendArc([234.5,-97.8575],{"radius":4,"clockwise":true,"large":false}).appendPoint([234.5,-93.8575]).appendArc([233.5,-92.8575],{"radius":1,"clockwise":false,"large":false}).appendPoint([217.5,-92.8575]).appendArc([216.5,-91.8575],{"radius":1,"clockwise":true,"large":false}).appendPoint([216.5,-91]).appendArc([215.5,-90],{"radius":1,"clockwise":false,"large":false}).appendPoint([199.5,-90]).appendArc([198.5,-89],{"radius":1,"clockwise":true,"large":false}).appendPoint([198.5,-86.2375]).appendArc([197.5,-85.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([174.5,-85.2375]).appendArc([173.5,-86.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([173.5,-89]).appendArc([172.5,-90],{"radius":1,"clockwise":true,"large":false}).appendPoint([156.5,-90]).appendArc([155.5,-91],{"radius":1,"clockwise":false,"large":false}).appendPoint([155.5,-103]).appendArc([154.5,-104],{"radius":1,"clockwise":true,"large":false}).appendPoint([138.5,-104]).appendArc([137.5,-105],{"radius":1,"clockwise":false,"large":false}).appendPoint([137.5,-161]).appendArc([137.8462811,-161.7567375],{"radius":1,"clockwise":false,"large":false}).appendPoint([137.5,-162]).close().innerToCAG()
.subtract(
    new CSG.Path2D([[140.5,-160],[182.5,-160]]).appendArc([184.5,-162],{"radius":2,"clockwise":true,"large":false}).appendPoint([184.5,-165.955]).appendArc([185.5,-166.955],{"radius":1,"clockwise":false,"large":false}).appendPoint([203.8042028,-166.955]).appendArc([204.0630218,-166.9890742],{"radius":1,"clockwise":true,"large":false}).appendPoint([220.5658791,-171.4110015]).appendArc([220.8070601,-171.5109019],{"radius":1,"clockwise":true,"large":false}).appendPoint([237.115022,-180.9263081]).appendArc([238.4810474,-180.5602827],{"radius":1,"clockwise":false,"large":false}).appendPoint([247.9595719,-164.1429967]).appendArc([248.0040989,-164.0695613],{"radius":2,"clockwise":true,"large":false}).appendPoint([254.1875238,-154.3487369]).appendArc([254.5,-153.2753015],{"radius":2,"clockwise":false,"large":false}).appendPoint([254.5,-105.8575]).appendArc([252.5,-103.8575],{"radius":2,"clockwise":false,"large":false}).appendPoint([234.5,-103.8575]).appendArc([232.5,-101.8575],{"radius":2,"clockwise":true,"large":false}).appendPoint([232.5,-95.8575]).appendArc([231.5,-94.8575],{"radius":1,"clockwise":false,"large":false}).appendPoint([215.5,-94.8575]).appendArc([214.5,-93.8575],{"radius":1,"clockwise":true,"large":false}).appendPoint([214.5,-93]).appendArc([213.5,-92],{"radius":1,"clockwise":false,"large":false}).appendPoint([197.5,-92]).appendArc([196.5,-91],{"radius":1,"clockwise":true,"large":false}).appendPoint([196.5,-88.2375]).appendArc([195.5,-87.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([176.5,-87.2375]).appendArc([175.5,-88.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([175.5,-91]).appendArc([174.5,-92],{"radius":1,"clockwise":true,"large":false}).appendPoint([158.5,-92]).appendArc([157.5,-93],{"radius":1,"clockwise":false,"large":false}).appendPoint([157.5,-105]).appendArc([156.5,-106],{"radius":1,"clockwise":true,"large":false}).appendPoint([140.5,-106]).appendArc([139.5,-107],{"radius":1,"clockwise":false,"large":false}).appendPoint([139.5,-159]).appendArc([140.5,-160],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
).extrude({ offset: [0, 0, 9] });
}


function _standoff_ol_extrude_4_outline_fn(){
    return CAG.circle({"center":[234.9371581,-154.6627043],"radius":2.5})
.union(
    CAG.circle({"center":[232,-113.3575],"radius":2.5})
).union(
    CAG.circle({"center":[172.5,-152],"radius":2.5})
).union(
    CAG.circle({"center":[160,-108.5333333],"radius":2.5})
).extrude({ offset: [0, 0, 4] });
}


function _holes_ol_extrude_9_outline_fn(){
    return CAG.circle({"center":[234.9371581,-154.6627043],"radius":1.5})
.union(
    CAG.circle({"center":[232,-113.3575],"radius":1.5})
).union(
    CAG.circle({"center":[172.5,-152],"radius":1.5})
).union(
    CAG.circle({"center":[160,-108.5333333],"radius":1.5})
).extrude({ offset: [0, 0, 9] });
}


function _switch_wall_cutout_ol_extrude_9_outline_fn(){
    return new CSG.Path2D([[253,-152.8575],[257,-152.8575]]).appendPoint([257,-144.8575]).appendPoint([253,-144.8575]).appendPoint([253,-152.8575]).close().innerToCAG()
.extrude({ offset: [0, 0, 9] });
}


function _usb_wall_cutout_ol_extrude_9_outline_fn(){
    return new CSG.Path2D([[238.5,-105.8575],[249.5,-105.8575]]).appendPoint([249.5,-99.8575]).appendPoint([238.5,-99.8575]).appendPoint([238.5,-105.8575]).close().innerToCAG()
.extrude({ offset: [0, 0, 9] });
}




                function _case_base_case_fn() {
                    

                // creating part 0 of case _case_base
                let _case_base__part_0 = _case_base_ol_extrude_2_outline_fn();

                // make sure that rotations are relative
                let _case_base__part_0_bounds = _case_base__part_0.getBounds();
                let _case_base__part_0_x = _case_base__part_0_bounds[0].x + (_case_base__part_0_bounds[1].x - _case_base__part_0_bounds[0].x) / 2
                let _case_base__part_0_y = _case_base__part_0_bounds[0].y + (_case_base__part_0_bounds[1].y - _case_base__part_0_bounds[0].y) / 2
                _case_base__part_0 = translate([-_case_base__part_0_x, -_case_base__part_0_y, 0], _case_base__part_0);
                _case_base__part_0 = rotate([0,0,0], _case_base__part_0);
                _case_base__part_0 = translate([_case_base__part_0_x, _case_base__part_0_y, 0], _case_base__part_0);

                _case_base__part_0 = translate([0,0,0], _case_base__part_0);
                let result = _case_base__part_0;
                
            
                    return result;
                }
            
            

                function _case_walls_case_fn() {
                    

                // creating part 0 of case _case_walls
                let _case_walls__part_0 = _wall_ring_ol_extrude_9_outline_fn();

                // make sure that rotations are relative
                let _case_walls__part_0_bounds = _case_walls__part_0.getBounds();
                let _case_walls__part_0_x = _case_walls__part_0_bounds[0].x + (_case_walls__part_0_bounds[1].x - _case_walls__part_0_bounds[0].x) / 2
                let _case_walls__part_0_y = _case_walls__part_0_bounds[0].y + (_case_walls__part_0_bounds[1].y - _case_walls__part_0_bounds[0].y) / 2
                _case_walls__part_0 = translate([-_case_walls__part_0_x, -_case_walls__part_0_y, 0], _case_walls__part_0);
                _case_walls__part_0 = rotate([0,0,0], _case_walls__part_0);
                _case_walls__part_0 = translate([_case_walls__part_0_x, _case_walls__part_0_y, 0], _case_walls__part_0);

                _case_walls__part_0 = translate([0,0,0], _case_walls__part_0);
                let result = _case_walls__part_0;
                
            
                    return result;
                }
            
            

                function _case_standoffs_case_fn() {
                    

                // creating part 0 of case _case_standoffs
                let _case_standoffs__part_0 = _standoff_ol_extrude_4_outline_fn();

                // make sure that rotations are relative
                let _case_standoffs__part_0_bounds = _case_standoffs__part_0.getBounds();
                let _case_standoffs__part_0_x = _case_standoffs__part_0_bounds[0].x + (_case_standoffs__part_0_bounds[1].x - _case_standoffs__part_0_bounds[0].x) / 2
                let _case_standoffs__part_0_y = _case_standoffs__part_0_bounds[0].y + (_case_standoffs__part_0_bounds[1].y - _case_standoffs__part_0_bounds[0].y) / 2
                _case_standoffs__part_0 = translate([-_case_standoffs__part_0_x, -_case_standoffs__part_0_y, 0], _case_standoffs__part_0);
                _case_standoffs__part_0 = rotate([0,0,0], _case_standoffs__part_0);
                _case_standoffs__part_0 = translate([_case_standoffs__part_0_x, _case_standoffs__part_0_y, 0], _case_standoffs__part_0);

                _case_standoffs__part_0 = translate([0,0,0], _case_standoffs__part_0);
                let result = _case_standoffs__part_0;
                
            
                    return result;
                }
            
            

                function _case_holes_case_fn() {
                    

                // creating part 0 of case _case_holes
                let _case_holes__part_0 = _holes_ol_extrude_9_outline_fn();

                // make sure that rotations are relative
                let _case_holes__part_0_bounds = _case_holes__part_0.getBounds();
                let _case_holes__part_0_x = _case_holes__part_0_bounds[0].x + (_case_holes__part_0_bounds[1].x - _case_holes__part_0_bounds[0].x) / 2
                let _case_holes__part_0_y = _case_holes__part_0_bounds[0].y + (_case_holes__part_0_bounds[1].y - _case_holes__part_0_bounds[0].y) / 2
                _case_holes__part_0 = translate([-_case_holes__part_0_x, -_case_holes__part_0_y, 0], _case_holes__part_0);
                _case_holes__part_0 = rotate([0,0,0], _case_holes__part_0);
                _case_holes__part_0 = translate([_case_holes__part_0_x, _case_holes__part_0_y, 0], _case_holes__part_0);

                _case_holes__part_0 = translate([0,0,0], _case_holes__part_0);
                let result = _case_holes__part_0;
                
            
                    return result;
                }
            
            

                function _case_switch_cutout_case_fn() {
                    

                // creating part 0 of case _case_switch_cutout
                let _case_switch_cutout__part_0 = _switch_wall_cutout_ol_extrude_9_outline_fn();

                // make sure that rotations are relative
                let _case_switch_cutout__part_0_bounds = _case_switch_cutout__part_0.getBounds();
                let _case_switch_cutout__part_0_x = _case_switch_cutout__part_0_bounds[0].x + (_case_switch_cutout__part_0_bounds[1].x - _case_switch_cutout__part_0_bounds[0].x) / 2
                let _case_switch_cutout__part_0_y = _case_switch_cutout__part_0_bounds[0].y + (_case_switch_cutout__part_0_bounds[1].y - _case_switch_cutout__part_0_bounds[0].y) / 2
                _case_switch_cutout__part_0 = translate([-_case_switch_cutout__part_0_x, -_case_switch_cutout__part_0_y, 0], _case_switch_cutout__part_0);
                _case_switch_cutout__part_0 = rotate([0,0,0], _case_switch_cutout__part_0);
                _case_switch_cutout__part_0 = translate([_case_switch_cutout__part_0_x, _case_switch_cutout__part_0_y, 0], _case_switch_cutout__part_0);

                _case_switch_cutout__part_0 = translate([0,0,0], _case_switch_cutout__part_0);
                let result = _case_switch_cutout__part_0;
                
            
                    return result;
                }
            
            

                function _case_usb_cutout_case_fn() {
                    

                // creating part 0 of case _case_usb_cutout
                let _case_usb_cutout__part_0 = _usb_wall_cutout_ol_extrude_9_outline_fn();

                // make sure that rotations are relative
                let _case_usb_cutout__part_0_bounds = _case_usb_cutout__part_0.getBounds();
                let _case_usb_cutout__part_0_x = _case_usb_cutout__part_0_bounds[0].x + (_case_usb_cutout__part_0_bounds[1].x - _case_usb_cutout__part_0_bounds[0].x) / 2
                let _case_usb_cutout__part_0_y = _case_usb_cutout__part_0_bounds[0].y + (_case_usb_cutout__part_0_bounds[1].y - _case_usb_cutout__part_0_bounds[0].y) / 2
                _case_usb_cutout__part_0 = translate([-_case_usb_cutout__part_0_x, -_case_usb_cutout__part_0_y, 0], _case_usb_cutout__part_0);
                _case_usb_cutout__part_0 = rotate([0,0,0], _case_usb_cutout__part_0);
                _case_usb_cutout__part_0 = translate([_case_usb_cutout__part_0_x, _case_usb_cutout__part_0_y, 0], _case_usb_cutout__part_0);

                _case_usb_cutout__part_0 = translate([0,0,0], _case_usb_cutout__part_0);
                let result = _case_usb_cutout__part_0;
                
            
                    return result;
                }
            
            

                function case_case_fn() {
                    

                // creating part 0 of case case
                let case__part_0 = _case_base_case_fn();

                // make sure that rotations are relative
                let case__part_0_bounds = case__part_0.getBounds();
                let case__part_0_x = case__part_0_bounds[0].x + (case__part_0_bounds[1].x - case__part_0_bounds[0].x) / 2
                let case__part_0_y = case__part_0_bounds[0].y + (case__part_0_bounds[1].y - case__part_0_bounds[0].y) / 2
                case__part_0 = translate([-case__part_0_x, -case__part_0_y, 0], case__part_0);
                case__part_0 = rotate([0,0,0], case__part_0);
                case__part_0 = translate([case__part_0_x, case__part_0_y, 0], case__part_0);

                case__part_0 = translate([0,0,0], case__part_0);
                let result = case__part_0;
                
            

                // creating part 1 of case case
                let case__part_1 = _case_walls_case_fn();

                // make sure that rotations are relative
                let case__part_1_bounds = case__part_1.getBounds();
                let case__part_1_x = case__part_1_bounds[0].x + (case__part_1_bounds[1].x - case__part_1_bounds[0].x) / 2
                let case__part_1_y = case__part_1_bounds[0].y + (case__part_1_bounds[1].y - case__part_1_bounds[0].y) / 2
                case__part_1 = translate([-case__part_1_x, -case__part_1_y, 0], case__part_1);
                case__part_1 = rotate([0,0,0], case__part_1);
                case__part_1 = translate([case__part_1_x, case__part_1_y, 0], case__part_1);

                case__part_1 = translate([0,0,0], case__part_1);
                result = result.union(case__part_1);
                
            

                // creating part 2 of case case
                let case__part_2 = _case_standoffs_case_fn();

                // make sure that rotations are relative
                let case__part_2_bounds = case__part_2.getBounds();
                let case__part_2_x = case__part_2_bounds[0].x + (case__part_2_bounds[1].x - case__part_2_bounds[0].x) / 2
                let case__part_2_y = case__part_2_bounds[0].y + (case__part_2_bounds[1].y - case__part_2_bounds[0].y) / 2
                case__part_2 = translate([-case__part_2_x, -case__part_2_y, 0], case__part_2);
                case__part_2 = rotate([0,0,0], case__part_2);
                case__part_2 = translate([case__part_2_x, case__part_2_y, 0], case__part_2);

                case__part_2 = translate([0,0,0], case__part_2);
                result = result.union(case__part_2);
                
            

                // creating part 3 of case case
                let case__part_3 = _case_holes_case_fn();

                // make sure that rotations are relative
                let case__part_3_bounds = case__part_3.getBounds();
                let case__part_3_x = case__part_3_bounds[0].x + (case__part_3_bounds[1].x - case__part_3_bounds[0].x) / 2
                let case__part_3_y = case__part_3_bounds[0].y + (case__part_3_bounds[1].y - case__part_3_bounds[0].y) / 2
                case__part_3 = translate([-case__part_3_x, -case__part_3_y, 0], case__part_3);
                case__part_3 = rotate([0,0,0], case__part_3);
                case__part_3 = translate([case__part_3_x, case__part_3_y, 0], case__part_3);

                case__part_3 = translate([0,0,0], case__part_3);
                result = result.subtract(case__part_3);
                
            

                // creating part 4 of case case
                let case__part_4 = _case_switch_cutout_case_fn();

                // make sure that rotations are relative
                let case__part_4_bounds = case__part_4.getBounds();
                let case__part_4_x = case__part_4_bounds[0].x + (case__part_4_bounds[1].x - case__part_4_bounds[0].x) / 2
                let case__part_4_y = case__part_4_bounds[0].y + (case__part_4_bounds[1].y - case__part_4_bounds[0].y) / 2
                case__part_4 = translate([-case__part_4_x, -case__part_4_y, 0], case__part_4);
                case__part_4 = rotate([0,0,0], case__part_4);
                case__part_4 = translate([case__part_4_x, case__part_4_y, 0], case__part_4);

                case__part_4 = translate([0,0,0], case__part_4);
                result = result.subtract(case__part_4);
                
            

                // creating part 5 of case case
                let case__part_5 = _case_usb_cutout_case_fn();

                // make sure that rotations are relative
                let case__part_5_bounds = case__part_5.getBounds();
                let case__part_5_x = case__part_5_bounds[0].x + (case__part_5_bounds[1].x - case__part_5_bounds[0].x) / 2
                let case__part_5_y = case__part_5_bounds[0].y + (case__part_5_bounds[1].y - case__part_5_bounds[0].y) / 2
                case__part_5 = translate([-case__part_5_x, -case__part_5_y, 0], case__part_5);
                case__part_5 = rotate([0,0,0], case__part_5);
                case__part_5 = translate([case__part_5_x, case__part_5_y, 0], case__part_5);

                case__part_5 = translate([0,0,0], case__part_5);
                result = result.subtract(case__part_5);
                
            
                    return result;
                }
            
            
        
            function main() {
                return case_case_fn();
            }

        