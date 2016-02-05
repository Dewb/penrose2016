def computeRegion(cube, channel, ledindex):
    regionmap = {
        (0,0): [ (30, "AB2"), (60, "B2"), (90, "B1"), (999, "B1") ],
        (0,1): [ (29, "BC1"), (63, "C1"), (90, "A2"), (999, "A2") ],
        (0,2): "AB2",
        (0,3): "AC1",
        (0,4): [ (23, "off"), (83, "A1"), (999, "AB1") ],
        (0,5): [ (25, "BC2"), (80, "B2"), (999, "off") ],
        (0,6): "C1",
        (0,7): "A2",
        (1,0): [ (28, "BC2"), (56, "C2"), (90, "A1"), (999, "A1") ],
        (1,1): [ (29, "AB1"), (63, "B1"), (90, "B2"), (999, "B2") ],
        (1,2): "BC2",
        (1,3): "BC1",
        (1,4): [ (24, "off"), (84, "C1"), (999, "AC1") ],
        (1,5): [ (25, "AC2"), (85, "C2"), (999, "off") ],
        (1,6): "B2",
        (1,7): "B1",
        (2,0): [ (28, "AC2"), (56, "A2"), (90, "C1"), (999, "C1") ],
        (2,1): [ (30, "AC1"), (58, "A1"), (90, "C2"), (999, "C2") ],
        (2,2): "AC2",
        (2,3): "AB1",
        (2,4): [ (24, "off"), (84, "A2"), (999, "AB2") ],
        (2,5): [ (25, "BC1"), (85, "B1"), (999, "off") ],
        (2,6): "C2",
        (2,7): "A1",

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
    "A1": 1,
    "B1": 2,
    "C1": 3,
    "AB1": 4,
    "BC1": 5,
    "AC1": 6,
    "A2": 7,
    "B2": 8,
    "C2": 9,
    "AB2": 10,
    "BC2": 11,
    "AC2": 12,
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
