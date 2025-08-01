import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # transition_model (corpus, "1.html", DAMPING)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    count = len(links)
    length = len(corpus)
    dict = {}

    for pages in corpus:
        dict[pages] = 0

    for link in links:
        dict[link] += damping_factor / count

    for link in corpus:
        dict[link] += (1 - damping_factor) / length

    # print(dict)
    return dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict = {}
    pages = []

    for page in corpus:
        pages.append(page)
    page = random.choice(pages)
    dict[page] = 1

    for i in range(n - 1):
        links_prob = transition_model(corpus, page, damping_factor)
        keys = list(links_prob.keys())
        values = list(links_prob.values())
        page = random.choices(keys, weights=values)[0]
        if page in dict:
            dict[page] += 1
        else:
            dict[page] = 1

    for link in dict:
        dict[link] = dict[link] / n

    return dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict = {}
    length = len(corpus)
    links = {}
    all = []
    for page in corpus:
        links[page] = []
        all.append(page)

    for page in corpus:
        if corpus[page] == set():
            corpus[page] = all

    for page in corpus:
        for pages, out_link in corpus.items():
            if page in out_link:
                links[page].append(pages)

    for pages in corpus:
        dict[pages] = 1 / length

    change = True
    while change == True:
        change = False
        new_pagerank = {}

        for page in corpus:
            sum = 0
            for link in links[page]:
                count = len(corpus[link])
                sum += dict[link] / count
            prev = dict[page]
            new = (1 - damping_factor) / length + (damping_factor * (sum))
            new_pagerank[page] = new

        for page in corpus:
            if abs(dict[page] - new_pagerank[page]) > 0.001:
                change = True
            dict[page] = new_pagerank[page]

    return dict


if __name__ == "__main__":
    main()
