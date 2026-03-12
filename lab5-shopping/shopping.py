import csv
from fileinput import filename
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file and convert it into numerical
    evidence and labels suitable for a k-nearest-neighbor classifier.
    """
    evidence = []
    labels = []

    # Map month abbreviations to numeric indices (Jan = 0, ..., Dec = 11)
    MONTH_MAP = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11,
    }

    # Read rows from CSV and convert each field to the appropriate type
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)  # skip header row

        for row in reader:
            # Build evidence row in the exact order required by the spec
            evidence_row = [
                int(row[0]),  # Administrative
                float(row[1]),  # Administrative_Duration
                int(row[2]),  # Informational
                float(row[3]),  # Informational_Duration
                int(row[4]),  # ProductRelated
                float(row[5]),  # ProductRelated_Duration
                float(row[6]),  # BounceRates
                float(row[7]),  # ExitRates
                float(row[8]),  # PageValues
                float(row[9]),  # SpecialDay
                MONTH_MAP[row[10]],  # Month
                int(row[11]),  # OperatingSystems
                int(row[12]),  # Browser
                int(row[13]),  # Region
                int(row[14]),  # TrafficType
                1 if row[15] == "Returning_Visitor" else 0,  # VisitorType
                1 if row[16] == "TRUE" else 0,  # Weekend
            ]

            evidence.append(evidence_row)

            # Encode Revenue as binary label (1 = TRUE, 0 = FALSE)
            labels.append(1 if row[17] == "TRUE" else 0)

    return evidence, labels


def train_model(evidence, labels):
    """
    Train a k-nearest-neighbor classifier (k=1) on the provided evidence
    and labels, and return the fitted model.
    """

    # Initialize a 1-nearest-neighbor classifier
    model = KNeighborsClassifier(n_neighbors=1)

    # Fit model on training data
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Compute sensitivity (true positive rate) and specificity (true negative rate)
    based on actual labels and model predictions.
    """

    # Counters for positive and negative cases
    true_positives = 0
    true_negatives = 0
    total_positives = 0
    total_negatives = 0

    # Compare each actual label to its prediction
    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            total_positives += 1
            if predicted == 1:
                true_positives += 1
        else:
            total_negatives += 1
            if predicted == 0:
                true_negatives += 1

    # Compute rates as proportions
    sensitivity = true_positives / total_positives
    specificity = true_negatives / total_negatives

    return sensitivity, specificity


if __name__ == "__main__":
    main()
