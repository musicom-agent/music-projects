def generate_euclidean_rhythm(steps, pulses):
    # Bjorklund algorithm to distribute pulses evenly across steps
    if pulses > steps:
        raise ValueError("Pulses cannot exceed steps")
        
    pattern = []
    counts = []
    remainders = []
    divisor = steps - pulses
    remainders.append(pulses)
    level = 0
    
    while True:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level += 1
        if remainders[level] <= 1:
            break
            
    counts.append(divisor)
    
    def build_pattern(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)
        else:
            for i in range(counts[level]):
                build_pattern(level - 1)
            if remainders[level] > 0:
                build_pattern(level - 2)
                
    build_pattern(level)
    pattern.reverse()
    
    # Rotate pattern to start with a pulse if possible
    first_one = pattern.index(1)
    pattern = pattern[first_one:] + pattern[:first_one]
    return pattern

if __name__ == "__main__":
    # Generate a classic 8-step Euclidean rhythm with 3 pulses (tresillo)
    rhythm_3_8 = generate_euclidean_rhythm(8, 3)
    print("Euclidean(8, 3) Tresillo:", rhythm_3_8)
    
    # Generate a classic 16-step Euclidean rhythm with 5 pulses (cinquillo variant or classic rhythm)
    rhythm_5_16 = generate_euclidean_rhythm(16, 5)
    print("Euclidean(16, 5):", rhythm_5_16)
