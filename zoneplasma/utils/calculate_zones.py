def computeRegion(cube, channel, ledindex):
    regionmap = {
        (0,0): [ (30, "off"), (60, "off"), (90, "C"), (999, "C") ],
        (0,1): [ (30, "BC"), (60, "B"), (90, "off"), (999, "off") ],
        (0,2): "AB",
        (0,3): "off",
        (0,4): [ (86, "A"), (999, "off") ],
        (0,5): [ (86, "off"), (999, "off") ],
        (0,6): "B",
        (0,7): "off",
        (1,0): [ (30, "off"), (60, "off"), (90, "A"), (999, "A") ],
        (1,1): [ (30, "AC"), (60, "C"), (90, "off"), (999, "off") ],
        (1,2): "BC",
        (1,3): "off",
        (1,4): [ (86, "B"), (999, "off") ],
        (1,5): [ (86, "off"), (999, "off") ],
        (1,6): "C",
        (1,7): "off",
        (2,0): [ (30, "off"), (60, "off"), (90, "B"), (999, "B") ],
        (2,1): [ (30, "AB"), (60, "A"), (90, "off"), (999, "off") ],
        (2,2): "AC",
        (2,3): "off",
        (2,4): [ (86, "C"), (999, "off") ],
        (2,5): [ (86, "off"), (999, "off") ],
        (2,6): "A",
        (2,7): "off",

    }
    r = regionmap[(cube, channel)]
    if not isinstance(r, list):
        return r
    else:
        for item in r:
            if ledindex < item[0]:
                return item[1]

    print "error: unmapped region"
    return "?"

regioncode = {
    "off": 0,
    "A": 1,
    "B": 2,
    "C": 3,
    "AB": 4,
    "BC": 5,
    "AC": 6,
}
NUM_CUBES = 3
LEDS_PER_STRIP = 120
NUM_STRIPS = 8

from pprint import pprint
from operator import itemgetter
print "// Zone codes:"
sorted_codes = sorted(regioncode.items(), key=itemgetter(1))
for k, v in sorted_codes:
    print "#define ZONE_" + k + " ", v
print



for cube in range(0, NUM_CUBES):
    print "#if PENROSE_ARM ==", cube
    print "uint8_t zonemap[", LEDS_PER_STRIP * NUM_STRIPS, "] = {"
    for strip in range(0, NUM_STRIPS):
        print "// strip channel", strip
        for pixel in range(0, LEDS_PER_STRIP):
            region = computeRegion(cube, strip, pixel)
            print regioncode[region],
            if (not (pixel == 119 and strip == 7)):
                print ",",
        print
    print "};"
    print "#endif"
