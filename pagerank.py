import os
import random
import re
import sys

import copy

DAMPING = 0.85
SAMPLES = 10000
#SAMPLES = 2


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ## My lines starts

    print('corpus:')
    print(corpus)
    # page = list(corpus.keys())[0]
    # print('page', page)
    
    # prob = transition_model(corpus, page, DAMPING)

    ## My lines stops

    # ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    
    # print(f"PageRank Results from Sampling (n = {SAMPLES})")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
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
    links = list(corpus[page])
    #print(f'Page: {page}, links: {links}')

    probs = dict.fromkeys(corpus.keys(), 0)
    #print(probs)
    # Is there any links from page
    if len(links) == 0:
        p = 1 / len(corpus.keys())
        #print('Page with no outgoing links')
        #print('p', p)
        for key in probs.keys():
            probs[key] = p
    else:
        # With probability DAMPING, randomly choose on of the links from page
        p1 = DAMPING / len(links)
        for link in links:
            probs[link] += p1
        # With probability 1 - DAMPING, randomly choose among all pages
        p2 = (1 - DAMPING) / len(corpus.keys())
        for key in probs:
            probs[key] += p2

    #print('probs', probs)
    #print('probs sum', sum(probs.values()))
    return probs



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = dict.fromkeys(corpus.keys(), 0)

    page = random.choices(list(corpus.keys()))[0]
    #print('first page:', page)
    counts[page] += 1

    i = 1
    while i < n:
        probs = transition_model(corpus, page, damping_factor)
        #print('probs', probs)
        page = random.choices(list(probs.keys()), list(probs.values()))[0]
        #print('next page', page)
        counts[page] += 1

        i += 1

    #print(counts)

    for key in counts:
        counts[key] /= n
    #print(counts)
    #print('counts sum', sum(counts.values()))
    return counts


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Check if there is some page with no links
    for p in corpus:
        if len(corpus[p]) == 0:
            #print(p, 'no links!')
            #print(corpus[p])
            corpus[p] = list(corpus.keys())
            #print(corpus[p])

    N = len(corpus)
    pr = dict.fromkeys(list(corpus.keys()), 1/N)
    print('pr', pr)
    k = 0
    print('****** start loop')
    while True:
        pr_new = dict.fromkeys(list(corpus.keys()), 0)
        #print('pr_new', pr_new)
        # find pages i that links to p
        in_links_to_p = dict()
        for p, links in corpus.items():
            #print(f'p: {p}, links: {links}')
            
            for l in links:
                #print('l', l)
                if l not in in_links_to_p:
                    in_links_to_p[l] = {p}
                else:
                    in_links_to_p[l].add(p)
        #print('in_links_to_p', in_links_to_p)
        for p in pr_new:
            pr_new[p] += (1 - damping_factor) / N
            for i in in_links_to_p[p]:
                #print(f'{i} are linked to {p}')
                num_links_i = len(corpus[i])
                #print('num_links_i', num_links_i)
                pr_new[p] += (damping_factor * pr[i]) / num_links_i

            #print('- - - - - ')

        #print('pr_new', pr_new)
        if stop(pr, pr_new):
            break
        pr = copy.deepcopy(pr_new)
        k += 1
        if k == 100:
            break
    print('****** after loop')
    print('Iterations k:', k)
    #print('pr', pr)
    print('pr_new', pr_new)
    print('pr_new sum', sum(pr_new.values()))
    return pr_new

def stop(pr, pr_new):
    # Returns True if PageRank value changes no more than 0.001
    # between the pr and pr_new rank values
    for key in pr:
        if abs(pr[key] - pr_new[key]) > 0.001:
            return False
    return True

if __name__ == "__main__":
    main()
