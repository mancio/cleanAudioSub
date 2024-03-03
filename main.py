import os
import subprocess
import sys
import json

# Global path to mkvmerge
sw_path = r"C:\Program Files\MKVToolNix\mkvmerge.exe"


def identify_and_parse_tracks(file_path):
    cmd = [sw_path, "--identify", "--identification-format", "json", file_path]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        track_info = json.loads(result.stdout)

        print(f"Track information for {file_path}:")
        for track in track_info.get('tracks', []):
            if track['type'] in ['audio', 'subtitles']:
                track_id = track.get('id', 'N/A')
                track_lang = track['properties'].get('language_ietf', track['properties'].get('language',
                                                                                              'und'))  # Use language_ietf if available
                track_type = track['type']
                print(f"  - Track ID: {track_id}, Type: {track_type}, Language: {track_lang}")
    except subprocess.CalledProcessError as e:
        print(f"Error while identifying tracks: {e}")


def remove_subtitles_and_audio(input_path, output_path, sub_to_keep, audio_to_keep):
    cmd = [
        sw_path,
        "-o", output_path,
        f"--audio-tracks", f"{audio_to_keep}",
        f"--subtitle-tracks", f"{sub_to_keep}",
        input_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(
            f"Processed {os.path.basename(input_path)}: kept audio track {audio_to_keep} and subtitle track {sub_to_keep}, saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {os.path.basename(input_path)}: {e}")


def process_files(input_folder, output_folder, sub_to_keep, audio_to_keep):
    output_changed_folder = os.path.join(input_folder, output_folder)
    if not os.path.exists(output_changed_folder):
        os.makedirs(output_changed_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".avi", ".mkv", ".mp4")):
            input_path = os.path.join(str(input_folder), str(filename))
            output_path = os.path.join(str(output_changed_folder), str(filename))

            # Identify and parse tracks
            identify_and_parse_tracks(input_path)

            # Remove unwanted tracks
            remove_subtitles_and_audio(input_path, output_path, sub_to_keep, audio_to_keep)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <input_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = "output_folder"  # Define your output folder name here
    audio_track_to_keep = 3  # Define the audio track to keep
    subtitle_track_to_keep = 7  # Define the subtitle track to keep

    process_files(input_folder, output_folder, subtitle_track_to_keep, audio_track_to_keep)
