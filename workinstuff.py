import math

#bitdepth of 16 or 24
def numToBytes(num):
    result = []

    if bitdepth == 24:
        rng = 3
    elif bitdepth == 16:
        rng = 2
    else:
        print("Somethings wrong")
        return 0

    for i in range(rng):
        bitplace = 8*i
        bitmask = 255 << bitplace
        x = (num & bitmask) >> bitplace
        result.append(x)

    return result

def main():
    

if __name__ == "__main__":
    main()