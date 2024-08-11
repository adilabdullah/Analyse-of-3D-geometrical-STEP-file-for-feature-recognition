import csv
import pandas as pd
import xlsxwriter
import json;
from numpyencoder import NumpyEncoder

import matplotlib.pyplot as plt
import seaborn as sns

import smtplib
import ssl
from email.message import EmailMessage
import mysql.connector

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.STEPControl import STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopoDS import topods_Vertex,topods_Face
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder


class Thesis:
    elemList=[];
    refDicts={};
    paramDicts={};
    count=0;

    refParamList=[];
    refParamDict={};
    myList=[];
    finalDict={}; 

    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="adil1234",
    database="thesis"
    )

    def readFile(self,fileName):
        f = open(fileName,'r')
        message=f.read();
        data=message[message.find('DATA;')+5:]

        stp=data[:data.find('ENDSEC;')]
        stp=stp.replace(' ', '');
        self.myList=stp.split(';');
        #print('SUCCESS');

    def extractFile(self):
        for i in self.myList:
            self.refParamList=[];
            self.elemList.append(i[i.find('=')+2:i.find('(')]);
            self.refDicts[i[i.find('#')+1:i.find('=')]] = i[i.find('=')+1:i.find('(')];
            params=i[i.find('(')+1:i.find(';')];
            params=params.replace(")","").replace("(","");
            paramsList=params.split(',');
            for j in paramsList:
                if('#' in j):
                    self.refParamList+=j.split('#');
                    self.paramDicts[i[i.find('#')+1:i.find('=')]]=paramsList;
                    self.refParamDict[i[i.find('#')+1:i.find('=')]]=list(filter(None, self.refParamList));
        #print('SUCCESS');
 
 

    def writeExcel(self,fileName): 
        filename = fileName+".xlsx"; 
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        row=1;
      
        worksheet.write(0, 0,'KEY')
        worksheet.write(0, 1,'ENTITY')
        worksheet.write(0, 2,'D0')
        worksheet.write(0, 3,'D1')
        worksheet.write(0, 4,'D2')
        worksheet.write(0, 5,'D3')
        worksheet.write(0, 6,'D4')
        worksheet.write(0, 7,'D5')
        worksheet.write(0, 8,'D6')
        worksheet.write(0, 9,'D7')
        worksheet.write(0, 10,'REFERENCES')
        for (key,value),(key1,value1),(key2,value2) in zip(self.paramDicts.items(),self.refDicts.items(),self.refParamDict.items()):
            #print("\nKey::"+key+":Value::"+value1);
            col=2;
            if(value1!=''):
                worksheet.write(row, 0,key)
                worksheet.write(row, 1,value1)
                worksheet.write(row, 10,str(value2))
                for v in value:
                    if(col==10):
                        break;
                    if(v[0:1]=='#'):
                        worksheet.write(row, col,v[1:])
                    elif(v=='.T.'):
                        worksheet.write(row, col,'0001')
                    elif(v=='.F.'):
                        worksheet.write(row, col,'0000')
                    elif(v[0:1]=='.'):
                        worksheet.write(row, col,'0003')                
                    else:
                       # print(str(v),end=",");
                        worksheet.write(row, col,str(v))
                    col+=1;               
            row+=1;      

        workbook.close()
        print('SUCCESS');
    
    def writeCSV(self,fileName): 
        read_file = pd.read_excel (fileName+".xlsx",header=None)  
        read_file.to_csv (fileName+".csv",header=None,index=False) 
    
    def replace_non_numeric(self,col,df):
