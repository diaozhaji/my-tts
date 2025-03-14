import torch
from TTS.tts.models import FastSpeech2
from TTS.utils.audio import AudioProcessor
from scipy.io import wavfile

# 初始化配置
device = "cuda" if torch.cuda.is_available() else "cpu"
text = "欢迎使用轻量级中文语音合成系统。"

# 加载预训练模型（自动下载权重）
model = FastSpeech2.from_pretrained(
    "fastspeech2-zh-CN-2025",  # 官方最新中文模型
    device_map=device,
    enable_fp16=True  # 启用半精度加速
)

# 生成语音波形
output = model.generate(
    text=text,
    speed=1.2,          # 语速调节 (0.5~2.0)
    energy_scale=0.8,   # 情感强度 (0.1~1.5)
    pitch_scale=1.1     # 音高变化 (0.1~1.5)
)

# 保存为 WAV 文件
wavfile.write(
    "output.wav",
    rate=model.config.audio.sample_rate,
    data=output["audio"].cpu().numpy()
)

print(f"语音已生成至 output.wav，时长 {output['duration']:.2f} 秒")
