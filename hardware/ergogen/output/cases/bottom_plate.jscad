function bottom_plate_ol_extrude_2_outline_fn(){
    return new CSG.Path2D([[140.5,-160],[182.5,-160]]).appendArc([184.5,-162],{"radius":2,"clockwise":true,"large":false}).appendPoint([184.5,-165.955]).appendArc([185.5,-166.955],{"radius":1,"clockwise":false,"large":false}).appendPoint([203.8042028,-166.955]).appendArc([204.0630218,-166.9890742],{"radius":1,"clockwise":true,"large":false}).appendPoint([220.5658791,-171.4110015]).appendArc([220.8070601,-171.5109019],{"radius":1,"clockwise":true,"large":false}).appendPoint([237.115022,-180.9263081]).appendArc([238.4810474,-180.5602827],{"radius":1,"clockwise":false,"large":false}).appendPoint([247.9595719,-164.1429967]).appendArc([248.0040989,-164.0695613],{"radius":2,"clockwise":true,"large":false}).appendPoint([254.1875238,-154.3487369]).appendArc([254.5,-153.2753015],{"radius":2,"clockwise":false,"large":false}).appendPoint([254.5,-105.8575]).appendArc([252.5,-103.8575],{"radius":2,"clockwise":false,"large":false}).appendPoint([234.5,-103.8575]).appendArc([232.5,-101.8575],{"radius":2,"clockwise":true,"large":false}).appendPoint([232.5,-95.8575]).appendArc([231.5,-94.8575],{"radius":1,"clockwise":false,"large":false}).appendPoint([215.5,-94.8575]).appendArc([214.5,-93.8575],{"radius":1,"clockwise":true,"large":false}).appendPoint([214.5,-93]).appendArc([213.5,-92],{"radius":1,"clockwise":false,"large":false}).appendPoint([197.5,-92]).appendArc([196.5,-91],{"radius":1,"clockwise":true,"large":false}).appendPoint([196.5,-88.2375]).appendArc([195.5,-87.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([176.5,-87.2375]).appendArc([175.5,-88.2375],{"radius":1,"clockwise":false,"large":false}).appendPoint([175.5,-91]).appendArc([174.5,-92],{"radius":1,"clockwise":true,"large":false}).appendPoint([158.5,-92]).appendArc([157.5,-93],{"radius":1,"clockwise":false,"large":false}).appendPoint([157.5,-105]).appendArc([156.5,-106],{"radius":1,"clockwise":true,"large":false}).appendPoint([140.5,-106]).appendArc([139.5,-107],{"radius":1,"clockwise":false,"large":false}).appendPoint([139.5,-159]).appendArc([140.5,-160],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    CAG.circle({"center":[234.9371581,-154.6627043],"radius":1.5})
.union(
    CAG.circle({"center":[172.5,-152],"radius":1.5})
).union(
    new CSG.Path2D([[226.0855394,-162.0299325],[242.540022,-171.5299325]]).appendPoint([246.540022,-164.6017293]).appendPoint([230.0855394,-155.1017293]).appendPoint([226.0855394,-162.0299325]).close().innerToCAG()
).union(
    new CSG.Path2D([[206.1991196,-156.3286933],[224.5517103,-161.2462551]]).appendPoint([226.6222626,-153.5188485]).appendPoint([208.2696719,-148.6012867]).appendPoint([206.1991196,-156.3286933]).close().innerToCAG()
).union(
    new CSG.Path2D([[185.5,-156.105],[204.5,-156.105]]).appendPoint([204.5,-148.105]).appendPoint([185.5,-148.105]).appendPoint([185.5,-156.105]).close().innerToCAG()
).union(
    new CSG.Path2D([[140.5,-149.15],[159.5,-149.15]]).appendPoint([159.5,-141.15]).appendPoint([140.5,-141.15]).appendPoint([140.5,-149.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[158.5,-101.15],[177.5,-101.15]]).appendPoint([177.5,-96.3875]).appendPoint([194.5,-96.3875]).appendPoint([194.5,-101.15]).appendPoint([212.5,-101.15]).appendPoint([212.5,-104.0075]).appendPoint([231.5,-104.0075]).appendPoint([231.5,-96.0075]).appendPoint([213.5,-96.0075]).appendPoint([213.5,-93.15]).appendPoint([195.5,-93.15]).appendPoint([195.5,-88.3875]).appendPoint([176.5,-88.3875]).appendPoint([176.5,-93.15]).appendPoint([158.5,-93.15]).appendPoint([158.5,-101.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[140.5,-132.15],[158.5,-132.15]]).appendPoint([158.5,-135.15]).appendPoint([177.5,-135.15]).appendPoint([177.5,-130.3875]).appendPoint([194.5,-130.3875]).appendPoint([194.5,-135.15]).appendPoint([212.5,-135.15]).appendPoint([212.5,-138.0075]).appendPoint([231.5,-138.0075]).appendPoint([231.5,-130.0075]).appendPoint([213.5,-130.0075]).appendPoint([213.5,-127.15]).appendPoint([195.5,-127.15]).appendPoint([195.5,-122.3875]).appendPoint([176.5,-122.3875]).appendPoint([176.5,-127.15]).appendPoint([159.5,-127.15]).appendPoint([159.5,-124.15]).appendPoint([140.5,-124.15]).appendPoint([140.5,-132.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[140.5,-115.15],[158.5,-115.15]]).appendPoint([158.5,-118.15]).appendPoint([177.5,-118.15]).appendPoint([177.5,-113.3875]).appendPoint([194.5,-113.3875]).appendPoint([194.5,-118.15]).appendPoint([212.5,-118.15]).appendPoint([212.5,-121.0075]).appendPoint([231.5,-121.0075]).appendPoint([231.5,-113.0075]).appendPoint([213.5,-113.0075]).appendPoint([213.5,-110.15]).appendPoint([195.5,-110.15]).appendPoint([195.5,-105.3875]).appendPoint([176.5,-105.3875]).appendPoint([176.5,-110.15]).appendPoint([159.5,-110.15]).appendPoint([159.5,-109.9475469]).appendArc([159.4200095,-107.15],{"radius":1.5,"clockwise":false,"large":true}).appendPoint([140.5,-107.15]).appendPoint([140.5,-115.15]).close().innerToCAG()
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

        