#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Agc command line interface for supervisor:
# 
#
# (C) 2020-07-29 AgreenCulture
# -----------------------------------------------------------
import os
import optparse
from agc_log import log, logError, logWarning, logInfo
from mip_socket import Mip_Socket
import json
from typing import Any, Union
import time
import sys
# default values definition
DEFAULT_CONFIG_FILENAME = "./agc_cli.cfg"

# stkRequester = "supervisorCLI"
field_dest = None

def on_STK_read_field_report(topic, message, mip_socket):
    logInfo("Test " + str(message["fpsGnssPositionNorth"]))
    logInfo("Test " + str(message["fpsGnssPositionEast"]))
    # if message["stkRequester"] == stkRequester:
    #     if (message["stkReadReport"] != "OK"):
    #         logError("message[\"stkReadReport\"] != \"OK\"")
    #         exit(0)
    #     logInfo("Writing field at " + field_dest)
    #     path = field_dest[:field_dest.rfind("/")]
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     f = open(field_dest, "w")
    #     f.write(message["field"])
    #     f.close()
    #     mip_socket.close()
    #     exit(0)

def main() -> None:
    """
    Parse the command line arguments and execute the script
    """
    # set usage message and application arguments definition
    usage = """usage: %prog [options] <field_dest>"""
    parser = optparse.OptionParser(usage)
    parser.add_option("-c", "--config", dest="configFilename",
                      help="config file to use (default is " +
                      DEFAULT_CONFIG_FILENAME + ")",
                      default=DEFAULT_CONFIG_FILENAME)
    (options, args) = parser.parse_args()
    # if len(args) == 0:
    #     parser.error('argument <field_dest> not given')
    # elif len(args) > 1:
    #     parser.error(
    #         'requires 1 argument (<field_dest>), more were given')
    #     sys.exit(1)
    # else:
    #     # execute script with options take from CLI args
    #     global field_dest
    #     field_dest = args[0]

    # logInfo("Field destination " + field_dest)
    mip_socket = Mip_Socket(options.configFilename)
    mip_socket.bind('FPS.gnss', on_STK_read_field_report)
    logInfo("sending FPS.gnss")
    # mip_socket.publish('FPS.gnss', {"stkRequester": stkRequester})

if __name__ == "__main__":
    main()
