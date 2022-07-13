import argparse
import sys

class fix_action_data(argparse.Action):
   def __call__(self, parser, namespace, values, option_string=None):
      fixed_list = []
      fixed_list.append(values[0])
      fixed_list.append(values[1])
      fixed_list.append(values[2].strip())
      fixed_list.append(values[3])
      setattr(namespace, self.dest, fixed_list)

def fix_args(args):
   arg_list = list()
   arg_so_far = ""
   state = False
   for arg in args:
      if not state:
         if arg.startswith('['):
            state = True
            arg_so_far = arg[1:]
            continue
         else:
            arg_list.append(arg)
            continue
      if state:
         if arg.endswith(']'):
            arg_so_far = arg_so_far + arg[:-1]
            state = False
            arg_list.append(arg_so_far)
            arg_so_far = ""
            continue
         else:
            arg_so_far = arg_so_far + arg

   return arg_list

def parse_optional(cmd):
   if cmd is not None:
      return cmd[1:] # remove leading --
   else:
      return cmd # empty list
class arg_parser:
   def __init__(self):
      self._parser = argparse.ArgumentParser(description='DUNE: Docker Utilities for Node Execution')
      self._parser.add_argument('--start', nargs='+', metavar=["NODE", "CONFIG-DIR (Optional)"], help='start a new node with a given name and an optional config.ini')
      self._parser.add_argument('--stop', metavar="NODE", help='stop a node with a given name')
      self._parser.add_argument('--remove', metavar="NODE", help='a node with a given name, will stop the node if running')
      self._parser.add_argument('--list', action='store_true', help='list all nodes available and their statuses')
      self._parser.add_argument('--simple-list', action='store_true', help='list all nodes available and their statuses without formatting and unicode')
      self._parser.add_argument('--set-active', metavar=("NODE"), help='set a node to active status')
      self._parser.add_argument('--get-active', action='store_true', help='get the name of the node that is currently active')
      self._parser.add_argument('--export-node', metavar=("NODE", "DIR"), nargs=2, help='export state and blocks log for the given node.')
      self._parser.add_argument('--import-node', metavar=("DIR", "NODE"), nargs=2, help='import state and blocks log to a given node')
      self._parser.add_argument('--monitor', action='store_true', help='monitor the currently active node')
      self._parser.add_argument('--import-dev-key', metavar="KEY", help='import a private key into developement wallet')
      self._parser.add_argument('--create-key', action='store_true', help='create an public key private key pair')
      self._parser.add_argument('--export-wallet', action='store_true', help='export the internal development wallet')
      self._parser.add_argument('--import-wallet', metavar=["DIR"], help='import a development wallet')
      self._parser.add_argument('--create-account', nargs='+', metavar=["NAME","CREATOR (Optional)", "PUB_KEY (Optional)", "PRIV_KEY (Optional)"], help='create an EOSIO account and an optional creator (the default is eosio)')
      self._parser.add_argument('--create-cmake-app', nargs=2, metavar=["PROJ_NAME", "DIR"], help='create a smart contract project at from a specific host location')
      self._parser.add_argument('--create-bare-app', nargs=2, metavar=["PROJ_NAME", "DIR"], help='create a smart contract project at from a specific host location')
      self._parser.add_argument('--cmake-build', nargs=1, metavar=["DIR", "-- FLAGS (Optional)"], help='build a smart contract project at the directory given optional flags are of the form -- -DFLAG1=On -DFLAG2=Off]')
      self._parser.add_argument('--ctest', nargs=1, metavar=["DIR", "-- FLAGS (Optional)"], help='run the ctest tests for a smart contract project at the directory given optional flags are of the form -- -VV')
      self._parser.add_argument('--gdb', nargs=1, metavar=["DIR", "-- FLAGS (Optional)"], help='run the ctest tests for a smart contract project at the directory given optional flags are of the form -- -VV')
      self._parser.add_argument('--deploy', nargs=2, metavar=["DIR", "ACCOUNT"], help='deploy a smart contract and ABI to account given')
      self._parser.add_argument('--destroy-container', action='store_true', help='destroy context container <Warning, this will destroy your state and block log>')
      self._parser.add_argument('--stop-container', action='store_true', help='stop the context container')
      self._parser.add_argument('--start-container', action='store_true', help='start the context container')
      self._parser.add_argument('--set-system-contract', metavar=["ACCOUNT"], help='set the system contract to an account given (default normally is `eosio`)')
      self._parser.add_argument('--set-bios-contract', metavar=["ACCOUNT"], help='set the bios contract to an account given (default normally is `eosio`)')
      self._parser.add_argument('--set-token-contract', metavar=["ACCOUNT"], help='set the system contract to an account given (default normally is`eosio.token`)')
      self._parser.add_argument('--bootstrap-system', action='store_true', help='install boot contract to eosio and activate all protocol features')
      self._parser.add_argument('--bootstrap-system-full', action='store_true', help='same as `--bootstrap-system` but also creating accounts needed for system contract and set codes for token, msig and system')
      self._parser.add_argument('--send-action', nargs=4, action=fix_action_data, metavar=["ACCOUNT", "ACTION", "DATA", "PERMISSION"], help='send action to account with data given and permission')
      self._parser.add_argument('--get-table', nargs=3, metavar=["ACCOUNT", "SCOPE", "TABLE"], help='get the data from the given table')
      self._parser.add_argument('--activate-feature', metavar=["CODENAME"], help='active protocol feature')
      self._parser.add_argument('--list-features', action='store_true', help='list available protocol feature code names')
      self._parser.add_argument('remainder', nargs=argparse.REMAINDER) # used to store arguments to individual programs, starting with --
      #TODO readdress after the launch
      #self._parser.add_argument('--start-webapp', metavar=["DIR"], help='start a webapp with ')
   
   def is_forwarding(self):
      return len(sys.argv) > 1 and sys.argv[1] == '--'
   
   def get_forwarded_args(self):
      return sys.argv[2:]

   def parse(self):
      return self._parser.parse_args()
