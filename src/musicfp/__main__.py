import argparse, os, sys, vlc, random
from pathlib import Path
from threading import Thread

parser = argparse.ArgumentParser(prog="musicfp", description="A terminal based media player for programmers")
parser.add_argument(
    "path", metavar="path", type=str, help="path to directory containing file(s)"
)
parser.add_argument(
    "-s", "--shuffle", action="store_true", help="enable shuffling of songs"
)

in_player_help_single = """
skip        skips playing song
pause       pauses/resumes playing song
vol[vol]    sets the volume to [vol]%   eg. vol75 -sets volume to 75%
quit        quits the program

help        displays usage of all commands
"""

in_player_help_multiple = """
pause       pauses/resumes playing song
next        plays next song
previous    plays previous song
vol[vol]    sets the volume to [vol]%   eg. vol75 -sets volume to 75%
quit        quits the program

help        displays usage of all commands
"""


class MultiplePlayer:
    def __init__(self, path, shuffle):
        self.player = vlc.MediaListPlayer()
        self.list = vlc.MediaList()
        self.player.get_media_player().audio_set_volume(100)
        self.path = path
        self.shuffle = shuffle

    def asyncInput(self):
        print(
            "Playing all songs from directory:",
            self.path,
            "with shuffle",
            ("OFF", "ON")[self.shuffle],
        )
        while True:
            command = input(">>  ")
            if command == "quit":
                self.player.stop()
                break
            elif command.startswith("vol"):
                volume = command.strip("vol")
                self.player.get_media_player().audio_set_volume(int(volume))
                print("Volume set to ", volume, "%")
            elif command == "next":
                self.player.next()
            elif command == "previous":
                self.player.previous()
            elif command == "pause":
                self.player.pause()
                print("Paused")
            elif command == "help":
                print(in_player_help_multiple)
            else:
                print("Invalid Command\nType help to view all available commands")

    def startProcessing(self):
        formats = [".m4a", ".flac", ".mp3", ".mp4", ".wav", ".wma", ".aac", ".mkv"]
        files = []
        for file in os.listdir(self.path):
            for format in formats:
                if file.endswith(format):
                    files.append(self.path / file)
                    break
        for i in range(files.__len__()):
            if self.shuffle:
                fileMRL = files[random.randint(0, len(files) - 1)]
                self.list.add_media(fileMRL)
                files.remove(fileMRL)
            else:
                fileMRL = files[i]
                self.list.add_media(fileMRL)
        self.player.set_media_list(self.list)
        self.player.play()


def play_multiple(dirPath, shuffle):
    item = MultiplePlayer(dirPath, shuffle)
    thread_a = Thread(target=item.startProcessing)
    thread_a.start()
    thread_b = Thread(target=item.asyncInput)
    thread_b.start()
    thread_a.join()
    thread_b.join()


class SinglePlayer:
    def __init__(self, file):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.audio_set_volume(100)
        self.media = vlc.Media(file)

    def asyncInput(self):
        self.media.parse()
        print("Playing", self.media.get_meta(0), 'from "', self.media.get_meta(4), '"')
        while True:
            command = input(">>  ")
            if command == "skip":
                self.player.stop()
                print("Skipped")
            elif command == "quit":
                self.player.stop()
                break
            elif command.startswith("vol"):
                volume = command.strip("vol")
                self.player.audio_set_volume(int(volume))
                print("Volume set to ", volume, "%")
            elif command == "pause":
                self.player.pause()
                print("Paused")
            elif command == "resume":
                self.player.pause()
                print("Resumed")
            elif command == "repeat":
                self.player.stop()
                print("Repeated")
                self.player.play()
            elif command == "help":
                print(in_player_help_single)
            else:
                print("Invalid Command\nType help to view all available commands")

    def startProcessing(self):
        self.player.set_media(self.media)
        self.player.play()


def play_single(filePath):
    item = SinglePlayer(filePath)
    thread_a = Thread(target=item.startProcessing)
    thread_a.start()
    thread_b = Thread(target=item.asyncInput)
    thread_b.start()
    thread_a.join()
    thread_b.join()


if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
elif len(sys.argv) >= 2:
    args = parser.parse_args()

    if os.path.isdir(args.path):
        path = args.path
    elif os.path.isfile(args.path):
        path = args.path
    else:
        if args.path == "current":
            path = os.getcwd()
        else:
            print("Directory does not exist")
            sys.exit()

    do_shuffle = args.shuffle
else:
    parser.print_help()

def main():
    formats = [".m4a", ".flac", ".mp3", ".mp4", ".wav", ".wma", ".aac", ".mkv"]
    if str(Path(path).suffix) in formats:
        play_single(Path(path))
    else:
        play_multiple(Path(path), do_shuffle)

if __name__ == "__main__":
    main()