#    df[col] = pd.to_numeric(df[col], errors='coerce')
#    col = df[df[col].isna(00)]
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Replace NaN values (originally non-numeric values) with a specified value, e.g., 0
        df[col].fillna(0, inplace=True)    
           

    def cleanData(self,fileName):

        df=pd.read_csv(fileName+".csv")
        df.drop_duplicates(keep=False, inplace=True)
        df.dropna(subset=['KEY','ENTITY'], inplace=True)
        df['D0'] = df['D0'].str.replace("'","")
        df['REFERENCES'] = df['REFERENCES'].str.replace("'","")
        self.replace_non_numeric('D0',df);    
        self.replace_non_numeric('D1',df);
        self.replace_non_numeric('D2',df);
        self.replace_non_numeric('D3',df);
        self.replace_non_numeric('D4',df);
        self.replace_non_numeric('D5',df);
        self.replace_non_numeric('D6',df);
        self.replace_non_numeric('D7',df);	
        df.to_csv(fileName+".csv",index=False);
    
    def describe_data(self,fileName):
        json_data_list = [];
        df=pd.read_csv(fileName+".csv")
        col_name = df.columns
        dtyp = df.dtypes
        uniq = df.nunique()
        uniqu = df.isnull().sum()
        na_val = df.isna().sum()
        val_count=df.columns.value_counts(dropna=False)
        for i in range(len(df.columns)):
            #print("%38s %10s   %10s %10s  %10s  %10s" % (col_name[i], dtyp[i], uniq[i], na_val[i],val_count[i],uniqu[i]))
            #    json_data_list['Column_Name'] = col_name[i]
            #    json_data_list['Data_Type'] = dtyp[i]
            #    json_data_list['Unique'] = uniq[i]
            #    json_data_list['Null_Values'] =  na_val[i]
            #    json_data_list['Values_Count'] = val_count[i]
            #    json_data_list['Unique'] = uniqu[i]  
            json_data_list.append({'Column_Name':col_name[i],'Data_Type':dtyp[i],'Unique':uniq[i],'Null_Values':na_val[i],'Values_Count':val_count[i],'Unique':uniqu[i]});
        data={
        'status':'success',
        'No_Rows':df.shape[0],
        'No_Columns':df.shape[1],
        'Total_NA':df.isna().sum().sum(),
        'Column_Data':json_data_list
        }
        return json.dumps(data,default=str);
        
        
    def create_charts_1(self,fileName):
        graph_img_path="D:/Thesis/Project/Chatbot/src/assets/graph";
        df=pd.read_csv(fileName+".csv")
        
        ##########################
        data = df.drop(['ENTITY','REFERENCES'],axis=1)
        #correlation = data.corr(method='pearson')
        plt.plot(data)
        plt.savefig(graph_img_path+"/graph_1.png")
        
        ###################################
        plt1 =data.plot(kind = 'box')
        fig = plt1.get_figure()
        fig.savefig(graph_img_path+"/graph_2.png")
        
        ###################################
        plt2 =data.plot(kind = 'density')
        fig = plt2.get_figure()
        fig.savefig(graph_img_path+"/graph_3.png")
        
        ###################################
        plt3 =data.plot(kind = 'density')
        fig = plt3.get_figure()
        fig.savefig(graph_img_path+"/graph_4.png")
        
        ###################################
        plt4=sns.boxplot(df)
        fig = plt4.get_figure()
        fig.savefig(graph_img_path+"/graph_5.png")
        
        ###################################
        plt5=sns.stripplot(data=df.drop(["ENTITY","REFERENCES"], axis=1).astype(float))
        fig = plt5.get_figure()
        fig.savefig(graph_img_path+"/graph_6.png")
        
        ###################################
        #dff=pd.DataFrame(df['ENTITY'],df['ENTITY'].value_counts())
        #plt6=sns.violinplot(x="count",y="ENTITY", data =dff)
        #fig = plt6.get_figure()
        #fig.savefig(graph_img_path+"/graph_7.png")
        
        ###################################
        dff=pd.DataFrame(df['ENTITY'],df['ENTITY'].value_counts())
        plt7=sns.swarmplot(x="count",y="ENTITY", data = dff)
        fig = plt7.get_figure()
        fig.savefig(graph_img_path+"/graph_8.png")
        ###################################
        #ax = df['ENTITY'].value_counts().head(15).plot(kind='bar', title='Top 10 Years Coasters Introduced')
        #ax.set_xlabel('Year Introduced')
        #ax.set_ylabel('Count')

        #plt.savefig(graph_img_path+"/graph_9.png")
        ###################################
        #dc={}
        #i=0
        #for x in df['REFERENCES']:
        #    if(len(list(x[1:x.find(']')].split(',')))>4):
        #        dc[i]=len(list(x[1:x.find(']')].split(',')))
        #        i+=1
        #plt9=plt.hist([key for key, val in dc.items() for _ in range(val)], bins=20)
        #fig=plt9.get_figure()
        #fig.savefig(graph_img_path+"/graph_10.png")
        
    def send_email(self,sender,subject,body):
    
# Define email sender and receiver
        email_sender = 'adilubit@gmail.com'
        email_password = 'zboy hqny zbkt hcpc'
        email_receiver = 'adil_abdullah@hotmail.com'

