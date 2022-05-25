import urllib.request as req
import argparse
import re


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    p.add_argument('url', type=str)

    return p.parse_args()


def load_website(url: str) -> str:
    s = req.urlopen(url)

    return s.read().decode('utf8')


def main():
    args = parse_args()

    website = load_website(args.url)

    links: list[str] = []

    for i in re.findall(r'href="http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"', website):
        links.append(i.split('"')[1])
        print(i)

    hosts = {i.split('/')[2] for i in links}

    for i in hosts:
        c = 0
        for j in links:
            if i in j:
                c += 1
        print(f"{i}: {c}")

    for i in set(re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", website)):
        print(i)

    print(len(re.findall(r'src="http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"', website)))


if __name__ == '__main__':
    main()
