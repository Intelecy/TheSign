$fa = 1;
$fs = 0.4;

dot_diameter = 16;
spacing = 61.5;
shells = 2;
x_spacing = 52;

difference() {
    rotate(30) {
        minkowski() {
            rouding = 15;
            circle(r=x_spacing*2-rouding, $fn=6);
            circle(r=rouding);
        };
    }
    
    union() {
        for (i = [0:shells-1]) {
            dots = max(1, i * 6);
            theta = 360 / dots;
            for (d = [0:dots]) {
                rotate(d * theta + theta/2) {
                    translate([spacing * i, 0, 0]) {
                        circle(d=dot_diameter);
                    };
                };
            }
        }
    };
}
