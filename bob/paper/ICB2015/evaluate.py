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
#s
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bob
import facereclib
import argparse
import os
import antispoofing.evaluation
import bob.palmvein
import subprocess

def command_line_arguments(command_line_parameters = None):
  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                                                      
  parser.add_argument('-d', '--dev-file', default = ('results/vera/NOM50_palmvein-preprocessor_none_lbp/scores/NOM50/nonorm/scores-dev'),
      help = 'The file of the scores file (4-column) containing the scores for the verification system, Normal Operation Mode (NOM) scenario.')
                                                           
  parser.add_argument('-s', '--spoofing-file', default = ('results/vera/SpoofingAttack50_palmvein-preprocessor_none_lbp/scores/SpoofingAttack50/nonorm/scores-dev'),
      help = 'The file of the scores file (4-column) containing the scores for the verification system, Spoofing Attack scenario.')

  parser.add_argument('-o', '--output-file', default = ('results/vera/SpoofingAttack50_palmvein-preprocessor_none_lbp.pdf'),
      help = 'The output file for SFAR curves.')

  parser.add_argument('-i', '--demandedplot', default = ('7'),
      help = 'The options of plotting the score distribution for licit and spoof scenario and threshold line and probability of success line. The output file for SFAR curves.')
 
  parser.add_argument('parameters', nargs = argparse.REMAINDER,
      help = "Parameters directly passed to the plot_on_demand.py script. Use -- to separate this parameters from the parameters of this script. See 'bin/plot_on_demand.py --help' for a complete list of options.")

  # add verbosity command line option
  facereclib.utils.add_logger_command_line_option(parser)
  # parse command line
  args = parser.parse_args(command_line_parameters)
  # set verbosity level
  facereclib.utils.set_verbosity_level(args.verbose)
 
  # return command line options
  return args


def main(command_line_parameters = None):
  
  args = command_line_arguments(command_line_parameters)
  
  # check that the result directories already exist
  if not os.path.exists(args.dev_file):
    raise IOError("The result directory '%s' does not exist. Check your parameters!" % args.dev_file)
  if not os.path.exists(args.spoofing_file):
    raise IOError("The result directory '%s' does not exist. Check your parameters!" % args.spoofing_file)

  parameters = [  '--dev-file', args.dev_file,
                  '--spoofing-file', args.spoofing_file]
  
  #Generation of the dev-scores_spoof
  bob.palmvein.script.scores2spoofingfile.main(parameters)
      
  spoofingScoresFile = args.spoofing_file+'_spoof'
  
  parameters = ['./bin/plot_on_demand.py',
                  args.dev_file,
                  args.dev_file,
                  spoofingScoresFile,
                  spoofingScoresFile,
                  '--demandedplot', args.demandedplot,
                  '--output', args.output_file]
  
    
  #Generation of the dev-scores_spoof
  subprocess.call(parameters)
  
  
       
