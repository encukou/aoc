// To use this, convert input data to a "input.heights" file with heights as
// numbers (a=0, ...). Separate numbers on each line by spaces.

module mountain () {
    surface(file = "input.heights", center = true, convexity = 5);
}
scale ([1, 1, 0.5]) {
    color ([0.5, 0.75, 0.9]) render(convexity=5) intersection () {
        mountain ();
        translate ([-100, -100, -0.5]) cube ([200, 200, 1]);
    }
    color ([0.1, 0.95, 0.3]) render(convexity=5) intersection () {
        mountain ();
        translate ([-100, -100, 0.5]) cube ([200, 200, 2]);
    }
    color ([0.85, 0.67, 0.2]) render(convexity=5) intersection () {
        mountain ();
        translate ([-100, -100, 2.5]) cube ([200, 200, 20]);
    }
    color ([0.9, 0.95, 1]) render(convexity=5) intersection () {
        mountain ();
        translate ([-100, -100, 22.5]) cube ([200, 200, 10]);
    }
}
