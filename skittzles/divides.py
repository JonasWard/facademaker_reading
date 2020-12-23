def lazy_divide_check(integer):
    dividers = []
    for i in range(2, int(integer ** .5), 1):
        division = integer / i
        if float(int(division)) == division:
            dividers.append( i )

    return dividers

if __name__ == "__main__":
    print( lazy_divide_check(5310) )