#check anagaram
def checkanagram(string1, string2):
    # Get lengths of both strings
    n1 = len(string1)
    n2 = len(string2)

    # If lenght of both strings is not same, then
    # they cannot be anagram
    if n1 != n2:
        return 0

    # Sort both strings
    string1 = sorted(string1)
    string2 = sorted(string2)

    # Compare sorted strings
    for value in range(0, n1):
        if string1[value] != string2[value]:
            return 0

    return 1



string1 = "anagram"
string2 = "nagaram"


if checkanagram(string1, string2):
    print("The two strings are anagram of each other")
else:
    print("The two strings are not anagram of each other")