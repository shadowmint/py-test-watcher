import os
import subprocess
from .exception import exception


def run(program, *kargs, **kwargs):
  """ Run a program on the path, with arguments.

      Use it like this:

      run("ls", "/home/")

      Or, if you just want to check IF the command can run, 
      without actually running it, pass 'check_only' like this:

      run("ls", check_only=True)

      To capture the output of the command (including errors)
      use:

      success, output = run("ls", "/bin")
  """
  check_only = kwarg("check_only", False, kwargs)
  capture_output = kwarg("capture_output", False, kwargs)
  rtn = True
  resolved = which(program)
  if check_only:
    return resolved is not None
  else:
    if resolved is not None:
      prog = [resolved]
      prog.extend(kargs)
      if capture_output:
        try:
          rtn = True, subprocess.check_output(prog, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
          e = exception()
          rtn = False, e.output
      else:
        try:
          subprocess.call(prog)
        except subprocess.CalledProcessError:
          rtn = False
    else:
      raise BadCommandException("Missing command: '%s'" % program)
  return rtn
    
def is_exe(fpath):
  """ Check file exists and is executable.
      TODO: Better way to do this maybe?
  """
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def which(program):
  """ Resolve a program from the PATH if possible """
  fpath, fname = os.path.split(program)
  if fpath:
    if is_exe(program):
      return program
  else:
    for path in os.environ["PATH"].split(os.pathsep):
      path = path.strip('"')
      exe_file = os.path.join(path, program)
      if is_exe(exe_file):
        return exe_file
      elif is_exe(exe_file + ".exe"):
        return exe_file + ".exe"
  return None


class BadCommandException(Exception):
  pass


def kwarg(key, default, kwargs):
  rtn = default
  if key in kwargs.keys():
    rtn = kwargs[key]
  return rtn
