"""
/******************************************************************************
  This source file is part of the Avogadro project.

  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import argparse
import json
import sys

def getOptions():
    # no options
    return {}

def addCentroid(opts, mol):
    selected = False
    if 'selected' in mol['atoms']:
        for item in mol['atoms']['selected']:
            if item:
                selected = True
                break # we have *some* atoms selected

    coords = mol['atoms']['coords']['3d']
    centroid = [0.0, 0.0, 0.0]
    numAtoms = 0
    if not selected:
        # nothing selected, so centroid to everything
        for i in range(0, len(coords), 3):
            for j in range(3):
                centroid[j] += coords[i+j]
        numAtoms = len(coords) / 3
    else:
        # centroid only to selected atoms
        numAtoms = 0
        atom = 0
        for i in range(0, len(coords), 3):
            if mol['atoms']['selected'][atom]:
                for j in range(3):
                    centroid[j] += coords[i+j]
                numAtoms += 1
            atom += 1

    for j in range(3):
        centroid[j] = centroid[j] / numAtoms

    newMol = "1\n\n"
    newMol += "Xx {} {} {}\n".format(centroid[0], centroid[1], centroid[2])

    return newMol


def runWorkflow():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Prepare the result
    result = {}
    result['append'] = True
    result['moleculeFormat'] = 'xyz'
    result['xyz'] = addCentroid(opts, opts['cjson'])
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Add a centroid')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-workflow', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Add Centroid")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_workflow']:
        print(json.dumps(runWorkflow()))
