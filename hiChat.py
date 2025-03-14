

import torch
import torchaudio
from chattts import ChatTTS

# 初始化 ChatTTS 模型
chat = ChatTTS.Chat()

# 加载模型（建议在首次运行时设置 compile=True 以提高性能）
chat.load(compile=False)

# 定义要合成的文本
texts = ["你好，这是一个 ChatTTS 语音合成测试。", "你可以通过这个模型生成自然流畅的语音。"]

# 生成语音
wavs = chat.infer(texts)

# 保存生成的音频文件
for i, wav in enumerate(wavs):
    try:
        torchaudio.save(f"output_{i}.wav", torch.from_numpy(wav).unsqueeze(0), 24000)
    except:
        torchaudio.save(f"output_{i}.wav", torch.from_numpy(wav), 24000)
    print(f"音频已保存到 output_{i}.wav")
