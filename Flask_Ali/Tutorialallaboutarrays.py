def ArrayInfo():
    numarray=[4,2,10,5,22,0]
    stringarray=["To", "Welcome", "My class!"]

    #Length an array
    numarraylen=len(numarray)
    print("the length of the array, numarray is: ", numarraylen)
    print("----------")

    #sorting an array
    stringarray.sort()
    print("the array, stringarray, in order is", stringarray)
    print("----------")

    #indexing an array-specific index
    print(stringarray[0])
    print(numarray[1])
    print(stringarray[2])
    print(numarray[3])
    print("----------")

    #Looping through an array
    for i in range(0,numarraylen):
        print(numarray[i]) 
    print("----------")

    #Adding new items to an array
    newword = "Hello"
    stringarray.append(newword)
    print(stringarray)
    print("----------")

    #Inserting a new item into an array
    newword="Hello!"
    stringarray.insert(0,newword)
    print(stringarray)
    print("----------")

    #Removing an item from an array
    stringarray.remove("Hello")
    print(stringarray)
    print("----------")

    #Removing an item from a specific index
    #Use only if you know the index
    numarray.pop(2)
    print(numarray)

def main():
    ArrayInfo()

if __name__ == "__main__":
    main()
