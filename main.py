import os
import time

from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
from win32con import FILE_FLAG_BACKUP_SEMANTICS
from win32con import FILE_SHARE_WRITE
from win32file import CloseHandle
from win32file import CreateFile
from win32file import GENERIC_WRITE
from win32file import OPEN_EXISTING
from win32file import SetFileTime


def get_file_time(filename):
  filename = os.path.abspath(filename)
  # 创建时间
  create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(filename)))
  # 修改时间
  update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(filename)))
  # 访问时间
  access_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getatime(filename)))
  return create_time, update_time, access_time

def modify_file_create_time(filename, create_time_str, update_time_str, access_time_str):
    try:
        format_str = "%Y-%m-%d %H:%M:%S"  # 时间格式
        # f = CreateFile(filename, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        f = CreateFile(filename, GENERIC_WRITE, FILE_SHARE_WRITE, None, OPEN_EXISTING,
                       FILE_FLAG_BACKUP_SEMANTICS, 0)
        create_time = Time(time.mktime(time.strptime(create_time_str, format_str)))
        update_time = Time(time.mktime(time.strptime(update_time_str, format_str)))
        access_time = Time(time.mktime(time.strptime(access_time_str, format_str)))
        SetFileTime(f, create_time, update_time, access_time)
        CloseHandle(f)
        print('update file time success:{}/{}/{}'.format(create_time_str, update_time_str,
                                                         access_time_str))
    except Exception as e:
        print('update file time fail:{}'.format(e))


if __name__ == '__main__':
    cTime = "2019-12-13 21:51:02"  # 创建时间
    mTime = "2019-02-02 00:01:03"  # 修改时间
    aTime = "2019-02-02 00:01:04"  # 访问时间
    fName = r"2.jpg"  # 可以是文件也可以是文件夹

    for file in os.listdir('.'):

        try:
            if file.split('.')[1] in ['jpg','jpeg','png','mp4']:
                up = get_file_time(file)[1]
                modify_file_create_time(file, up, up, up)
                time.sleep(1)
        except:
            continue