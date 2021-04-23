import subprocess
import re           #for using regular expression
import os

class AdbCmd():
    def __init__(self):
        self.deviceID = 0
        self.str_cmd('adb start-server')

    def str_cmd(self, command, type=True):
        popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        (stdoutdata, stderrdata) = popen.communicate()
        return (stdoutdata[:-1], stderrdata[:-1])
        
    # if Error Occur, return type is 'str'
    # or normal return case, return type is 'tuple', (Device ID, Device Model)
    def devices(self):
        (list_deviceID, err_list_deviceID) = self.str_cmd('adb devices')
        list_deviceID = re.sub('device|\t', '' , list_deviceID).split('\n') #clearance, just remain device ID number
        (list_deviceModel, err_list_deviceModel) = self.str_cmd('adb shell getprop ro.product.model')
        if (len(list_deviceID) < 3):    # Detect 0 Device
            return -1
        elif (len(err_list_deviceModel) != 0):  # Detect more than 2 Devices
            return err_list_deviceModel
        else:
            return (list_deviceID[1], list_deviceModel) # Detect just one Device

    # if Error Occur, return type is 'str'
    # or normal return case, return type is 'tuple', (Device ID, Device Model)
    def extract_list_pkg(self):
        (raw_app_path, err_raw_app_path) = self.str_cmd('adb shell pm list packages -f')
        if (len(err_raw_app_path) == 0):
            pkg_list = raw_app_path.split('\n')
            pkg_list = [[i[i.rfind('=')+1:], i[i.find(':')+1:i.rfind('=')]] for i in pkg_list]
            pkg_list.sort()
            with open('pkg_list.log', 'w') as file_pkglist:         #just for log files
                for newline_pkg in pkg_list:
                    if newline_pkg[0] != "android":
                        # file_pkglist.write(newline_pkg[0] + ', ' + newline_pkg[1] +'\n')     
                        file_pkglist.write(newline_pkg[0]+'\n')     
            return pkg_list
        else:
            return err_raw_app_path
    
    def import_list_pkg(self, logfile_path='pkg_list.log'):
        pkg_list=[]
        try:
            log_file = open(logfile_path, 'r')
            for line in log_file:
                [pkg_name, pkg_path]=line.split(',')
                pkg_list.append([pkg_name, pkg_path[:-1]])
            return pkg_list
        except:
            return "file path not found"

    def install_pkg(self, pkgfile_name):
        (log, err) = self.str_cmd('adb shell pm install {}.apk'.format(pkgfile_name))
        if (len(err) != 0):
            return err
        else:
            return log

    def delete_pkg(self, pkg_name, delete_data=True):
        if (delete_data == True):
            (log, err) = self.str_cmd('adb shell pm uninstall {}'.format(pkg_name))
        else:
            (log, err) = self.str_cmd('adb shell pm uninstall -k {}'.format(pkg_name))    
        if (len(err) != 0):
            return err
        else:
            return log

    def disable_pkg(self, pkg_name):
        (log, err) = self.str_cmd('adb shell pm disable {}'.format(pkg_name))
        if (len(err) != 0):
            return err
        else:
            return log

    def enable_pkg(self, pkg_name):
        (log, err) = self.str_cmd('adb shell pm enable {}'.format(pkg_name))
        if (len(err) != 0):
            return err
        else:
            return log

    def backup_pkg(self, pkg_path, pkg_name):
        try:
            if not os.path.exists('backup_apk'):
                os.makedirs('backup_apk')
        except OSError:
            return ('Error: Creating directory backup_apk')
        (log, err) = self.str_cmd('adb pull {} backup_apk\{}.apk'.format(pkg_path, pkg_name))
        if (len(err) != 0):
            return err
        else:
            return log

    def kill(self):
        self.str_cmd('adb kill-sever')

def main():
    adb = AdbCmd()
    adb.kill
    deviceID = adb.devices()
    if (str(type(deviceID)) == "<class 'tuple'>"):
        print (deviceID)
        list = adb.extract_list_pkg()
        # adb.backup_pkg(list[162][1], list[162][0])

        # print (adb.install_pkg('com.kyobo.ebook.b2b.phone.type3'))
        # print (adb.delete_pkg('com.kyobo.ebook.b2b.phone.type3'))
        
        adb.kill
    else:
        adb.kill
    

if __name__ == "__main__":
    main()  



# 1. Android 버전 확인
#   adb shell getprop ro.build.version.release

# 2. SDK 버전 확인
#   adb shell getprop ro.build.version.sdk

# 3. Android Setting 열기
#   adb shell am start -n com.android.settings/com.android.settings.Settings

# 4. APK 설치
#   adb install -r APK_FILE

# 5. APK 제거
#   adb unintall 패키지명

# 6. 장치 모델명 확인
#   adb shell getprop ro.product.model

# 7. 화면 해상도 확인
#    adb shell dupsys window | grep DisplayWidth

# 9. Screenshot 저장
#    adb shell /system/bin/screencap -p 장치내경로

# 10. 장치 검색
#    adb devices

# 11. 장치 재부팅
#    adb reboot 

# 12. adb 종료
#    adb kill-sever

# 13. adb 실행
#    adb start-server

# 14. 장치의 파일 가져오기
#    adb pull 장치내경로 PC내경로

# 15. 장치로 파일 복사하기
#     adb push PC내경로 장치내경로

# 18. 장치 작동 시간 확인
#     adb uptime