# Set the subject and body of the email
        try:
            subject = subject
            body = body

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

        # Add SSL (layer of security)
            context = ssl.create_default_context()

        # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
            return 'success';
        except Exception as e:
            return str(e);



    def insert_user(self,user):
        try:
            print(user['user']['email']);
            print(user['user']['username']);
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO user_info (email,username,user_password,user_cpassword,account_status) VALUES (%s,%s,%s,%s,%s)"
            val = (user['user']['email'],user['user']['username'],user['user']['password'],user['user']['cpassword'],'Y')
            mycursor.execute(sql, val)
            self.mydb.commit()
            mycursor.close();
            self.mydb.close()
            return 'success';
        except Exception as e:
            return str(e);    
            
    def login_user(self,user):
        try:
            print(user['user']['username']);
            print(user['user']['password']);
            mycursors = self.mydb.cursor()

            sql="SELECT * from user_info where (email=%s or username=%s) and user_password=%s"
            val=(user['user']['username'],user['user']['username'],user['user']['password']);
            mycursors.execute(sql,val)
            mycursors.fetchall()
            print("Result::"+str(mycursors.rowcount))
            if(mycursors.rowcount<1):
                return 'not found';
            else:
                return 'success';
        except Exception as e:
            return str(e);       

    def calculate_face_area(self,face):
        """
        Calculate the area of a given face.
        """
        props = GProp_GProps()
        brepgprop_SurfaceProperties(face, props)
        return props.Mass()

    def calculate_area(self,shape):
        topology = TopologyExplorer(shape)
        faces = list(topology.faces())
        areaList=[];
    # Calculate the area of each face and print it
        for i, face in enumerate(faces, start=1):
            area = self.calculate_face_area(face)
#        print(f"Face {i}: Area = {area:.2f} square units")
            areaList.append(f"Face {i}: Area = {area:.2f} square units")
        return areaList;
    
    def calculate_edge(self,shape):
        edge_explorer = TopExp_Explorer(shape, TopAbs_EDGE)
        # Count the number of edges
        edge_count = 0
        while edge_explorer.More():
            edge_count += 1
            edge_explorer.Next()
#    print("Edge count::"+str(edge_count));    
        return str(edge_count);  
      
    def calculate_vertex(self,shape):
        vertices = []
        vertex_explorer = TopExp_Explorer(shape, TopAbs_VERTEX)
        while vertex_explorer.More():
            vertex = topods_Vertex(vertex_explorer.Current())
            pnt = BRep_Tool.Pnt(vertex)
            vertices.append((pnt.X(), pnt.Y(), pnt.Z()))
            vertex_explorer.Next();
#    for vertex in vertices:
#        print(vertex)
        return vertices;    
            
    def read_step_file(self,file_path):
        step_reader = STEPControl_Reader()
        Interface_Static_SetCVal("read.step.product.mode", "1")
        status = step_reader.ReadFile(file_path)
        if status != 1:
            raise Exception("Error: can't read file.")
        step_reader.TransferRoot(1)
        shape = step_reader.Shape(1)
        return shape
    # Function to extract properties
    def extract_properties(self,shape):
        properties = {}
        
        face_count = 0
        plane_count = 0
        cylinder_count = 0
        
        # Volume properties
        props = GProp_GProps()
        brepgprop_VolumeProperties(shape, props)
        properties['Volume'] = props.Mass()
        properties['Center of Mass'] = props.CentreOfMass().Coord()
        # properties['Inertia Matrix'] = props.MatrixOfInertia();#.Data()
        inertia_matrix = props.MatrixOfInertia()
        properties['Inertia Matrix'] = [[inertia_matrix.Value(i, j) for j in range(1, 4)] for i in range(1, 4)]

        # Surface area
        brepgprop_SurfaceProperties(shape, props)
        properties['Surface Area'] = props.Mass()

        # Exploring Faces to get more details
        exp = TopExp_Explorer(shape, TopAbs_FACE)
        face_count = 0
        
        for _ in range(exp.More()):
            face = topods_Face(exp.Current())
            surf = BRepAdaptor_Surface(face, True)
            if surf.GetType() == GeomAbs_Plane:
                plane_count += 1
            elif surf.GetType() == GeomAbs_Cylinder:
                cylinder_count += 1
            
            face_count += 1
            exp.Next()
        
        properties['Number of Faces'] = face_count

        # Exploring Solids
        exp = TopExp_Explorer(shape, TopAbs_SOLID)
        solid_count = 0
        for _ in range(exp.More()):
            solid_count += 1
            exp.Next()
        
        properties['Number of Solids'] = solid_count
        properties['Number of planes'] = plane_count
        properties['Number of cylinder'] = cylinder_count
        return properties
        
    def step_properties(self,filename):
        shape = self.read_step_file(filename)
        properties = self.extract_properties(shape)
        propsList=[];
        elemList=[];
        for prop, value in properties.items():
            propsList.append(f"{prop}: {value}");
        elemList.append(propsList);
        elemList.append(self.calculate_vertex(shape));
        elemList.append(self.calculate_edge(shape));
        elemList.append(self.calculate_area(shape));
        return elemList
#writeExcel('Example02');
#writeCSV('Example02');
#cleanData('Example02');



#obj=Thesis()
#obj.readFile("D:\\Nitrexo\\Sample Steps\\Example02.STEP")
#obj.extractFile()
#obj.writeExcel('Example02');
#obj.writeCSV('Example02');
#obj.cleanData('Example02');