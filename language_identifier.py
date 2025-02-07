import sys
import math


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    counts = {chr(i) : 0 for i in range (ord('A'), ord("Z")+1)}

    with open (filename,encoding='utf-8') as f:
        text = f.read()
        text = text.upper()

        for ch in text:
            if 'A' <= ch <= 'Z':
                counts[ch] += 1

    print("Q1")
    for letter in sorted(counts.keys()):
        print(f"{letter} {counts[letter]}")

    return counts

def compute_F(counts, parameter_vector, prior):

    F = math.log(prior)
    counter = 0  
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        F += counts[letter] * math.log(parameter_vector[counter])
        counter += 1  
    return F

def main():
    if len(sys.argv) != 4:
        print("input parameters error")
        sys.exit(1)

    letter_file = sys.argv[1]
    english_prior = float(sys.argv[2])
    spanish_prior = float(sys.argv[3])

    e_vector, s_vector = get_parameter_vectors()
    counts = shred(letter_file)

    X1 = counts['A']
    Q2_e = X1 * math.log(e_vector[0])
    Q2_s = X1 * math.log(s_vector[0])

    print("Q2")
    print(f"{Q2_e:.4f}")  
    print(f"{Q2_s:.4f}")

    F_e= compute_F(counts, e_vector, english_prior)
    F_s = compute_F(counts, s_vector, spanish_prior)
    
    print("Q3")
    print(f"{F_e:.4f}")
    print(f"{F_s:.4f}")

    diff = F_s - F_e

    if diff >= 100:
        p_e = 0.0
    elif diff <= -100:
        p_e = 1.0
    else:
        p_e = 1.0 / (1.0 + math.exp(diff))
    
    print("Q4")
    print(f"{p_e:.4f}")

if __name__ == "__main__":
    main()




