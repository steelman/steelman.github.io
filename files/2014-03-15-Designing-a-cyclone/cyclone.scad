/* -*- mode: scad; c-basic-offset: 4; c-file-style: "k&r"; indent-tabs-mode: nil -*- */
/* All measurements are in milimeters */

top_diameter=200;
bottom_diameter=100;
height=300;
inlet_diameter = 40;

/* internal variables */
$fn=50;
inlet_radius  =  inlet_diameter / 2;
top_radius    =    top_diameter / 2;
bottom_radius = bottom_diameter / 2;
tga           = (top_radius - bottom_radius) / height;
total_height  = top_radius / tga;
bottom_height = total_height - height;

/* inlet position */
inlet_vertical_position = total_height-inlet_diameter * 1.5 ;
inlet_horizontal_position = inlet_vertical_position * tga - inlet_radius*1.1;
inlet_position = [0,inlet_horizontal_position,inlet_vertical_position];
inlet_angle = 80;

difference() {
    /* the cyclone */
    translate([0,0,bottom_height])
        cylinder(r1=bottom_radius, r2=top_radius, h=height);
    /* remove the inside */
    translate([0,0,4])
        cylinder(r1=0, r2=top_radius, h=total_height);
    /* cut in half at y = 0 and x > 0 */
    rotate([0,0,0])
	translate([-top_radius - 10,-0.5,-10])
        cube([top_radius + 10,1,total_height+20]);
    /* the inlet */
    translate(inlet_position)
	rotate([0,inlet_angle,0])
        cylinder(r=inlet_radius, h=top_diameter);
}

