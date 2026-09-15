import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import yt_dlp

class VideoDownloaderApp(App):
    def build(self):
        self.title = 'Video Downloader'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(
            text='[b]Video Downloader[/b]',
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=80
        ))
        
        self.url_input = TextInput(
            hint_text='الصق رابط الفيديو هنا...',
            multiline=False,
            size_hint_y=None,
            height=60
        )
        layout.add_widget(self.url_input)
        
        self.download_btn = Button(
            text='تحميل الفيديو',
            size_hint_y=None,
            height=70
        )
        self.download_btn.bind(on_press=self.start_download)
        layout.add_widget(self.download_btn)
        
        self.progress_bar = ProgressBar(max=100)
        layout.add_widget(self.progress_bar)
        
        self.status_label = Label(
            text='جاهز للتحميل',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.status_label)
        
        return layout
    
    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = 'الرجاء إدخال رابط صالح'
            return
        
        self.download_btn.disabled = True
        self.status_label.text = 'جاري التحميل...'
        
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_video(self, url):
        try:
            download_path = '/storage/emulated/0/Download'
            if not os.path.exists(download_path):
                download_path = os.getcwd()
            
            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'format': 'best[ext=mp4]/best',
                'progress_hooks': [self.progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            Clock.schedule_once(lambda dt: self.download_complete(True))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.download_complete(False, str(e)))
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent = float(d.get('_percent_str', '0%').replace('%', '').strip())
                Clock.schedule_once(lambda dt: self.update_progress(percent))
            except:
                pass
    
    def update_progress(self, percent):
        self.progress_bar.value = percent
        self.status_label.text = f'جاري التحميل... {percent:.1f}%'
    
    def download_complete(self, success, error=None):
        self.download_btn.disabled = False
        if success:
            self.status_label.text = 'تم التحميل بنجاح!'
            self.progress_bar.value = 100
        else:
            self.status_label.text = f'فشل: {error[:50] if error else "خطأ غير معروف"}'
            self.progress_bar.value = 0

if __name__ == '__main__':
    VideoDownloaderApp().run()
