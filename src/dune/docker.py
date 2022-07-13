import subprocess, platform, os, getpass

class docker:
   _container = ""
   _image     = ""
   def __init__(self, container, image):
      self._container = container
      self._image     = image

      # check if container is running
      stdout, stderr, ec = self.execute_docker_cmd(['container', 'ls'])

      # if container is not in the list then create one
      if not self._container in stdout:
      # check if container is stopped
         stdout, stderr, ec = self.execute_docker_cmd(['container', 'ls', '-a'])
         if self._container in stdout:
            self.execute_docker_cmd(['container', 'start', self._container])
         else:
            # start a new container
            print("Creating docker container ["+self._container+"]")
            host_dir = '/'
            if platform.system() == 'Windows':
               host_dir = 'C:/'

            stdout, stderr, ec = self.execute_docker_cmd(['run', '-p', '8888:8888', '-p', '9876:9876', '-p', '8080:8080', '-p', '3000:3000', '-p', '8000:8000', '-v', host_dir+':/host', '-d', '--name='+self._container, self._image, 'tail', '-f', '&>', '/dev/null', '&'])

   def abs_host_path(self, dir):
      abs_path = os.path.abspath(dir)
      if platform.system() == 'Windows':
         abs_path = abs_path[3:].replace('\\', '/') # remove the drive letter prefix and replace the separators
      else:
         abs_path = abs_path[1:]

      return '/host/'+abs_path
 
   def get_container(self):
      return self._container

   def get_image(self):
      return self._image

   def execute_docker_cmd(self, cmd):
      proc = subprocess.Popen(['docker']+cmd,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout, stderr = proc.communicate()
      return [stdout.decode('UTF-8'), stderr.decode('UTF-8'), proc.poll()]
   
   def file_exists(self, fn):
      return self.execute_cmd(['test', '-f', fn])[2] == 0
   
   def dir_exists(self, d):
      return self.execute_cmd(['test', '-d', d])[2] == 0

   def tar_dir(self, n, d):
      return self.execute_cmd(['tar', 'cvzf', n+'.tgz', d])
 
   def untar(self, d):
      return self.execute_cmd(['tar', 'xvzf', d])
   
   def cp_to_host(self, cf, hf):
      return self.execute_docker_cmd(['cp', self._container+":"+cf, hf])
   
   def cp_from_host(self, hf, cf):
      return self.execute_docker_cmd(['cp', hf, self._container+":"+cf])
   
   def rm(self, f):
      self.execute_cmd(['rm', '-rf', f])

   def find_pid(self, s):
      stdout, stderr, ec = self.execute_cmd(['ps', 'ax'])
      for line in stdout.splitlines(True):
         if "PID TTY" in line:
            continue
         else:
            if s in line:
               return line.split()[0]
      
      return -1
   
   def get_container_name(self):
      return self._container
   
   def commit(self, name):
      self.execute_docker_cmd(['commit', 'dune', 'dune'])

   def start(self):
      print("Starting docker container ["+self._container+"]") 
      self.execute_docker_cmd(['container', 'start', self._container])
   
   def stop(self):
      print("Stopping docker container ["+self._container+"]")
      self.execute_docker_cmd(['container', 'stop', self._container])

   def destroy(self):
      print("Destroying docker container ["+self._container+"]")
      self.execute_docker_cmd(['container', 'stop', self._container])
      self.execute_docker_cmd(['container', 'rm', self._container])

   def execute_cmd_at(self, dir, cmd):
      proc = subprocess.Popen(['docker', 'container', 'exec', '-w', dir, self._container]+cmd)
      proc.communicate()

   def execute_cmd(self, cmd):
      return self.execute_docker_cmd(['container', 'exec', self._container] + cmd)

   def execute_interactive_cmd(self, cmd):
      proc = subprocess.Popen(['docker', 'container', 'exec', '-i', self._container]+cmd)
      proc.communicate()
      #return self.execute_docker_cmd(['container', 'exec', '-i', self._container] + cmd)

   def execute_cmd2(self, cmd):
      proc = subprocess.Popen(['docker', 'container', 'exec', self._container] + cmd)
      proc.communicate()

   def execute_bg_cmd(self, cmd):
      return self.execute_cmd(cmd+['&'])