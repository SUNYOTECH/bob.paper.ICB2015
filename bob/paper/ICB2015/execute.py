#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Pedro Tome <pedro.tome@idiap.ch>
# @date: Fri 01 May 18:18:08 2014 CEST
#
# Copyright (C) 2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bob.palmvein
import argparse
import os
import pkg_resources
import facereclib


def command_line_arguments(command_line_parameters = None):
  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  
  parser.add_argument('-d', '--database', default = ('verapalm'),
      help = 'The databases to run experiments on.')

  parser.add_argument('-p', '--preprocessing', nargs='+', default = ('palmvein-preprocessor'),
      help = 'The image preprocessing to run; the preprocessors will automatically assigned to the according experiment.')

  parser.add_argument('-f', '--features', default = ('lbp-localbinarypatterns'),
      help = 'The features to run; the feature selected is the local binary patterns for these experiments.')

  parser.add_argument('-t', '--tool', default = ('match-lbp'),
      help = 'The matchers to run; the matcher selected is match-lbp for these experiments.')

  parser.add_argument('-P', '--protocols', nargs='+', default = ('nom50', 'spoofingAttack50'),
      help = 'The protocols to run; the protocols will automatically assigned to the according database.')

  parser.add_argument('-q', '--dry-run', action = 'store_true',
      help = 'Writes the actual call to the palmveinreclib instead of executing it')

  parser.add_argument('-T', '--temp-directory', default = 'temp',
      help = "The output directory for temporary files.")

  parser.add_argument('-R', '--result-directory', default = 'results',
      help = "The output directory for result files.")
      
  parser.add_argument('parameters', nargs = argparse.REMAINDER,
      help = "Parameters directly passed to the face verify script. Use -- to separate this parameters from the parameters of this script. See 'bin/fingerveinverify.py --help' for a complete list of options.")

  # add verbosity command line option
  facereclib.utils.add_logger_command_line_option(parser)
  # parse command line
  args = parser.parse_args(command_line_parameters)
  # set verbosity level
  facereclib.utils.set_verbosity_level(args.verbose)

  # return command line arguments
  return args

def main(command_line_parameters = None):

  args = command_line_arguments(command_line_parameters)
  
  # get the directory, where the configuration files are stored
  config_dir = os.path.dirname(pkg_resources.resource_filename('bob.paper.ICB2015', 'execute.py'))
 
  # iterate over all protocols ...
  for protocol in args.protocols:
    # ... that fit to the database
    #for preprocessing in args.preprocessing:
      # collect the parameters that will be sent to the bin/fingerveinverify.py script,
      # which will finally execute the experiments
      parameters = ['./bin/palmveinverify.py',
                    '--database', args.database,
                    '--protocol', protocol,
                    '--preprocessing', args.preprocessing,
                    '--features', args.features,
                    '--tool', args.tool,            
                    '--temp-directory', os.path.join(args.temp_directory, args.database),
                    '--result-directory', os.path.join(args.result_directory, args.database),
                    '--sub-directory', protocol+'_'+args.preprocessing+'_'+args.features]
  
      # set the verbosity level
      if args.verbose:
        parameters.append('-' + 'v'*args.verbose)
  
      # add the command line arguments that were specified on command line
      if args.parameters:
        parameters.extend(args.parameters[1:])
  
      if args.dry_run:
        # Write what we would have executed
        print "Would have executed:"
        print " ".join(parameters)
      else:
        # Write what we will execute
        print "Launching:"
        print " ".join(parameters)
        # execute the fingervein recognition algorithm
        facereclib.script.faceverify.main(parameters)
  
  
