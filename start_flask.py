import subprocess
import time

# 启动Flask应用
print('正在启动Flask应用...')
process = subprocess.Popen(['python', 'app.py'], shell=True)
time.sleep(3)
print('Flask应用已启动，请在浏览器中访问 http://localhost:5000')
