if __name__ == '__main__':

    t1 = ('1', '2')
    t2 = ('1', '2') 
    t3 = ('1', '3')

    print(hex(id(t1)), hex(id(t2)), hex(id(t3)))
    
    dic = {'0' : t1, '1' : t3}
        
    print(dic)
    if t1 == t2:
        print('yes')


    dic['0'].remove(t2)
    print(dic)
