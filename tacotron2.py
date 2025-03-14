
from TTS.api import TTS


text="""
「啊」魏贞浑身浪肉一颤，蜜穴紧紧夹住我的大肉棒，处女般紧致的温暖嫩
肉把我裹得倒吸一口冷气。我抽了一记屁光，命令道：「学牛叫。」随即大力抽
插起来，外面传来魏贞「哞哞」的叫声。这个奶子和屁股都大到不可思议的骚货，
被我用后入式干得世界第一的肥奶乱摇，嘴里发出牛鸣声，真是活脱脱一头变态
大奶牛啊。外面街上人山人海的观众显然被眼前的景象震撼了，疯狂地喊着「神
牛」，甚至都有人跪了下来，要膜拜我这位驯服神牛的主人。

"""

# 初始化 TTS 模型
tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST")

# 将文本转换为语音并保存为音频文件
tts.tts_to_file(
    text,
    file_path="output_1.wav"
)
