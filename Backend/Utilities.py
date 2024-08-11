import pandas as pd;


df=pd.read_csv('D:\Thesis\Datasets\Step_datasets_14.csv');
#print(df);
dc={}
i=0
for x in df['REFERENCES']:
    if(len(list(x[1:x.find(']')].split(',')))>1):
        dc[i]=len(list(x[1:x.find(']')].split(',')))
    i+=1
     
#{k:v for (k,v) in dc.items() if v > 1}

for y,z in dc.items():
    print("Key::"+str(y)+"Value::"+str(z));
#    stp=data[:data.find('ENDSEC;')]

#l=df['REFERENCES']    
#dict((x,l.count(x)) for x in set(l))

#list_count = df['REFERENCES'].apply(lambda x: isinstance(x, list)).sum()

#print(f"Number of list values in 'column1': {list_count}")