def folder(l):
    n=len(l);
    d=[];
    flag=True;
    while flag==True:
        first=l.pop(0);
        last=l.pop(n-2);
        d.append(first+last);
        n=len(l);
        if(n==1):
            d.append(l.pop(0));
            flag=False;
        elif (n==0):
            flag=False;
    return(d);
    
    
if __name__=="__main__":
    l=[1,2,3,4,5,6];
    print(folder(l));
    
    
