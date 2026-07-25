function switch_plate_ol_extrude_1_6_outline_fn(){
    return new CSG.Path2D([[140.5,-160],[182.5,-160]]).appendArc([184.5,-162],{"radius":2,"clockwise":true,"large":false}).appendPoint([184.5,-165.955]).appendArc([185.5,-166.955],{"radius":1,"clockwise":false,"large":false}).appendPoint([203.8042028,-166.955]).appendArc([204.0630218,-166.9890742],{"radius":1,"clockwise":true,"large":false}).appendPoint([220.5658791,-171.4110015]).appendArc([220.8070601,-171.5109019],{"radius":1,"clockwise":true,"large":false}).appendPoint([237.115022,-180.9263081]).appendArc([238.4810474,-180.5602827],{"radius":1,"clockwise":false,"large":false}).appendPoint([247.9595719,-164.1429967]).appendArc([248.0040989,-164.0695613],{"radius":2,"clockwise":true,"large":false}).appendPoint([254.1875238,-154.3487369]).appendArc([254.5,-153.2753015],{"radius":2,"clockwise":false,"large":false}).appendPoint([254.5,-105.8575]).appendArc([252.5,-103.8575],{"radius":2,"clockwise":false,"large":false}).appendPoint([234.5,-103.8575]).appendArc([232.5,-101.8575],{"radius":2,"clockwise":true,"large":false}).appendPoint([232.5,-95.8575]).appendArc([231.5,-94.8575],{"radius":1,"clockwise":false,"large":false}).appendPoint([215.5,-94.8575]).appendArc([214.5,-93.8575],{"radius":1,"clockwise":true,"large":false}).appendPoint([214.5,-93]).appendArc([213.5,-92],{"radius":1,"clockwise":false,"large":false}).appendPoint([197.5,-92]).appendArc([196.5,-91],{"radius":1,"clockwise":true,"large":false}).appendPoint([196.5,-88.2375]).appendArc([195.5,-87.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([176.5,-87.2375]).appendArc([175.5,-88.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([175.5,-91]).appendArc([174.5,-92],{"radius":1,"clockwise":true,"large":false}).appendPoint([158.5,-92]).appendArc([157.5,-93],{"radius":1,"clockwise":false,"large":false}).appendPoint([157.5,-105]).appendArc([156.5,-106],{"radius":1,"clockwise":true,"large":false}).appendPoint([140.5,-106]).appendArc([139.5,-107],{"radius":1,"clockwise":false,"large":false}).appendPoint([139.5,-159]).appendArc([140.5,-160],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    CAG.circle({"center":[234.9371581,-154.6627043],"radius":1.5})
.union(
    CAG.circle({"center":[172.5,-152],"radius":1.5})
).union(
    new CSG.Path2D([[206.7046791,-164.487548],[220.0344555,-168.0592508]]).appendPoint([223.6061583,-154.7294744]).appendPoint([210.2763819,-151.1577716]).appendPoint([206.7046791,-164.487548]).close().innerToCAG()
).union(
    new CSG.Path2D([[215.1,-111.7575],[228.9,-111.7575]]).appendPoint([228.9,-97.9575]).appendPoint([215.1,-97.9575]).appendPoint([215.1,-111.7575]).close().innerToCAG()
).union(
    new CSG.Path2D([[215.1,-128.7575],[228.9,-128.7575]]).appendPoint([228.9,-114.9575]).appendPoint([215.1,-114.9575]).appendPoint([215.1,-128.7575]).close().innerToCAG()
).union(
    new CSG.Path2D([[197.1,-108.9],[210.9,-108.9]]).appendPoint([210.9,-95.1]).appendPoint([197.1,-95.1]).appendPoint([197.1,-108.9]).close().innerToCAG()
).union(
    new CSG.Path2D([[197.1,-125.9],[210.9,-125.9]]).appendPoint([210.9,-112.1]).appendPoint([197.1,-112.1]).appendPoint([197.1,-125.9]).close().innerToCAG()
).union(
    new CSG.Path2D([[179.1,-104.1375],[192.9,-104.1375]]).appendPoint([192.9,-90.3375]).appendPoint([179.1,-90.3375]).appendPoint([179.1,-104.1375]).close().innerToCAG()
).union(
    new CSG.Path2D([[179.1,-121.1375],[192.9,-121.1375]]).appendPoint([192.9,-107.3375]).appendPoint([179.1,-107.3375]).appendPoint([179.1,-121.1375]).close().innerToCAG()
).union(
    new CSG.Path2D([[179.1,-138.1375],[192.9,-138.1375]]).appendPoint([192.9,-124.3375]).appendPoint([179.1,-124.3375]).appendPoint([179.1,-138.1375]).close().innerToCAG()
).union(
    new CSG.Path2D([[161.1,-125.9],[174.9,-125.9]]).appendPoint([174.9,-112.1]).appendPoint([161.1,-112.1]).appendPoint([161.1,-125.9]).close().innerToCAG()
).union(
    new CSG.Path2D([[143.1,-122.9],[156.9,-122.9]]).appendPoint([156.9,-109.1]).appendPoint([143.1,-109.1]).appendPoint([143.1,-122.9]).close().innerToCAG()
).union(
    new CSG.Path2D([[143.1,-139.9],[156.9,-139.9]]).appendPoint([156.9,-126.1]).appendPoint([143.1,-126.1]).appendPoint([143.1,-139.9]).close().innerToCAG()
).union(
    new CSG.Path2D([[188.1,-163.855],[201.9,-163.855]]).appendPoint([201.9,-150.055]).appendPoint([188.1,-150.055]).appendPoint([188.1,-163.855]).close().innerToCAG()
).union(
    new CSG.Path2D([[215.1,-145.7575],[228.9,-145.7575]]).appendPoint([228.9,-131.9575]).appendPoint([215.1,-131.9575]).appendPoint([215.1,-145.7575]).close().innerToCAG()
).union(
    new CSG.Path2D([[197.1,-142.9],[210.9,-142.9]]).appendPoint([210.9,-129.1]).appendPoint([197.1,-129.1]).appendPoint([197.1,-142.9]).close().innerToCAG()
).union(
    new CSG.Path2D([[161.1,-142.9],[174.9,-142.9]]).appendPoint([174.9,-129.1]).appendPoint([161.1,-129.1]).appendPoint([161.1,-142.9]).close().innerToCAG()
).union(
    new CSG.Path2D([[143.1,-156.9],[156.9,-156.9]]).appendPoint([156.9,-143.1]).appendPoint([143.1,-143.1]).appendPoint([143.1,-156.9]).close().innerToCAG()
).union(
    new CSG.Path2D([[224.4622054,-170.0416294],[236.413356,-176.9416294]]).appendPoint([243.313356,-164.9904788]).appendPoint([231.3622054,-158.0904788]).appendPoint([224.4622054,-170.0416294]).close().innerToCAG()
).union(
    new CSG.Path2D([[161.4544949,-108.9],[174.9,-108.9]]).appendPoint([174.9,-95.1]).appendPoint([161.1,-95.1]).appendPoint([161.1,-107.5135294]).appendArc([161.4544949,-108.9],{"radius":1.5,"clockwise":false,"large":true}).close().innerToCAG()
)).extrude({ offset: [0, 0, 1.6] });
}




                function switch_plate_case_fn() {
                    

                // creating part 0 of case switch_plate
                let switch_plate__part_0 = switch_plate_ol_extrude_1_6_outline_fn();

                // make sure that rotations are relative
                let switch_plate__part_0_bounds = switch_plate__part_0.getBounds();
                let switch_plate__part_0_x = switch_plate__part_0_bounds[0].x + (switch_plate__part_0_bounds[1].x - switch_plate__part_0_bounds[0].x) / 2
                let switch_plate__part_0_y = switch_plate__part_0_bounds[0].y + (switch_plate__part_0_bounds[1].y - switch_plate__part_0_bounds[0].y) / 2
                switch_plate__part_0 = translate([-switch_plate__part_0_x, -switch_plate__part_0_y, 0], switch_plate__part_0);
                switch_plate__part_0 = rotate([0,0,0], switch_plate__part_0);
                switch_plate__part_0 = translate([switch_plate__part_0_x, switch_plate__part_0_y, 0], switch_plate__part_0);

                switch_plate__part_0 = translate([0,0,0], switch_plate__part_0);
                let result = switch_plate__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return switch_plate_case_fn();
            }

        