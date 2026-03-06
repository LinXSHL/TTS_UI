import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import tkinter.ttk as ttk
import asyncio
import edge_tts
import threading
import os
import platform
import subprocess

# --- 原始发音人数据（保留核心字段用于界面展示） ---
RAW_VOICE_DATA = """
af-ZA-AdriNeural Female Friendly, Positive
af-ZA-WillemNeural Male Friendly, Positive
am-ET-AmehaNeural Male Friendly, Positive
am-ET-MekdesNeural Female Friendly, Positive
ar-AE-FatimaNeural Female Friendly, Positive
ar-AE-HamdanNeural Male Friendly, Positive
ar-BH-AliNeural Male Friendly, Positive
ar-BH-LailaNeural Female Friendly, Positive
ar-DZ-AminaNeural Female Friendly, Positive
ar-DZ-IsmaelNeural Male Friendly, Positive
ar-EG-SalmaNeural Female Friendly, Positive
ar-EG-ShakirNeural Male Friendly, Positive
ar-IQ-BasselNeural Male Friendly, Positive
ar-IQ-RanaNeural Female Friendly, Positive
ar-JO-SanaNeural Female Friendly, Positive
ar-JO-TaimNeural Male Friendly, Positive
ar-KW-FahedNeural Male Friendly, Positive
ar-KW-NouraNeural Female Friendly, Positive
ar-LB-LaylaNeural Female Friendly, Positive
ar-LB-RamiNeural Male Friendly, Positive
ar-LY-ImanNeural Female Friendly, Positive
ar-LY-OmarNeural Male Friendly, Positive
ar-MA-JamalNeural Male Friendly, Positive
ar-MA-MounaNeural Female Friendly, Positive
ar-OM-AbdullahNeural Male Friendly, Positive
ar-OM-AyshaNeural Female Friendly, Positive
ar-QA-AmalNeural Female Friendly, Positive
ar-QA-MoazNeural Male Friendly, Positive
ar-SA-HamedNeural Male Friendly, Positive
ar-SA-ZariyahNeural Female Friendly, Positive
ar-SY-AmanyNeural Female Friendly, Positive
ar-SY-LaithNeural Male Friendly, Positive
ar-TN-HediNeural Male Friendly, Positive
ar-TN-ReemNeural Female Friendly, Positive
ar-YE-MaryamNeural Female Friendly, Positive
ar-YE-SalehNeural Male Friendly, Positive
az-AZ-BabekNeural Male Friendly, Positive
az-AZ-BanuNeural Female Friendly, Positive
bg-BG-BorislavNeural Male Friendly, Positive
bg-BG-KalinaNeural Female Friendly, Positive
bn-BD-NabanitaNeural Female Friendly, Positive
bn-BD-PradeepNeural Male Friendly, Positive
bn-IN-BashkarNeural Male Friendly, Positive
bn-IN-TanishaaNeural Female Friendly, Positive
bs-BA-GoranNeural Male Friendly, Positive
bs-BA-VesnaNeural Female Friendly, Positive
ca-ES-EnricNeural Male Friendly, Positive
ca-ES-JoanaNeural Female Friendly, Positive
cs-CZ-AntoninNeural Male Friendly, Positive
cs-CZ-VlastaNeural Female Friendly, Positive
cy-GB-AledNeural Male Friendly, Positive
cy-GB-NiaNeural Female Friendly, Positive
da-DK-ChristelNeural Female Friendly, Positive
da-DK-JeppeNeural Male Friendly, Positive
de-AT-IngridNeural Female Friendly, Positive
de-AT-JonasNeural Male Friendly, Positive
de-CH-JanNeural Male Friendly, Positive
de-CH-LeniNeural Female Friendly, Positive
de-DE-AmalaNeural Female Friendly, Positive
de-DE-ConradNeural Male Friendly, Positive
de-DE-FlorianMultilingualNeural Male Friendly, Positive
de-DE-KatjaNeural Female Friendly, Positive
de-DE-KillianNeural Male Friendly, Positive
de-DE-SeraphinaMultilingualNeural Female Friendly, Positive
el-GR-AthinaNeural Female Friendly, Positive
el-GR-NestorasNeural Male Friendly, Positive
en-AU-NatashaNeural Female Friendly, Positive
en-AU-WilliamMultilingualNeural Male Friendly, Positive
en-CA-ClaraNeural Female Friendly, Positive
en-CA-LiamNeural Male Friendly, Positive
en-GB-LibbyNeural Female Friendly, Positive
en-GB-MaisieNeural Female Friendly, Positive
en-GB-RyanNeural Male Friendly, Positive
en-GB-SoniaNeural Female Friendly, Positive
en-GB-ThomasNeural Male Friendly, Positive
en-HK-SamNeural Male Friendly, Positive
en-HK-YanNeural Female Friendly, Positive
en-IE-ConnorNeural Male Friendly, Positive
en-IE-EmilyNeural Female Friendly, Positive
en-IN-NeerjaExpressiveNeural Female Friendly, Positive
en-IN-NeerjaNeural Female Friendly, Positive
en-IN-PrabhatNeural Male Friendly, Positive
en-KE-AsiliaNeural Female Friendly, Positive
en-KE-ChilembaNeural Male Friendly, Positive
en-NG-AbeoNeural Male Friendly, Positive
en-NG-EzinneNeural Female Friendly, Positive
en-NZ-MitchellNeural Male Friendly, Positive
en-NZ-MollyNeural Female Friendly, Positive
en-PH-JamesNeural Male Friendly, Positive
en-PH-RosaNeural Female Friendly, Positive
en-SG-LunaNeural Female Friendly, Positive
en-SG-WayneNeural Male Friendly, Positive
en-TZ-ElimuNeural Male Friendly, Positive
en-TZ-ImaniNeural Female Friendly, Positive
en-US-AnaNeural Female Cartoon, Cute
en-US-AndrewMultilingualNeural Male Warm, Confident
en-US-AndrewNeural Male Warm, Confident
en-US-AriaNeural Female Positive, Confident
en-US-AvaMultilingualNeural Female Expressive, Caring
en-US-AvaNeural Female Expressive, Caring
en-US-BrianMultilingualNeural Male Approachable
en-US-BrianNeural Male Approachable
en-US-ChristopherNeural Male Reliable, Authority
en-US-EmmaMultilingualNeural Female Cheerful, Clear
en-US-EmmaNeural Female Cheerful, Clear
en-US-EricNeural Male Rational
en-US-GuyNeural Male Passion
en-US-JennyNeural Female Friendly, Comfort
en-US-MichelleNeural Female Friendly, Pleasant
en-US-RogerNeural Male Lively
en-US-SteffanNeural Male Rational
en-ZA-LeahNeural Female Friendly, Positive
en-ZA-LukeNeural Male Friendly, Positive
es-AR-ElenaNeural Female Friendly, Positive
es-AR-TomasNeural Male Friendly, Positive
es-BO-MarceloNeural Male Friendly, Positive
es-BO-SofiaNeural Female Friendly, Positive
es-CL-CatalinaNeural Female Friendly, Positive
es-CL-LorenzoNeural Male Friendly, Positive
es-CO-GonzaloNeural Male Friendly, Positive
es-CO-SalomeNeural Female Friendly, Positive
es-CR-JuanNeural Male Friendly, Positive
es-CR-MariaNeural Female Friendly, Positive
es-CU-BelkysNeural Female Friendly, Positive
es-CU-ManuelNeural Male Friendly, Positive
es-DO-EmilioNeural Male Friendly, Positive
es-DO-RamonaNeural Female Friendly, Positive
es-EC-AndreaNeural Female Friendly, Positive
es-EC-LuisNeural Male Friendly, Positive
es-ES-AlvaroNeural Male Friendly, Positive
es-ES-ElviraNeural Female Friendly, Positive
es-ES-XimenaNeural Female Friendly, Positive
es-GQ-JavierNeural Male Friendly, Positive
es-GQ-TeresaNeural Female Friendly, Positive
es-GT-AndresNeural Male Friendly, Positive
es-GT-MartaNeural Female Friendly, Positive
es-HN-CarlosNeural Male Friendly, Positive
es-HN-KarlaNeural Female Friendly, Positive
es-MX-DaliaNeural Female Friendly, Positive
es-MX-JorgeNeural Male Friendly, Positive
es-NI-FedericoNeural Male Friendly, Positive
es-NI-YolandaNeural Female Friendly, Positive
es-PA-MargaritaNeural Female Friendly, Positive
es-PA-RobertoNeural Male Friendly, Positive
es-PE-AlexNeural Male Friendly, Positive
es-PE-CamilaNeural Female Friendly, Positive
es-PR-KarinaNeural Female Friendly, Positive
es-PR-VictorNeural Male Friendly, Positive
es-PY-MarioNeural Male Friendly, Positive
es-PY-TaniaNeural Female Friendly, Positive
es-SV-LorenaNeural Female Friendly, Positive
es-SV-RodrigoNeural Male Friendly, Positive
es-US-AlonsoNeural Male Friendly, Positive
es-US-PalomaNeural Female Friendly, Positive
es-UY-MateoNeural Male Friendly, Positive
es-UY-ValentinaNeural Female Friendly, Positive
es-VE-PaolaNeural Female Friendly, Positive
es-VE-SebastianNeural Male Friendly, Positive
et-EE-AnuNeural Female Friendly, Positive
et-EE-KertNeural Male Friendly, Positive
fa-IR-DilaraNeural Female Friendly, Positive
fa-IR-FaridNeural Male Friendly, Positive
fi-FI-HarriNeural Male Friendly, Positive
fi-FI-NooraNeural Female Friendly, Positive
fil-PH-AngeloNeural Male Friendly, Positive
fil-PH-BlessicaNeural Female Friendly, Positive
fr-BE-CharlineNeural Female Friendly, Positive
fr-BE-GerardNeural Male Friendly, Positive
fr-CA-AntoineNeural Male Friendly, Positive
fr-CA-JeanNeural Male Friendly, Positive
fr-CA-SylvieNeural Female Friendly, Positive
fr-CA-ThierryNeural Male Friendly, Positive
fr-CH-ArianeNeural Female Friendly, Positive
fr-CH-FabriceNeural Male Friendly, Positive
fr-FR-DeniseNeural Female Friendly, Positive
fr-FR-EloiseNeural Female Friendly, Positive
fr-FR-HenriNeural Male Friendly, Positive
fr-FR-RemyMultilingualNeural Male Friendly, Positive
fr-FR-VivienneMultilingualNeural Female Friendly, Positive
ga-IE-ColmNeural Male Friendly, Positive
ga-IE-OrlaNeural Female Friendly, Positive
gl-ES-RoiNeural Male Friendly, Positive
gl-ES-SabelaNeural Female Friendly, Positive
gu-IN-DhwaniNeural Female Friendly, Positive
gu-IN-NiranjanNeural Male Friendly, Positive
he-IL-AvriNeural Male Friendly, Positive
he-IL-HilaNeural Female Friendly, Positive
hi-IN-MadhurNeural Male Friendly, Positive
hi-IN-SwaraNeural Female Friendly, Positive
hr-HR-GabrijelaNeural Female Friendly, Positive
hr-HR-SreckoNeural Male Friendly, Positive
hu-HU-NoemiNeural Female Friendly, Positive
hu-HU-TamasNeural Male Friendly, Positive
id-ID-ArdiNeural Male Friendly, Positive
id-ID-GadisNeural Female Friendly, Positive
is-IS-GudrunNeural Female Friendly, Positive
is-IS-GunnarNeural Male Friendly, Positive
it-IT-DiegoNeural Male Friendly, Positive
it-IT-ElsaNeural Female Friendly, Positive
it-IT-GiuseppeMultilingualNeural Male Friendly, Positive
it-IT-IsabellaNeural Female Friendly, Positive
iu-Cans-CA-SiqiniqNeural Female Friendly, Positive
iu-Cans-CA-TaqqiqNeural Male Friendly, Positive
iu-Latn-CA-SiqiniqNeural Female Friendly, Positive
iu-Latn-CA-TaqqiqNeural Male Friendly, Positive
ja-JP-KeitaNeural Male Friendly, Positive
ja-JP-NanamiNeural Female Friendly, Positive
jv-ID-DimasNeural Male Friendly, Positive
jv-ID-SitiNeural Female Friendly, Positive
ka-GE-EkaNeural Female Friendly, Positive
ka-GE-GiorgiNeural Male Friendly, Positive
kk-KZ-AigulNeural Female Friendly, Positive
kk-KZ-DauletNeural Male Friendly, Positive
km-KH-PisethNeural Male Friendly, Positive
km-KH-SreymomNeural Female Friendly, Positive
kn-IN-GaganNeural Male Friendly, Positive
kn-IN-SapnaNeural Female Friendly, Positive
ko-KR-HyunsuMultilingualNeural Male Friendly, Positive
ko-KR-InJoonNeural Male Friendly, Positive
ko-KR-SunHiNeural Female Friendly, Positive
lo-LA-ChanthavongNeural Male Friendly, Positive
lo-LA-KeomanyNeural Female Friendly, Positive
lt-LT-LeonasNeural Male Friendly, Positive
lt-LT-OnaNeural Female Friendly, Positive
lv-LV-EveritaNeural Female Friendly, Positive
lv-LV-NilsNeural Male Friendly, Positive
mk-MK-AleksandarNeural Male Friendly, Positive
mk-MK-MarijaNeural Female Friendly, Positive
ml-IN-MidhunNeural Male Friendly, Positive
ml-IN-SobhanaNeural Female Friendly, Positive
mn-MN-BataaNeural Male Friendly, Positive
mn-MN-YesuiNeural Female Friendly, Positive
mr-IN-AarohiNeural Female Friendly, Positive
mr-IN-ManoharNeural Male Friendly, Positive
ms-MY-OsmanNeural Male Friendly, Positive
ms-MY-YasminNeural Female Friendly, Positive
mt-MT-GraceNeural Female Friendly, Positive
mt-MT-JosephNeural Male Friendly, Positive
my-MM-NilarNeural Female Friendly, Positive
my-MM-ThihaNeural Male Friendly, Positive
nb-NO-FinnNeural Male Friendly, Positive
nb-NO-PernilleNeural Female Friendly, Positive
ne-NP-HemkalaNeural Female Friendly, Positive
ne-NP-SagarNeural Male Friendly, Positive
nl-BE-ArnaudNeural Male Friendly, Positive
nl-BE-DenaNeural Female Friendly, Positive
nl-NL-ColetteNeural Female Friendly, Positive
nl-NL-FennaNeural Female Friendly, Positive
nl-NL-MaartenNeural Male Friendly, Positive
pl-PL-MarekNeural Male Friendly, Positive
pl-PL-ZofiaNeural Female Friendly, Positive
ps-AF-GulNawazNeural Male Friendly, Positive
ps-AF-LatifaNeural Female Friendly, Positive
pt-BR-AntonioNeural Male Friendly, Positive
pt-BR-FranciscaNeural Female Friendly, Positive
pt-BR-ThalitaMultilingualNeural Female Friendly, Positive
pt-PT-DuarteNeural Male Friendly, Positive
pt-PT-RaquelNeural Female Friendly, Positive
ro-RO-AlinaNeural Female Friendly, Positive
ro-RO-EmilNeural Male Friendly, Positive
ru-RU-DmitryNeural Male Friendly, Positive
ru-RU-SvetlanaNeural Female Friendly, Positive
si-LK-SameeraNeural Male Friendly, Positive
si-LK-ThiliniNeural Female Friendly, Positive
sk-SK-LukasNeural Male Friendly, Positive
sk-SK-ViktoriaNeural Female Friendly, Positive
sl-SI-PetraNeural Female Friendly, Positive
sl-SI-RokNeural Male Friendly, Positive
so-SO-MuuseNeural Male Friendly, Positive
so-SO-UbaxNeural Female Friendly, Positive
sq-AL-AnilaNeural Female Friendly, Positive
sq-AL-IlirNeural Male Friendly, Positive
sr-RS-NicholasNeural Male Friendly, Positive
sr-RS-SophieNeural Female Friendly, Positive
su-ID-JajangNeural Male Friendly, Positive
su-ID-TutiNeural Female Friendly, Positive
sv-SE-MattiasNeural Male Friendly, Positive
sv-SE-SofieNeural Female Friendly, Positive
sw-KE-RafikiNeural Male Friendly, Positive
sw-KE-ZuriNeural Female Friendly, Positive
sw-TZ-DaudiNeural Male Friendly, Positive
sw-TZ-RehemaNeural Female Friendly, Positive
ta-IN-PallaviNeural Female Friendly, Positive
ta-IN-ValluvarNeural Male Friendly, Positive
ta-LK-KumarNeural Male Friendly, Positive
ta-LK-SaranyaNeural Female Friendly, Positive
ta-MY-KaniNeural Female Friendly, Positive
ta-MY-SuryaNeural Male Friendly, Positive
ta-SG-AnbuNeural Male Friendly, Positive
ta-SG-VenbaNeural Female Friendly, Positive
te-IN-MohanNeural Male Friendly, Positive
te-IN-ShrutiNeural Female Friendly, Positive
th-TH-NiwatNeural Male Friendly, Positive
th-TH-PremwadeeNeural Female Friendly, Positive
tr-TR-AhmetNeural Male Friendly, Positive
tr-TR-EmelNeural Female Friendly, Positive
uk-UA-OstapNeural Male Friendly, Positive
uk-UA-PolinaNeural Female Friendly, Positive
ur-IN-GulNeural Female Friendly, Positive
ur-IN-SalmanNeural Male Friendly, Positive
ur-PK-AsadNeural Male Friendly, Positive
ur-PK-UzmaNeural Female Friendly, Positive
uz-UZ-MadinaNeural Female Friendly, Positive
uz-UZ-SardorNeural Male Friendly, Positive
vi-VN-HoaiMyNeural Female Friendly, Positive
vi-VN-NamMinhNeural Male Friendly, Positive
zh-CN-XiaoxiaoNeural Female Warm
zh-CN-XiaoyiNeural Female Lively
zh-CN-YunjianNeural Male Passion
zh-CN-YunxiNeural Male Lively, Sunshine
zh-CN-YunxiaNeural Male Cute
zh-CN-YunyangNeural Male Professional, Reliable
zh-CN-liaoning-XiaobeiNeural Female Humorous
zh-CN-shaanxi-XiaoniNeural Female Bright
zh-HK-HiuGaaiNeural Female Friendly, Positive
zh-HK-HiuMaanNeural Female Friendly, Positive
zh-HK-WanLungNeural Male Friendly, Positive
zh-TW-HsiaoChenNeural Female Friendly, Positive
zh-TW-HsiaoYuNeural Female Friendly, Positive
zh-TW-YunJheNeural Male Friendly, Positive
zu-ZA-ThandoNeural Female Friendly, Positive
zu-ZA-ThembaNeural Male Friendly, Positive
"""

class TTSConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文字转MP3语音工具")
        # 进一步增加高度以容纳新的下拉框模块
        self.root.geometry("700x600")
        self.root.minsize(600, 550)
        
        # 解析语音列表，用于下拉框展示
        self.voice_display_list = self.parse_voice_data()
        
        self.setup_ui()

    def parse_voice_data(self):
        """解析文本常量中的发音人数据，生成UI展示列表"""
        display_list = []
        for line in RAW_VOICE_DATA.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                gender = parts[1]
                # 把后面代表特征的文字拼接起来
                desc = " ".join(parts[2:]) if len(parts) > 2 else "General"
                # 格式化展示内容，例如：zh-CN-YunjianNeural  [Male - Passion]
                display_str = f"{name}  [{gender} - {desc}]"
                display_list.append(display_str)
        return display_list

    def setup_ui(self):
        """初始化界面布局 (工作流扩展为4步)"""
        # --- 第一步：文本输入区 ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(15, 5))
        
        lbl_step1 = tk.Label(top_frame, text="第一步：输入或导入需要转换的文字", font=("微软雅黑", 10, "bold"))
        lbl_step1.pack(anchor="w", pady=(0, 5))

        self.text_area = scrolledtext.ScrolledText(top_frame, wrap=tk.WORD, font=("微软雅黑", 11))
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.btn_import = tk.Button(top_frame, text="从TXT文件导入文字", command=self.load_txt_file)
        self.btn_import.pack(anchor="e", pady=5)

        # --- 第二步：发音人选择区 (新增) ---
        voice_frame = tk.Frame(self.root)
        voice_frame.pack(fill=tk.X, padx=20, pady=(5, 10))

        lbl_step2 = tk.Label(voice_frame, text="第二步：选择发音人 (声音/角色)", font=("微软雅黑", 10, "bold"))
        lbl_step2.pack(anchor="w", pady=(0, 5))
        
        # 使用 ttk.Combobox 创建下拉框
        self.combo_voice = ttk.Combobox(voice_frame, values=self.voice_display_list, state="readonly", font=("微软雅黑", 10))
        self.combo_voice.pack(fill=tk.X)
        
        # 默认选中中文男声 YunjianNeural (通过遍历查找索引)
        default_index = 0
        for i, v in enumerate(self.voice_display_list):
            if "zh-CN-YunjianNeural" in v:
                default_index = i
                break
        self.combo_voice.current(default_index)

        # --- 第三步：保存路径区 ---
        mid_frame = tk.Frame(self.root)
        mid_frame.pack(fill=tk.X, padx=20, pady=(5, 10))

        lbl_step3 = tk.Label(mid_frame, text="第三步：设置MP3保存位置", font=("微软雅黑", 10, "bold"))
        lbl_step3.pack(anchor="w", pady=(0, 5))

        path_subframe = tk.Frame(mid_frame)
        path_subframe.pack(fill=tk.X)

        self.path_var = tk.StringVar()
        self.entry_path = tk.Entry(path_subframe, textvariable=self.path_var, font=("微软雅黑", 10))
        self.entry_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.btn_browse = tk.Button(path_subframe, text="浏览文件夹...", command=self.browse_save_path, width=12)
        self.btn_browse.pack(side=tk.RIGHT)

        # --- 第四步：核心启动按钮区 ---
        bottom_frame = tk.Frame(self.root, pady=15)
        bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.lbl_status = tk.Label(bottom_frame, text="状态: 准备就绪，请填写以上信息", fg="#009688", font=("微软雅黑", 10))
        self.lbl_status.pack(pady=(0, 10))

        self.btn_convert = tk.Button(bottom_frame, text="▶ 一键生成MP3音频", command=self.start_conversion, 
                                     bg="#FF5722", fg="white", font=("微软雅黑", 14, "bold"), 
                                     width=20, height=2, cursor="hand2")
        self.btn_convert.pack()

    def load_txt_file(self):
        file_path = filedialog.askopenfilename(
            parent=self.root, title="选择TXT文件", filetypes=[("TXT文档", "*.txt")]
        )
        if not file_path: return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.lbl_status.config(text="状态: TXT文件读取成功！", fg="green")
        except Exception as e:
            messagebox.showerror("读取失败", f"文件读取报错：\n{str(e)}", parent=self.root)

    def browse_save_path(self):
        path = filedialog.asksaveasfilename(
            parent=self.root, title="保存MP3音频文件", 
            defaultextension=".mp3", filetypes=[("MP3音频", "*.mp3")],
            initialfile="我的合成语音.mp3"
        )
        if path: self.path_var.set(path)

    def start_conversion(self):
        text = self.text_area.get(1.0, tk.END).strip()
        output_path = self.path_var.get().strip()
        
        # 获取下拉框当前选中的值，并提取出真正的Voice ID (即按空格分割的第一部分)
        selected_voice_display = self.combo_voice.get()
        actual_voice_id = selected_voice_display.split()[0]
        
        if not text:
            messagebox.showwarning("缺少文字", "请先在上方输入需要转换的文字内容！", parent=self.root)
            return
        if not actual_voice_id:
            messagebox.showwarning("缺少发音人", "请在下拉框中选择一个发音人！", parent=self.root)
            return
        if not output_path:
            messagebox.showwarning("缺少路径", "请点击【浏览文件夹...】设置MP3的保存位置！", parent=self.root)
            return
            
        if not output_path.lower().endswith('.mp3'):
            output_path += '.mp3'
            self.path_var.set(output_path)

        # 冻结界面防止重复点击
        self.btn_convert.config(state=tk.DISABLED, text="⏳ 正在拼命生成中...", bg="#9E9E9E")
        self.btn_import.config(state=tk.DISABLED)
        self.btn_browse.config(state=tk.DISABLED)
        self.combo_voice.config(state=tk.DISABLED)
        self.lbl_status.config(text=f"状态: 正在使用 {actual_voice_id} 转换，请稍候...", fg="#FF9800")

        # 启动后台线程 (传入提取出的实际语音ID)
        thread = threading.Thread(target=self.run_tts_thread, args=(text, actual_voice_id, output_path))
        thread.daemon = True
        thread.start()

    def run_tts_thread(self, text, voice_id, output_file):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._edge_tts_logic(text, voice_id, output_file))
            self.root.after(0, self.on_conversion_success, output_file)
        except Exception as e:
            self.root.after(0, self.on_conversion_error, str(e))
        finally:
            loop.close()

    async def _edge_tts_logic(self, text, voice_id, output_file):
        # 此时传入用户选择的动态 voice_id
        communicate = edge_tts.Communicate(text, voice_id)
        submaker = edge_tts.SubMaker()
        
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    def on_conversion_success(self, final_path):
        self._reset_ui()
        self.lbl_status.config(text="状态: 🎉 音频生成成功！", fg="green")
        
        if messagebox.askyesno("生成完毕", "MP3音频已成功生成！\n\n是否立即打开文件所在的文件夹？", parent=self.root):
            self.open_file_folder(final_path)

    def on_conversion_error(self, error_msg):
        self._reset_ui()
        self.lbl_status.config(text="状态: ❌ 生成失败", fg="red")
        messagebox.showerror("生成出错", f"程序在生成音频时遇到错误：\n{error_msg}", parent=self.root)

    def _reset_ui(self):
        self.btn_convert.config(state=tk.NORMAL, text="▶ 一键生成MP3音频", bg="#FF5722")
        self.btn_import.config(state=tk.NORMAL)
        self.btn_browse.config(state=tk.NORMAL)
        self.combo_voice.config(state="readonly")

    def open_file_folder(self, file_path):
        try:
            abs_path = os.path.abspath(file_path)
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer /select,"{abs_path}"')
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-R", abs_path])
            else:
                subprocess.Popen(["xdg-open", os.path.dirname(abs_path)])
        except Exception as e:
            print(f"打开文件夹失败: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TTSConverterApp(root)
    root.mainloop()
