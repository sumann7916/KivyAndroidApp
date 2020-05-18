import pytube
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
import certifi
import os
from android.permissions import request_permissions, Permission
from android.storage import primary_external_storage_path
from android.storage import app_storage_path
from android.storage import secondary_external_storage_path


# For android
request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
Permission.READ_EXTERNAL_STORAGE])

settings_path = app_storage_path()

primary_ext_storage = primary_external_storage_path()

secondary_ext_storage = secondary_external_storage_path()
os.environ['SSL_CERT_FILE'] = certifi.where()


class MenuWindow(Screen):
    url = ObjectProperty(None)
    audio = ObjectProperty(None)
    video = ObjectProperty(None)

    def paste(self):
        self.url.text = Clipboard.paste()

    # For choosing between audio and video

    def urlerror(self):
        content = Button(text='OK', size_hint=(.4, .8))
        errorpopup = Popup(title='Enter a valid URL',
                           size_hint=(.3, .3), content=content)
        errorpopup.open()
        content.bind(on_press=errorpopup.dismiss)



    def download(self):
    #try:
        url = self.url.text
        yt = pytube.YouTube(url)
        title = yt.title
        video = yt.streams.filter(subtype='mp4', progressive=True).first()
        audio = yt.streams.filter(only_audio=True).first()

        os.chdir(primary_ext_storage)

        if not os.path.exists("YTDownloads"):
            os.makedirs("YTDownloads")
        path = primary_ext_storage + '/YTDownloads/'
        if self.ids.audio.source == 'checked.png':
            file = audio
        else:
            file = video
        file.download(path)
        #Handling errors in case of Invalid URL
    #except R
        #self.urlerror()






    def audio_down(self):
        self.ids.audio.source = 'checked.png'
        self.ids.video.source = 'multimedia.png'

    def video_down(self):
        self.ids.video.source = 'checked.png'
        self.ids.audio.source = 'technology.png'



class AudioButton(ButtonBehavior, Image):
    pass


class PasteButton(ButtonBehavior, Image):
    pass


class VideoButton(ButtonBehavior, Image):
    pass


class DownloadManager(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class DownloadButton(ButtonBehavior, Image):
    pass


class MyURL(TextInput):
    pass


# Popups
class ErrorPopup(Popup):
    pass



kv = Builder.load_file("my.kv")


class MyApp(App):
    def build(self):
        return kv




if __name__ == "__main__":
    MyApp().run()
