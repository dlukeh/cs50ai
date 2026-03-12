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
    with probability 'damping_factor', choose a link at random 
    linked to by a 'page'. With probability '1 - damping_factor', choose 
    a link at random chosen from all pages in the corpus. 
    """
    
    distribution = {}
    # total number of pages
    N = len(corpus)
    
    # outgoing links from the current page (safe lookup)
    links = corpus.get(page, set())
    
    if links:
        L = len(links)
        
        # base probability for all pages
        for p in corpus:
            distribution[p] = (1 - damping_factor) / N
        
        # add link-follow probability
        for p in links:
            distribution[p] += damping_factor / L
    
    else:
        # no outgoing links uniform distribution
        for p in corpus:
            distribution[p] = 1 / N
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling n pages
    according to the transition model.
    """
    visits = {page: 0 for page in corpus}

    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        visits[page] += 1

        model = transition_model(corpus, page, damping_factor)
        page = random.choices(
            population=list(model.keys()),
            weights=list(model.values()),
            k=1
        )[0]

    return {page: visits[page] / n for page in corpus}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pr = {page: 1 / N for page in corpus}
    margin = 0.001

    while True:
        new_pr = {page: (1 - damping_factor) / N for page in corpus}

        for page in corpus:
            if corpus[page]:
                for linked in corpus[page]:
                    new_pr[linked] += damping_factor * (pr[page] / len(corpus[page]))
            else:
                # Dead end distribute evenly
                for p in corpus:
                    new_pr[p] += damping_factor * (pr[page] / N)

        # Check convergence
        if max(abs(new_pr[p] - pr[p]) for p in pr) < margin:
            return new_pr

        pr = new_pr


if __name__ == "__main__":
    main()
