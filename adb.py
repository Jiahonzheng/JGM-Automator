import subprocess
import time
import multiprocessing
from utility import randomize_offset, randomize_scale


class Adb():
    def __init__(self):
        assert self.is_correctly_connected(
        ), 'Make sure ADB is correctly configured and only one device is connected.'

    def is_correctly_connected(self):
        '''
        Return True if ADB enrivonment is correctly configured and only one divice is connected.
        '''
        output = subprocess.check_output(
            "adb devices", shell=True).decode('utf-8')
        if output.startswith('List of devices attached') and output.count('device') == 2:
            return True
        else:
            return False

    def get_screenshot(self, filename):
        '''
        Get screenshot and save as 'filename'
        '''
        subprocess.check_output(
            'adb shell screencap -p /sdcard/{}'.format(filename), shell=True)
        subprocess.check_output(
            'adb pull /sdcard/{}'.format(filename), shell=True)
        # print('Get screenshot {}'.format(filename))

    def get_screenshot_while_touching(self, filename, location, pressed_time=6):
        '''
        Get screenshot with screen touched.
        Multiprocess or Multithread is needed.
        '''
        p = multiprocessing.Process(
            target=self.tap_continuously, args=[location, pressed_time])
        p.start()
        time.sleep(2)
        self.get_screenshot(filename)
        time.sleep(0.5)
        p.join()

    def tap(self, location, with_bias=True):
        '''
        slightly tap.
        location: (x, y)
        '''
        if with_bias:
            location = map(randomize_offset, location)

        subprocess.check_output(
            'adb shell input touchscreen tap {} {}'.format(*location), shell=True)

    def tap_continuously(self, location, duration):
        '''
        Seems there is no direct ADB command to do this.
        So just swipe from a location to the same location.
        '''
        self.swipe(location, location, duration * 1000)

    def tap_periodically(self, location, times, interval=0.2):
        for _ in range(times):
            self.tap(location)
            time.sleep(interval)

    def swipe(self, start, end, duration=400, with_bias=True):
        '''
        swipe from start point to end point,
        duration is the total time consumed, used to control speed.
        '''
        if with_bias:
            start = map(randomize_offset, start)
            end = map(randomize_offset, end)
            duration = int(randomize_scale(duration))

        subprocess.check_output('adb shell input touchscreen swipe {} {} {} {} {}'.format(
            *start, *end, duration), shell=True)


if __name__ == '__main__':
    adb = Adb()
    # time.sleep(5)
    # adb.get_screenshot('eee.png')