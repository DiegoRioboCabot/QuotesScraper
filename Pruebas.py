def list_difference(list1, list2):

    list3 = list2.copy()
    return [item for item in list2 if item not in list1]



lista_1 = [1,2,3,4,5,6,7,8,9,0]
lista_2 = ["a","b",1,2,4,5,"c","d",9,0]

lista_3 = list_difference(lista_1,lista_2)
print(lista_3)