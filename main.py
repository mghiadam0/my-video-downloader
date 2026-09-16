import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class VideoDownloaderApp(App):
    def build(self):
        self.title = 'Video Downloader'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(
            text='Video Downloader',
            font_size='24sp',
            size_hint_y=None,
            height=80
        ))
        
        self.url_input = TextInput(
            hint_text='Paste video URL here...',
            multiline=False,
            size_hint_y=None,
            height=60
        )
        layout.add_widget(self.url_input)
        
        self.download_btn = Button(
            text='Download',
            size_hint_y=None,
            height=70
        )
        self.download_btn.bind(on_press=self.start_download)
        layout.add_widget(self.download_btn)
        
        self.status_label = Label(
            text='Ready (Test build)',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.status_label)
        
        return layout
    
    def start_download(self, instance):
        self.status_label.text = 'Test build - yt-dlp removed for now'

if __name__ == '__main__':
    VideoDownloaderApp().run()
