import math
import sys


class Point:
    x = 0
    y = 0

    def __init__(self, inx, iny):
        self.x = inx
        self.y = iny


# <summary>List of points used as reference</summary>
# <remarks>
# Only 3 points will be used, for simplicity.
# These 3 points will define the plan z=0
# The first one is the origin (0, 0)
# The second one will be in the x-axis (d, 0)
# </remarks>
distab = 0
reference = 0
minimum = 0
maximum = 0

# <summary>
# Distances used in the formula. They are the coordinates for points b and c (see above)
# </summary>
d = 0
i = 0
j = 0

# <summary>Distance between A and B</summary>
distAB = 0

# <summary>Distance between A and C</summary>
distAC = 0

# <summary>Distance between B and C</summary>
distBC = 0


# <summary>
# Initialize the reference points
# </summary>
# <param name="b">Second reference points</param>
# <param name="c">Third reference point</param>
# <remarks>
# By definition, the first point's coordinates will be (0, 0) and the second point's y
# coordinate will be 0.
# </remarks>


def set_references(b, c):
    global distAB, distAC, distBC, reference, d, i, j

    if b.x != 0:
        print "Second reference point's x coordinate must be zero"
        # throw new ArgumentOutOfRangeException("b", b.x, "Second reference point's x coordinate must be zero")

    reference = (Point(0, 0), Point(b.y, 0), Point(c.x, c.y))
    d = b.y
    i = c.x
    j = c.y

    distAB = d
    distAC = math.sqrt(square(i) + square(j))
    # print "i:%s" % i
    # print "d:%s" % d
    # print "j:%s" % j
    # print "%s" % (square(i) + d - square(j))
    distBC = math.sqrt(math.fabs(square(i) + d - square(j)))


# <summary>
# Calculates the maximum and minimum adjustments (values by which a and b can be
# multiplied) so that a circle with radius a will touch a circle with radius b, if they
# are d apart.
# </summary>
# <param name="a">Radius of first circle</param>
# <param name="b">Radius of second circle</param>
# <param name="d">Distance between them. Must not be zero</param>
# <param name="minimum">minimum adjustment</param>
# <param name="maximum">maximuma adjustment</param>
# <remarks>
# The minimum value will make the circles just touch, one being outside the other
# The maximum value will make them just touch, one being inside the other
# </remarks>
def calculate_one_adjust(a, b, d):
    global maximum, minimum

    if d == 0:
        # throw new ArgumentOutOfRangeException("d", "Distance cannot be zero")
        print "Distance cannot be zero"

    # Special case where both signals are the same strength: there isn't a superior limit
    # for the adjustment.
    if a == b:
        maximum = 9999999999

    else:
        maximum = d / math.fabs(a - b)

    minimum = d / (a + b)

    return minimum, maximum


# <summary>
# Calculates the adjust to transform the strenght of the three signals into a value
# suitable for calculation
# </summary>
# <param name="strengtha">Strength of signal A</param>
# <param name="strengthb">Strength of signal B</param>
# <param name="strengthc">Strength of signal C</param>
# <returns>
# A value that, multiplied by each of the signals strengths, will result in a good
# calculation 0 if there is no such value.
# </returns>
def calculate_adjust(strengtha, strengthb, strengthc):
    global minimum, minab
    global maximum

    # We need at least 2 signals
    if (strengtha == 0 and strengthb == 0) or (strengtha == 0 and strengthc == 0) or (
            strengthb == 0 and strengthc == 0):
        return 0

    minab, maxab = calculate_one_adjust(strengtha, strengthb, distAB)
    minac, maxac = calculate_one_adjust(strengtha, strengthc, distAC)
    minbc, maxbc = calculate_one_adjust(strengthb, strengthc, distBC)

    # If one of the strengths is zero, ignore it.
    if strengtha == 0:
        minimum = minbc
        maximum = maxbc

    elif strengthb == 0:
        minimum = minac
        maximum = maxac

    elif strengthc == 0:
        minimum = minab
        maximum = maxab

    else:
        minimum = max(max(minab, minac), minbc)
        maximum = min(min(maxab, maxac), maxbc)

    if minimum > maximum:
        # Cannot find a suitable adjust
        return 0

    elif minimum == maximum:
        # No contest. They are the same.
        # We could fall back to the else block and have the same result
        return minimum

    elif maximum == 9999999999:
        # No maximum limit, return the minimum. This may increase the accuracy.
        return minimum

    else:
        # We can safely assume there won't be an overflow here. The signals would have to
        # be fabsurdly strong for that...
        return math.sqrt(minimum * maximum)


# <summary>
# The entire point of this class: Calculate the point which distance to the reference
# points is proportional to the respective strengths.
# </summary>
# <param name="strengtha">Strength of signal A</param>
# <param name="strengthb">Strength of signal B</param>
# <param name="strengthc">Strength of signal C</param>
# <returns>
# A point which distance to the reference points is proportional to the respective signalstrengths


def trilaterate(strengtha, strengthb, strengthc):
    strengtha = -strengtha/100
    strengthb = -strengthb/100
    strengthc = -strengthc/100

    adjust = calculate_adjust(strengtha, strengthb, strengthc)
    #print "adjust:%s" % adjust
    # Could not find a suitable adjust: return null as an indication of failure
    if adjust == 0:
        return None

    # Adjust the strengths to an optimal value
    r1 = strengtha * adjust
    r2 = strengthb * adjust
    r3 = strengthc * adjust

    # Calculate the point using the formula in the reference
    # print "r1: %s" % r1
    # print "r2: %s" % r2
    # print "r3: %s" % r3
    # print "square r1: %s" % square(r1)
    # print "square r2: %s" % square(r2)
    # print "square r3: %s" % square(r3)
    # print "d: %s" % d
    # print "i: %s" % i
    # print "j: %s" % j

    x = (square(r1) - square(r2) + square(r3)) / (2 * d)
    y = (square(r1) - square(r3) + square(i) + square(j)) / ((2*j) - ((i/j) * x))

    return x, y


def square(n):
    return n * n


def main(argv):
    set_references(Point(0, float(argv[0])), Point(float(argv[1]), float(argv[2])))
    return "%s,%s\n" % trilaterate(float(argv[3]), float(argv[4]), float(argv[5]))


if __name__ == "__main__":
    main(sys.argv[1:])
