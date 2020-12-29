from picamera import PiCamera
from time import sleep
import os
from gpiozero import LED

camera = PiCamera(resolution=(1640,1232))
light = LED(26, False)

def capture(fname):
    light.on()
    camera.capture(fname)
    light.off()

def take_preview(seconds):
    '''(int) -> NoneType
    Previews the camera for time (seconds)
    '''
    
    camera.start_preview()
    sleep(seconds)
    camera.stop_preview()

def delayed_capture(seconds, filename):
    '''(number, string) -> NoneType

    Captures an image with name filename after
    a preview of seconds seconds'''
    
    camera.start_preview()
    sleep(seconds)
    camera.stop_preview()
    capture(filename)

def timelapse(repeat_number, delay, file_key_word):
    '''(int, number) -> NoneType

    Captures images repeat_number times with delay seconds between
    each capture. Also logs data about the timelapse.'''
    
    z = file_key_word
    x = 0
    
    #logging timelapse information for future reference
    fhand = open('{0}_log.txt'.format(z), 'w')
    import datetime
    fhand.write('start date and time\n')
    fhand.write(str(datetime.datetime.now()))
    fhand.write('\n')
    fhand.write('number of captures\n')
    fhand.write(str(repeat_number))
    fhand.write('\n')
    fhand.write('delay between captures\n')
    fhand.write('{0}{1}'.format(delay, ' seconds'))
    fhand.close()
    while x != repeat_number:
        n = "{0}_{1}.jpg".format(z, x)
        capture(n)
        x = x + 1
        sleep(delay)
        
def long_timelapse(repeats, Ldelay, file_key_word):
    '''(int, number) -> NoneType

    captures timelapse. First parameter is the number of images.
    The second paramenter is the delay, measured in minutes
    '''
    
    timelapse(repeats, Ldelay * 60, file_key_word)
    
def VLtimelapse(repeats, VLdelay, file_key_word):
    '''(int, number) -> NoneType
    like timelapse or long_timelapse, but delay is measured in hours
    '''
    
    timelapse(repeats, VLdelay*60*60, file_key_word)


def take_video(time, filename):
    '''(int, str) -> NoneType

    takes a video for time seconds and names it filename
    with the extension .h264
    '''
    
    file = filename + '.h264'
    camera.start_recording(file)
    sleep(time)
    camera.stop_recording()


def make_experiment_folder(folder_name):
    '''(str) -> NoneType

    Creates a new folder in the present directory named folder_name
    '''
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

def save_to_particular_folder(folder):
    '''(str) -> str

    Returns the file path to the folder, assuming the folder has been created in the present directory.
    '''
    
    save_path = "/home/pi/imaging/" + folder + '/'
    return save_path


def improved_menu(choice=''):
    folder = input("Input a folder name to save your experiment in: ")
    make_experiment_folder(folder)
    save_to = save_to_particular_folder(folder)

    while choice != 1:
        try:
            choice = int(input('''Menu
-----------------------------------------
The following options are currently available

1. leave this menu

2. preview the camera

3. take a picture

4. take a timelapse

5. take a video

6. change the save location
--------------------------------------------

enter the number of the desired action: '''))
        except:
            print('\nAn error occured.\nMake sure you enter valid input.\n')
            continue

        if choice == 1:
            print('menu left')
            break

        elif choice == 2:
            preview_length = input("Enter the number of seconds for the camera preview to run:")
            preview_len = float(preview_length)
            take_preview(preview_len)

        elif choice == 3:
            picture_delay = input("How many seconds would you like to delay the picture? (enter 0 if you don't want a delay):")
            if picture_delay == 'zero':
                pic_delay = 0
            else:
                pic_delay = float(picture_delay)

            file_name = input("enter a filename for your picture (make sure to include the extension (.jpg, .gif, etc)):")
            delayed_capture(pic_delay, save_to + file_name)

        elif choice == 4:
            delay_unit = input("Should the time between captures be measured in hours, minutes, or seconds? [hours/minutes/seconds]:")
            number_repeats = input("Enter the number of captures:")
            repeat_num = int(number_repeats)
            delay_is = input("Enter the delay between captures:")
            delay = float(delay_is)
            keyword = input("Enter a keyword for the timelapse images:")
            
            if delay_unit == 'seconds':
                timelapse(repeat_num, delay, save_to + keyword)
            
            if delay_unit == 'minutes':
                long_timelapse(repeat_num, delay, save_to + keyword)
            
            if delay_unit == 'hours':
                VLtimelapse(repeat_num, delay, save_to + keyword)

        elif choice == 5:
            video_len_type = input('Do you want the video length to be measured in hours, seconds, or minutes? [hours/minutes/seconds]:')
            prompt_for_name = input("What should the video's name be? enter here:")
            video_len = 'how long should the video be? enter here:'

            if video_len_type == 'hours':
                len_vid = input(video_len)
                vid_len = eval(len_vid)
                take_video(vid_len*60*60, save_to + prompt_for_name)

            if video_len_type == 'minutes':
                len_vid = input(video_len)
                vid_len = eval(len_vid)
                take_video(vid_len*60, save_to + prompt_for_name)

            if video_len_type == 'seconds':
                len_vid = input(video_len)
                vid_len = eval(len_vid)
                take_video(vid_len, save_to + prompt_for_name)
        elif choice == 6:
            folder = input("Input a folder name to save your experiment in: ")
            make_experiment_folder(folder)
            save_to = save_to_particular_folder(folder)
        else:
            print('\nyou seem to have entered invalid input.\n')

if __name__ == '__main__':
    try:
        improved_menu()
    except e:
        raise e # we don't actually want to deal with this,
    finally:
        camera.close() # just make sure this always happens.
        light.close() # this should also always happen.
