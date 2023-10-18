import os
import subprocess


def remove_subtitles_and_audio(input_folder, output_folder, sub_to_keep, audio_to_keep):
    # Ensure the output folder exists
    output_changed_folder = os.path.join(input_folder, output_folder)
    if not os.path.exists(output_changed_folder):
        os.makedirs(output_changed_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".avi", ".mkv", ".mp4")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_changed_folder, filename)

            sw_path = r"C:\Program Files\MKVToolNix\mkvmerge.exe"

            # Define the MKVToolNix command to remove subtitles and audio
            cmd = [
                sw_path,
                "-o", output_path,
                f"--audio-tracks", f"{audio_to_keep}",  # Keep audio track 0
                f"--subtitle-tracks", f"{sub_to_keep}",  # Keep the specified subtitle track
                input_path
            ]

            try:
                # Run the MKVToolNix command
                subprocess.run(cmd, check=True)
                print(
                    f"Removed all subtitles and audio (except audio track 0) except subtitle track {sub_to_keep} from "
                    f"{filename} and saved to {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    input_folder = r"path"  # Replace with the path to your input folder
    output_folder = "output_folder"  # Replace with the path to your output folder
    subtitle_track_to_keep = 2  # Specify the subtitle track to keep
    audio_to_keep = 2

    remove_subtitles_and_audio(input_folder, output_folder, subtitle_track_to_keep, audio_to_keep)
