$fa = 1;
$fs = 0.4;

dot_diameter = 16; // must match ../stl/Dot.stl
spacing = 61.5; // deived from ../svg/intelecy-logo.svg
shells = 3;

// calulated consts
x_spacing = sqrt(0.75) * spacing;
dots_max = shells * 2 + 1;

difference() {
    rotate(30) {
        minkowski() {
            rouding = 15;
            circle(r=x_spacing*(shells + 1)+rouding, $fn=6);
            circle(r=rouding);
        };
    }

    union() {
        for (i = [0:shells]) {
            dots = dots_max - i;
            start_y = spacing * (dots-1) / 2;
            x = i * x_spacing;

            for (d = [0:dots-1]) {
                translate([x, start_y - d*spacing, 0]) {
                    circle(d=dot_diameter);
                }
                if (i != 0) {
                    translate([-x, start_y - d*spacing, 0]) {
                        circle(d=dot_diameter);
                    }
                }
            }
        }
    };
}