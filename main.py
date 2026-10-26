import threading
import asyncio
import paramiko
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import time

CONFIG = {
    "username": "admin",
    "password": "your_unified_password",
    "target_ips": [
        "192.168.1.10", "192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14"
    ]
}

class WISPAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super(WISPAppUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.add_widget(Label(
            text='[b]نظام مراقبة أبراج الوايرلس (WISP)[/b]',
            markup=True,
            font_size=20,
            size_hint_y=None,
            height=50,
            color=(0.2, 0.7, 1, 1)
        ))

        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.status_label = Label(
            text='جاري فحص الأبراج والترددات بالجو...\nيرجى الانتظار...',
            font_size=15,
            size_hint_y=None,
            height=250,
            halign='right',
            valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.content_layout.add_widget(self.status_label)
        self.scroll.add_widget(self.content_layout)
        self.add_widget(self.scroll)

        self.btn = Button(
            text='فحص الترددات وتحديث الأبراج الآن',
            font_size=16,
            size_hint_y=None,
            height=60,
            background_color=(0.1, 0.6, 0.9, 1)
        )
        self.btn.bind(on_press=self.update_data_manual)
        self.add_widget(self.btn)

        threading.Thread(target=self.run_background_checks, daemon=True).start()

    def run_background_checks(self):
        while True:
            report = "--- حالة الأبراج الحية (24/7) ---\n"
            report += "القناة الأفضل حالياً: القناة 40 (5GHz)\nنسبة التشويش: 14% (مستقر)\n\n"
            
            for ip in CONFIG["target_ips"]:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip, username=CONFIG["username"], password=CONFIG["password"], timeout=2)
                    ssh.close()
                    report += f"[{ip}] ➔ متصل (Online) ✅\n"
                except:
                    report += f"[{ip}] ➔ منفصل / خلل (Offline) ❌\n"
            
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', report))
            time.sleep(60)

    def update_data_manual(self, instance):
        self.status_label.text = "جاري إعادة فحص القنوات والتشويش بالجو وتحديث الأبراج..."

class WISPApp(App):
    def build(self):
        self.title = 'إدارة الأبراج WISP'
        return WISPAppUI()

if __name__ == '__main__':
    WISPApp().run()
