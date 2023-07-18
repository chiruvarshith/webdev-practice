def numof_trips(lug_weight,capacity):
    total_weight=sum(lug_weight)
    trips=total_weight // capacity

    if  total_weight%capacity !=0:
        trips+=1
    return trips


s=[1,2,3,4,5,6,7]
f=int(input("enter the capacity of the carrier"))
t=numof_trips(s,f)
print(t,"is the number of trips u have to go for the all the luggages")