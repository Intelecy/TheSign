$fa = 1;
$fs = 0.4;

target_qr_width = 175;
dim = 25;
margin = 0.5;
font = "FiraCode Nerd Font:style=SemiBold";
font_sz = 8.5;

pixel_sz = target_qr_width / dim;

qr_data = [
    [1,1,1,1,1,1,1,0,1,1,0,0,1,1,0,0,1,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,1,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,1,0,0,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,0,0,0,0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,1,0,0,1,1,1,0,1,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [1,1,1,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,0,1,1,1,0,1],
    [0,0,1,1,0,1,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1],
    [0,0,0,0,1,1,1,1,1,0,0,1,0,1,1,0,0,1,0,0,1,0,1,0,0],
    [1,0,1,0,0,1,0,0,0,0,0,0,1,1,1,1,0,1,0,1,0,1,1,1,0],
    [0,1,0,1,1,0,1,1,0,1,0,0,0,1,1,0,0,0,1,1,0,1,0,0,0],
    [0,1,1,1,0,1,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0],
    [0,1,1,1,0,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,1,1,1,1,0],
    [1,0,0,0,0,0,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,0,1,0],
    [0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0],
    [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,0,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,1,0,1,1,0,1,1,1,0,0,0,1,1,0,0,0],
    [1,0,1,1,1,0,1,0,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,1,0,1,0,1,1,0,1,0,0,0,1,1,1,1,1,0,0,0,1,1],
    [1,0,1,1,1,0,1,0,1,0,0,1,1,1,0,0,1,0,0,1,1,0,0,1,0],
    [1,0,0,0,0,0,1,0,1,0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,0],
    [1,1,1,1,1,1,1,0,1,1,0,0,0,1,1,1,0,1,0,0,1,0,1,1,1],
];

translate([0, 25]) {
    union() {
        qr_render(qr_data);
        logo();
    };
}
bottom_text();

module bottom_text() {
    translate([0, 0]) {
        text("Network:  Intelecy Guest", size=font_sz, font=font, halign="left");
        
        translate([0, -(font_sz + font_sz * 0.33)])
            text("Password: GoingGreen", size=font_sz, font=font, halign="left");
    };
}

module logo() {
    margin_bottom = 15;
    width = target_qr_width * 1;
    
    translate([-1 * (width - target_qr_width) / 2, target_qr_width + margin_bottom, 0])
        resize([width, 0], auto=true)
            import("../svg/intelecy-logo-2.svg");
}

module position_sq() {
    union() {
        difference() {
            square(size = pixel_sz * 7, center = false);
            translate([pixel_sz, pixel_sz]) square(size = pixel_sz * 5, center = false);
        }
        translate([pixel_sz * 2, pixel_sz * 2]) square(size = pixel_sz * 3, center = false);
    }
}

module qr_render(data, module_size = pixel_sz) {
    union() {
        for(r = [0 : dim - 1]) {
            for(c = [0 : dim - 1]) {
                if(data[r][c] == 1) {
                    xo = c * module_size;
                    yo = (dim - 1 - r) * module_size;
                    
                    translate([xo + module_size / 2, yo + module_size / 2, 0]) {
                        // square([module_size, module_size]);
                        circle(d = module_size - margin);
                    }
                }
            }
        }
        
        position_sq();
        translate([0, pixel_sz * (dim - 7)]) position_sq();
        translate([pixel_sz * (dim - 7), pixel_sz * (dim - 7)]) position_sq();
    }
}
