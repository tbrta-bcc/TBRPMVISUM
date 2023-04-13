import os
import shutil

scname  = Visum.Net.AttValue("SC_NAME")
parent_dir=(os.path.join(Visum.GetPath(2), "outputs"))
path=os.path.join(parent_dir,scname)
isExist=os.path.exists(path)
if not isExist:
  os.mkdir(path)
  os.mkdir(os.path.join(path,"matrix"))
  os.mkdir(os.path.join(path,"panda"))
  os.mkdir(os.path.join(path,"skims"))
  os.mkdir(os.path.join(path,"summaries"))
  src=(os.path.join(Visum.GetPath(2), "libraries\\HTML"))
  destination=(os.path.join(path,"HTML"))
  shutil.copytree(src, destination)