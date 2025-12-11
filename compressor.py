import ffmpeg

def compress_video(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .output(
            output_path,
            vcodec='libx264',
            crf=23,        # lower = better quality
            preset='medium'
        )
        .overwrite_output()
        .run()
    )
