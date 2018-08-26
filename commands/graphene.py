"""
/******************************************************************************
  This source file is part of the Avogadro project.

  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import argparse
import json
import sys
import os
from random import randrange
from sknano.generators import GrapheneGenerator

# Some globals:
debug = True


def getOptions():
    userOptions = {}

    userOptions['Layers'] = {}
    userOptions['Layers']['type'] = 'integer'
    userOptions['Layers']['default'] = 1

    userOptions['ACLength'] = {}
    userOptions['ACLength']['label'] = 'Armchair Length'
    userOptions['ACLength']['type'] = 'float'
    userOptions['ACLength']['default'] = 1.0
    userOptions['ACLength']['precision'] = 3
    userOptions['ACLength']['suffix'] = ' nm'
    userOptions['ACLength']['toolTip'] = 'Length of the armchair side'

    userOptions['ZZLength'] = {}
    userOptions['ZZLength']['label'] = 'Zig-zag Length'
    userOptions['ZZLength']['type'] = 'float'
    userOptions['ZZLength']['default'] = 1.0
    userOptions['ZZLength']['precision'] = 3
    userOptions['ZZLength']['suffix'] = ' nm'
    userOptions['ZZLength']['toolTip'] = 'Length of the zig-zag side'

    opts = {'userOptions': userOptions}

    return opts


def generate(opts):
    ac = float(opts['ACLength'])
    zz = float(opts['ZZLength'])
    n = int(opts['Layers'])

    graphene = GrapheneGenerator(armchair_edge_length=20, zigzag_edge_length=1, nlayers=n)
    # need a better random temporary name
    name = 'temp{}.xyz'.format(randrange(32768))
    graphene.save(fname=name)

    with open(name) as f:
        xyzData = f.read()
    os.remove(name)

    return xyzData


def runWorkflow():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Append tube in xyz format (Avogadro will bond everything)
    result = {}
    result['append'] = True
    result['moleculeFormat'] = 'xyz'
    result['xyz'] = generate(opts)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Graphene')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-workflow', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Graphene...")
    if args['menu_path']:
        print("&Build|Insert")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_workflow']:
        print(json.dumps(runWorkflow()))
