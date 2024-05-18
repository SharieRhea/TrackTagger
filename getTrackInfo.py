import sys
import json

def main():
    if len(sys.argv) < 2:
        sys.stderr.write(f"Invalid number of arguments: {len(sys.argv)}\n")
        exit(1)

    filename = sys.argv[1]
    if not filename.endswith(".json"):
        sys.stderr.write("Must provide a json file.\n")
        exit(2)

    with open(filename) as file:
        # deserialize into dict
        data = json.load(file)
        
        # attempt to access track info, failure indicates no valid result for given title and artist
        try:
            title = data["track"]["name"]
        except KeyError:
            sys.stderr.write("Track not found.\n")
            exit(3)

        artist = data["track"]["artist"]["name"]
        playcount = data["track"]["playcount"]
        # normalize tags to be in all lowercase to reduce duplicates
        tags = []
        for tag in data["track"]["toptags"]["tag"]:
            tags.append(tag["name"].lower())

        # print track info to stdout to be captured by bash script
        print(title)
        print(artist)
        print(playcount)
        print(tags)

        # attempt to access album info, for some reason not every track has an album associated with it
        try:
            albumTitle = data["track"]["album"]["title"]
            albumArtist = data["track"]["album"]["artist"]
            # -1 grabs the last image in the list, which is guaranteed to be the largest file size
            albumCover = data["track"]["album"]["image"][-1]["#text"]

            # print album info to stdout to be captured by bash script
            print(albumTitle)
            print(albumArtist)
            print(albumCover)
        except KeyError:
            sys.stderr.write("Album not found.\n")
    
if __name__ == "__main__":
    main()
