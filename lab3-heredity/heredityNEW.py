import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having 0, 1, or 2 copies of the gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    # Probability of trait given gene count
    "trait": {
        2: {True: 0.65, False: 0.35},
        1: {True: 0.56, False: 0.44},
        0: {True: 0.01, False: 0.99}
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")

    # Load data from CSV
    people = load_data(sys.argv[1])

    # Initialize probability distributions for each person
    probabilities = {
        person: {
            "gene": {0: 0, 1: 0, 2: 0},
            "trait": {True: 0, False: 0}
        }
        for person in people
    }

    # Loop over all possible sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Skip sets that contradict known data
        fails_evidence = any(
            people[person]["trait"] is not None
            and people[person]["trait"] != (person in have_trait)
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all possible gene distributions
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Compute joint probability for this configuration
                p = joint_probability(people, one_gene, two_genes, have_trait)

                # Add it into the running totals
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Normalize all probability distributions
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a CSV file into a dictionary.
    Each person has: name, mother, father, and known trait (True/False/None).
    """
    data = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True if row["trait"] == "1"
                    else False if row["trait"] == "0"
                    else None
                )
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    Used to enumerate all possible gene/trait assignments.
    """
    s = list(s)
    return [
        set(combo)
        for r in range(len(s) + 1)
        for combo in itertools.combinations(s, r)
    ]


# ------------------------------------------------------------
#  JOINT PROBABILITY
# ------------------------------------------------------------

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute the joint probability of:
    - this exact assignment of gene counts
    - this exact assignment of trait presence
    """

    prob = 1.0

    # Helper: probability a parent passes the gene
    def pass_prob(parent):
        if parent in two_genes:
            return 1 - PROBS["mutation"]
        elif parent in one_gene:
            return 0.5
        else:
            return PROBS["mutation"]

    for person in people:

        # Determine gene count
        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0

        # Trait probability for this person
        has_trait = person in have_trait
        trait_prob = PROBS["trait"][genes][has_trait]

        mom = people[person]["mother"]
        dad = people[person]["father"]

        # Case 1: No parents → unconditional probability
        if mom is None and dad is None:
            gene_prob = PROBS["gene"][genes]

        # Case 2: Parents → compute from inheritance rules
        else:
            mom_pass = pass_prob(mom)
            dad_pass = pass_prob(dad)

            if genes == 2:
                gene_prob = mom_pass * dad_pass
            elif genes == 1:
                gene_prob = mom_pass * (1 - dad_pass) + (1 - mom_pass) * dad_pass
            else:  # genes == 0
                gene_prob = (1 - mom_pass) * (1 - dad_pass)

        # Multiply into running joint probability
        prob *= gene_prob * trait_prob

    return prob


# ------------------------------------------------------------
#  UPDATE
# ------------------------------------------------------------

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add joint probability p into the running totals for each person.
    """

    for person in probabilities:

        # Gene count bucket
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0

        probabilities[person]["gene"][gene_count] += p

        # Trait bucket
        has_trait = person in have_trait
        probabilities[person]["trait"][has_trait] += p


# ------------------------------------------------------------
#  NORMALIZE
# ------------------------------------------------------------

def normalize(probabilities):
    """
    Normalize each probability distribution so values sum to 1.
    """

    for person in probabilities:

        # Normalize gene distribution
        gene_total = sum(probabilities[person]["gene"].values())
        for g in probabilities[person]["gene"]:
            probabilities[person]["gene"][g] /= gene_total

        # Normalize trait distribution
        trait_total = sum(probabilities[person]["trait"].values())
        for t in probabilities[person]["trait"]:
            probabilities[person]["trait"][t] /= trait_total


if __name__ == "__main__":
    main()
