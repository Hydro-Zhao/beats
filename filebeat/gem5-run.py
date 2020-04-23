#! /usr/bin/env python2.7

import optparse
import os
import sys
import copy

#from gem5tools.config2pngbase64 import
#may use the gem5tools as module later
#just use os.system now

# TODO an option to specific the name of the simulation output, pass it as an option of ./filebeat

def main():
    # Parse options
    usage = ('./gem5-run.py [OPTION]')
    parser = optparse.OptionParser(usage=usage)
    parser.add_option(
        '--setup',
        action='store_true', default=False,
        help="setup space and index pattern(default: '%default')")
    parser.add_option(
        '--deploy',
        action='store_true', default=False,
        help="(default: '%default')")
    parser.add_option(
        '--export_dashboards',
        action='store_true', default=False,
        help="export dashboards, if modified dashboard and want to make it persistens(default: '%default')")

    (options, args) = parser.parse_args()

    #if len(args) != 1:
    #    parser.error('incorrect number of arguments')
    #    sys.exit(1)

    if options.setup:
        print "just ignore the Error messages"
        os.system("gem5tools/make_fileset.sh")
        os.system("gem5tools/setup.sh")
    elif options.deploy:
        #os.system("gem5tools/config2pngbase64.py")
        os.system("gem5tools/parse_exec.py")
        os.system("gem5tools/deploy.sh")
    elif options.export_dashboards:
        os.system("gem5tools/export_dashboards.sh")

if __name__ == '__main__':
    sys.path.append(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', 'src', 'python'))
    main()
