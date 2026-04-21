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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # create a new directory based on corpus
    prob_d = {page_name: 0 for page_name in corpus}

    # links + number of links
    links = corpus[page]
    no_links = len(links)

    # We need to identify the number of pages in the corpus
    No_pages = len(corpus)

    # IF there are no links - what happens
    if no_links == 0:
        for page_name in prob_d:
            prob_d[page_name] = (damping_factor) / No_pages
        return prob_d

    # Probability of picking a random page
    condition1 = (1 - damping_factor) / (No_pages)

    # Poribability of picking a linked page
    condition2 = (damping_factor) / (no_links)

    # Retunr probabilities of each one
    # We first add the probability of conition1 (probability of picking a random page)
    for page_name in prob_d:
        prob_d[page_name] += condition1

        # Then we add condition 2 - probability of picking a linked page from said page
        if page_name in links:
            prob_d[page_name] += condition2

    return prob_d


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initial sample
    corpus_list = list(corpus)
    random_page = random.choice(corpus_list)

    # distribution to track how many times each page is sampled
    samples = {page_name: 0 for page_name in corpus}
    # add initial sample visited
    samples[random_page] += 1

    for num in range(0, n - 1):

        # next probability after initial
        T_model = transition_model(corpus, random_page, damping_factor)

        # use random value to hep pick next page based on transition model:
        random_v = random.random()
        total_prob = 0

        for page_name, prob in T_model.items():
            total_prob += prob
            # if random prob is less than page prob then pick it
            if random_v <= total_prob:
                random_page = page_name
                break

        samples[random_page] += 1

    # Normalisation
    page_rank = {page_name: (sample_no / n) for page_name, sample_no in samples.items()}

    print("Sum of sample page ranks: ", round(sum(page_rank.values()), 4))

    return page_rank

    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initial Rank
    N = len(corpus)
    initial_rank = 1 / N
    no_links = (1 - damping_factor) / N

    # initialise a python dictonary based on the corpus:
    current_rank = {page_name: initial_rank for page_name in corpus}
    # initialise a python dictonary based on the corpus for the new rank
    new_rank = {page_name: 0 for page_name in corpus}
    # use a while function e.g. while  modulus of (state 2 - state1) > 0.001
    # This function needs to review the direcotry and see if there is any change more than 0.001 in any of the pages

    rank_dif = initial_rank
    while rank_dif >= 0.001:
        # itterations += 1
        rank_dif = 0

        for page in corpus:
            surf_prob = 0
            for Pagei in corpus:
                # If Pagei has no links it picks randomly any corpus page:
                if len(corpus[Pagei]) == 0:
                    surf_prob += current_rank[Pagei] * initial_rank

                # Elif Pagei has a link to the initial page, it randomly picks a linked page on pag2:
                elif page in corpus[Pagei]:
                    surf_prob += current_rank[Pagei] / len(corpus[Pagei])
                    # Calculate new page rank
                rank = no_links + (damping_factor * surf_prob)
                new_rank[page] = rank

        # normalisation
        # sum all values
        normal = sum(new_rank.values())
        # divide by each rank by sum of all values for every page in new rank
        new_rank = {page: (rank / normal) for page, rank in new_rank.items()}

        # Update the rank_dif for the While statment
        for page in corpus:
            # use abs() to ensure value is positive
            rank_change = abs(current_rank[page] - new_rank[page])
            if rank_change > rank_dif:
                rank_dif = rank_change

        # update current rank to be the new rank
        current_rank = new_rank.copy()

    return new_rank

    raise NotImplementedError


if __name__ == "__main__":
    main()
