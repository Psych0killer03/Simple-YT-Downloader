from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QLineEdit, QRadioButton)
from pytube import YouTube
from pytube import Playlist
from moviepy.editor import *
import os

class Window(QWidget):
    def __init__(self):
        super().__init__()
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(300, 300, 400, 500)
        self.setFixedSize(500, 130)
        self.setWindowTitle('YT-Downloader by Psych0sisPy')
        self.setStyleSheet('background-color: gray')


        btn = QPushButton('Download from URL', self)
        btn.clicked.connect(lambda: self.on_click())
        btn.setToolTip('Press this button to download the video or playlist selected in the URL bar')
        btn.resize(120, 50)
        btn.move(self.frameGeometry().width() - btn.frameGeometry().width() - 10, self.frameGeometry().height() - btn.frameGeometry().height() - 10)
        btn.setStyleSheet('background-color: white;' 'selection-background-color: gray')


        self.textbox = QLineEdit(self)
        self.textbox.setToolTip('Enter YouTube URL')
        self.textbox.resize(480, 40)
        self.textbox.move(round(self.frameGeometry().width() / 2) - round(self.textbox.frameGeometry().width() / 2),
                          self.frameGeometry().height() - 110)
        self.textbox.setStyleSheet('background-color: white')

        self.audio = QRadioButton('Audio Only', self)
        self.audio.setToolTip('If checked will only download audio from source in MP3 format.')
        self.audio.resize(100, 20)
        self.audio.move(round(self.frameGeometry().width()) - round(btn.frameGeometry().width() + self.audio.frameGeometry().width()*2),
                        self.frameGeometry().height() - self.audio.frameGeometry().height() - 10)
        self.audio.setStyleSheet('background-color: rgba(0, 0, 0, 0)')

        self.video = QRadioButton('Video Only', self)
        self.video.setToolTip('If checked will only download video from source in MP4 format.')
        self.video.resize(100, 20)
        self.video.move(round(self.frameGeometry().width()) - round(btn.frameGeometry().width() + self.video.frameGeometry().width()),
                        self.frameGeometry().height() - self.video.frameGeometry().height() - 10)
        self.video.setStyleSheet('background-color: rgba(0, 0, 0, 0)')

        self.both = QRadioButton('Video and Audio', self)
        self.both.setToolTip('If checked will only download video from source in MP4 format.')
        self.both.resize(110, 20)
        self.both.move(round(self.frameGeometry().width()) - round(btn.frameGeometry().width() + self.audio.frameGeometry().width()*3 + 25),
                        self.frameGeometry().height() - self.audio.frameGeometry().height() - 10)
        self.both.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.both.setEnabled(True)

        self.show()
    def on_click(self):

        try:
            if not os.path.exists('Downloads/'):
                os.mkdir('Downloads/')
            directory = os.getcwd()
            os.chdir('Downloads')
            if 'playlist' in self.textbox.text():
                playlist = Playlist(self.textbox.text())
                name = playlist.title.replace("/", "").replace(':', '').replace('*', '').replace('?', '').replace('"',
                                                                                                                    '').replace(
                            "'", "").replace('<', '').replace('>', '').replace('|', '').replace('$', '').replace(',', '').replace('.', '')
                if not os.path.exists(name):
                    os.mkdir(name)
                os.chdir(name)
                if self.audio.isChecked() == True:
                    for url in playlist:

                        YouTube(url).streams.filter(file_extension='mp4' ,only_audio=True).first().download()
                        file = YouTube(url).title.replace("/", "").replace(':', '').replace('*', '').replace('?', '').replace('"',
                                                                                                                    '').replace(
                            "'", "").replace('<', '').replace('>', '').replace('|', '').replace('$', '').replace(',', '').replace('.', '')
                        mp4_file = f"{file}.mp4"
                        mp3_file = f"{file}.mp3"
                        audioclip = AudioFileClip(mp4_file)
                        audioclip.write_audiofile(mp3_file)
                        audioclip.close()
                        os.remove(mp4_file)
                elif self.video.isChecked() == True:
                    for url in playlist:
                        YouTube(url).streams.filter(only_video=True).order_by(
                            'resolution').desc().first().download()
                else:
                    for url in playlist:
                        YouTube(url).streams.filter(progressive=True).order_by('resolution').desc().first().download()
            else:
                yt = YouTube(self.textbox.text())
                file = yt.title.replace("/", "").replace(':', '').replace('*', '').replace('?', '').replace('"',
                                                                                                                    '').replace(
                            "'", "").replace('<', '').replace('>', '').replace('|', '').replace('$', '').replace(',', '').replace('.', '')
                os.mkdir(file)
                os.chdir(file)
                if self.audio.isChecked() == True:

                    yt.streams.filter(only_audio=True).first().download()


                    mp4_file = f"{file}.mp4"
                    mp3_file = f"{file}.mp3"

                    audioclip = AudioFileClip(mp4_file)
                    audioclip.write_audiofile(mp3_file)
                    audioclip.close()
                    os.remove(mp4_file)
                elif self.video.isChecked() == True:
                    yt.streams.filter(only_video=True).order_by(
                        'resolution').desc().first().download()
                else:
                    yt.streams.filter(progressive=True).order_by('resolution').desc().first().download()
            os.chdir(directory)
        except Exception as e:
            self.textbox.setText('Not a valid YouTube URL')
            os.chdir(directory)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())