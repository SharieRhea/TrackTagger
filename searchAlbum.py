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
        albums = data["results"]["albummatches"]

        if len(albums) is 0:
            sys.stderr.write("Album not found.")
            exit (3)

        # collect the first 5 results
        results = []
        for i in range(5):
            albumInfo = []
            albumInfo.append(albums["album"][i]["name"])
            albumInfo.append(albums["album"][i]["artist"])
            # -1 grabs the last image in the list, which is guaranteed to be the largest file size
            albumInfo.append(albums["album"][i]["image"][-1]["#text"])
            results.append(albumInfo)

        # print album info to stdout to be caputured by bash script
        for album in results:
            print(album)

if __name__ == "__main__":
    main()
