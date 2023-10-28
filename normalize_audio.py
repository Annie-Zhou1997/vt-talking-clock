import subprocess
import os

def normalize_audio(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".wav", ".WAV")):
            input_filepath = os.path.join(input_folder, filename)
            output_filepath = os.path.join(output_folder, filename)

            # 第一步：分析音频并获取峰值音量 max_volume
            command = ["ffmpeg", "-i", input_filepath, "-af", "volumedetect", "-vn", "-sn", "-dn", "-f", "null", "/dev/null"]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
            output = result.stderr
            max_volume_line = [line for line in output.split("\n") if "max_volume" in line]
            if not max_volume_line:
                print(f"未能分析 {filename} 的音量。")
                continue
            max_volume = max_volume_line[0].split(" ")[-2]
            
            # 第二步：根据分析结果调整音量 ajusted_volume
            command = ["ffmpeg", "-i", input_filepath, "-af", f"volume={max_volume}dB", output_filepath]
            subprocess.run(command)

            print(f"{filename} 已被标准化。结果保存在 {output_filepath}")

if __name__ == "__main__":
    input_folder = "/Users/zhou/Desktop/vt-talking-clock/English"
    output_folder = "/Users/zhou/Desktop/vt-talking-clock/English_1"
    normalize_audio(input_folder, output_folder)
