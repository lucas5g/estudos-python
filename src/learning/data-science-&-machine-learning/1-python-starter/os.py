import os

os.getcwd()
os.listdir()

actual_dir = os.getcwd()
# os.chdir('/Users/lucas')
# os.chdir('test')

os.mkdir('Pasta')

os.rename('test.txt', 'test2.txt')

os.rmdir('Pasta')

os.system('date')

os.path.join(os.getcwd(), 'pasta')

os.getcwd() + '/pasta'

os.path.basename(os.getcwd())

os.getcwd().split('/')[-1]

os.path.split()


curr_dir = os.getcwd()

curr_dir
lt = os.path.getmtime(curr_dir)

from datetime import datetime 

datetime.utcfromtimestamp(lt)

os.path.isfile(curr_dir)
os.path.isdir(curr_dir)