from TTS.api import TTS

# 创建TTS实例（自动下载模型）
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

text="""
In the small village of Valoria, nestled within the depths of the forest, reside various creatures from goblins to elves, magicians and knights. 
Despite its quirky inhabitants, there is an underlying fear due to the hidden dangers lurking within the woods. In this village lives a knight named Thor. He is a retired guard for the city, having fought in many wars on behalf of the kingdom. His house sits amidst a lush garden, green grass and forest, always prepared to face any monster that may cross his path. 
But he hadn't anticipated encountering an assertive character at his doorstep.
"""

# 生成语音并保存
tts.tts_to_file(
    text,
    file_path="output.wav"
)

print("Audio saved to output.wav")

