"""
This script generates a regex expression for use with long text answers in Google Forms, based on a list of user-defined
keywords. Sublist enable the use of alternative keywords.

Output
======
The regex expression is stored in a .txt file in the same directory as this script. The regex expression is additionally
printed to the console output.

Example
=======
In the USER DEFINITIONS section, the following example can be defined to generate a regex definition that enables
correct answers like
"River modifications like diversion dams but also agriculture and urbanization can alter the discharge of a river."

keywords = [
    "modif",
    "urban",
    ["dam", "diver.*", "stor.*"],
    ["agriculture", "land"]
]
"""
import itertools


# USER SECTION (modifying the code beyond this section will alter the behavior of the algorithm.------------------------
keywords = [
    "modif",
    "urban",
    ["dam", "diver.*", "stor.*"],
    ["agriculture", "land"]
]
# ------------------------ ------------------------ ------------------------ ------------------------ ------------------


def generate_keywords_regex(keywords):
    """
    Given a list of keywords (strings or sublists), return a regex pattern that matches any permutation of those
    keywords in any order. If an element is a list, it is turned into an (alt1|alt2|...) group.

    Args:
        keywords (list): List of user-defined keywords (see USER SECTION).

    Note:
      - This function may generate large expressions if you have many keywords, due to the factorial (n!) permutations.
      - The final pattern by default has '.*' around each keyword to allow arbitrary text between them.
      - Parentheses group each permutation, which are then joined with | so that any one permutation can match.
    """

    # A small helper to turn a single keyword or a list of keywords into the piece of pattern ".*(x|y|z).*"
    def to_pattern(item):
        if isinstance(item, list):
            # Join all possibilities in a single group; to specifically adjust for partial matches (like 'diver.*'),
            # adjust here; currently, the output is verbatim
            return f".*({'|'.join(item)}).*"
        else:
            # Single string
            return f".*{item}.*"

    # Build a set to avoid duplicating identical permutations when the list has repeated entries
    visited = set()
    permutation_patterns = []

    for permutation in itertools.permutations(keywords):
        # Convert each item in the permutation to the appropriate sub-pattern
        parts = [to_pattern(x) for x in permutation]
        # Join all parts - they already have leading and trailing '.*'
        full_permutation_pattern = "".join(parts)

        # Enclose each permutation pattern in parentheses
        if full_permutation_pattern not in visited:
            visited.add(full_permutation_pattern)
            permutation_patterns.append(f"({full_permutation_pattern})")

    # Join all permutation-based patterns with an OR
    final_pattern = "|".join(permutation_patterns)
    return final_pattern


def save_pattern_to_file(pattern2save, file_name):
    """
    Saves a given (regex) pattern to a text file efficiently.
    Args:
        pattern2save (str): The regex pattern to save.
        file_name (str): The name of the file to save the pattern in.
    """
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(pattern2save)
        print(f"Pattern saved successfully to {file_name}.")
    except Exception as e:
        print(f"An error occurred while saving the pattern: {e}")


if __name__ == "__main__":
    pattern = generate_keywords_regex(keywords)
    print("Regex expression:\n" + str(pattern))
    save_pattern_to_file(pattern, "gForms-regex-pattern.txt")
