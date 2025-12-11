import ffmpeg
import os

def extract_audio(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .output(output_path, acodec="mp3", audio_bitrate="320k")
        .overwrite_output()
        .run()
    )

def normalize_audio(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .filter('loudnorm')
        .output(output_path)
        .overwrite_output()
        .run()
    )
