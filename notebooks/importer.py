import sys
import os
from pathlib import Path
my_path = Path().absolute()
src_path = os.path.join(my_path, 'src')
sys.path.append(src_path)
