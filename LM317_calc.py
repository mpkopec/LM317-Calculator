from __future__ import division

__author__ = 'Maciej Kopec'

import getopt
import sys
from math import fabs


# ------------- FUNCTIONS ------------
# Help printing function
def usage():
    print "Here be usage"

# Returns voltage depending on given resistance in ohms
def output(R1, R2):
    return 1.25*(1 + R2/R1) + 100e-6*R2

# Searches for the resistance combination that is closes to the wanted value
# in series of resistors. Series is multiplied by 0.1, 1, 10, 100, 1000 to cover
# more possible resistances.
def findResistance(wanted, series):
    delta = 10000
    R1f = 0
    R2f = 0
    for mul in range(-1, 4):
        for R1 in series:
            R1 *= 10**mul
            for R2 in series:
                R2 *= 10**mul
                res = fabs(output(R1, R2) - wanted)
                if res < delta:
                    delta = res
                    R1f = R1
                    R2f = R2
    return R1f, R2f

# Imports series form file. CSV like, but separated by whitespaces (the whitespace
# count between values can be as big as desired).
def seriesFromFile(seriesCode):
    filename = seriesCode + ".txt"
    fileHandle = open(filename)
    contents = fileHandle.read()
    fileHandle.close()

    splitted = contents.split()
    for i in range(len(splitted)):
        splitted[i] = float(splitted[i])
    return splitted

# --------------- MAIN ---------------

# ------------ VARIABLES -------------
series = "e24"
seriesValues = seriesFromFile(series)
# in percent
precision = 5
voltage = 5
tables = False
countR = False
Rf, RfMinV, RfMaxV = ([0, 0], [0, 0], [0, 0])

# --------- OPTIONS HANDLING ---------
try:
    opts, args = getopt.getopt(sys.argv[1:], "s:p:v:t", ["series=", "precision=", "voltage=", "R1=", "R2="])
except getopt.GetoptError as err:
    # print help information and exit:
    print str(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ("-s", "--series"):
        series = a
        seriesValues = seriesFromFile(series)
    elif o in ("-p", "--precision"):
        precision = float(a)
    elif o in ("-v", "--voltage"):
        voltage = float(a)
    elif o == '-t':
        tables = True
    elif o == "--R1":
        countR = True
        Rf[0] = float(a)
    elif o == "--R2":
        countR = True
        Rf[1] = float(a)
    else:
        assert False, "unhandled option"

# ----------- FINDING NEMO -----------
# Look thorough the series only if the user did not provide resistances (at least one)
# for calculation.
if not countR:
    Rf = findResistance(voltage, seriesValues)

RfMinV = ((1 + precision/100)*Rf[0], (1 - precision/100)*Rf[1])
RfMaxV = ((1 - precision/100)*Rf[0], (1 + precision/100)*Rf[1])

# ---------- PRINTING NEMO -----------
if not tables:
    print "----------------------------------------------------------------"
    print "Found minimum resistances (R1, R2):", '({:.4e}, {:.4e})'.format(RfMinV[0], RfMinV[1])
    print "Found nominal resistances (R1, R2):", '({:.4e}, {:.4e})'.format(Rf[0], Rf[1])
    print "Found maximum resistances (R1, R2):", '({:.4e}, {:.4e})'.format(RfMaxV[0], RfMaxV[1])
    print "----------------------------------------------------------------"
    print "Minimum voltage:", '{:7.4f}'.format(output(RfMinV[0], RfMinV[1])), "V"
    print "Nominal voltage:", '{:7.4f}'.format(output(Rf[0], Rf[1])), "V"
    print "Maximum voltage:", '{:7.4f}'.format(output(RfMaxV[0], RfMaxV[1])), "V"
    print "----------------------------------------------------------------"
else:
    # Importing only if -t option given so to people without terminaltables could use the script.
    from terminaltables import AsciiTable
    resTableInfo = [
        ["Res group\\Res ID", "R1", "R2"],
        ["Minimum R", '{:.4e}'.format(RfMinV[0]), '{:.4e}'.format(RfMinV[1])],
        ["Nominal R", '{:.4e}'.format(Rf[0]), '{:.4e}'.format(Rf[1])],
        ["Maximum R", '{:.4e}'.format(RfMaxV[0]), '{:.4e}'.format(RfMaxV[1])]
    ]
    resAsciiTable = AsciiTable(resTableInfo)
    volTableInfo = [
        ["Voltage", "Value [V]"],
        ["Minimum voltage", '{:7.4f}'.format(output(RfMinV[0], RfMinV[1]))],
        ["Nominal voltage", '{:7.4f}'.format(output(Rf[0], Rf[1]))],
        ["Maximum voltage", '{:7.4f}'.format(output(RfMaxV[0], RfMaxV[1]))]
    ]
    volAsciiTable = AsciiTable(volTableInfo)
    print "----------------------------------------------------------------"
    print resAsciiTable.table
    print "----------------------------------------------------------------"
    print volAsciiTable.table
    print "----------------------------------------------------------------"