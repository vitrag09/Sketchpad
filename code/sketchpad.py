import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from os import system
from PIL import Image, ImageTk,ImageColor,ImageGrab
import io
import pickle

class Paint(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Sketchpad")
        self.root.resizable(False,False)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        #building ui component
        self.create_ui()
        
        #creating essential variables and binding methods
        self.setup()
        # self.rect = self.canvas.create_rectangle(0,0,1200,200,fill="#FF9933")
        # self.rect = self.canvas.create_rectangle(0,400,1200,600,fill="#138808")
        # self.circle= self.canvas.create_oval(510,210,690,390,outline="#000080",width=10)
        # #self.circle= self.canvas.create_oval(580,280,620,320,fill="#000080",width=5)
        # temp_x=510
        # temp_y=300
            
        
        # self.line = self.canvas.create_line(600,300,temp_x,temp_y,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,temp_x+180,temp_y,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,temp_x+90,temp_y-90,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,temp_x+90,temp_y+90,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,560,215,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,538,238,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,518,263,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,538,362,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,671,245,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,658,362,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,643,222,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,690,270,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,682,335,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,634,378,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,565,380,fill="#000080",width=10)
        # self.line = self.canvas.create_line(600,300,516,330,fill="#000080",width=10)
        self.root.mainloop()

    def update_mode(self,i):
        if self.mode=="copy" or self.mode=="cut" or self.mode=="ungroup":
            for t in self.copied_tag_list:
                self.canvas.itemconfig(t,dash=(255,255))
        elif self.mode=="group":
            for t in self.grouping_list:
                self.canvas.itemconfig(t,dash=(255,255))
            self.groups.append(self.grouping_list)
            self.grouping_list=[]
        
        elif self.mode=="polygon" or self.mode=="polyline":
            self.polygon_start_point_saved=False
            if self.mode=="polygon":
                self.poly = self.canvas.create_line(self.start_polygon[0], self.start_polygon[1], self.previous_point_poly.x,self.previous_point_poly.y,fill = self.color,tags=self.polygon_tag)
            self.l.append(self.polygon_tag)
            self.polygon_tag=""
            self.start_polygon=[]
            self.previous_point_poly=""
        self.previous_mode=self.mode
        if self.icons[i]=="undo":
            self.use_undo()   
        elif self.icons[i]=="redo":
            self.use_redo()   
        elif self.icons[i]=="save":
            self.save_canvas()   
        elif self.icons[i]=="open":
            self.load()
            
        else:
            #it will update the mode when buttom will get clicked
            self.icon_buttons[self.previous_button_clicked]['state']="normal"
            self.previous_button_clicked=i
            self.mode_status_var.set(self.icons[i]) 
            self.icon_buttons[i]['state']="disabled"
            self.mode=self.icons[i]
        

    def update_color(self,i):
        self.color=self.colors[i]
        self.main_color["image"]=self.color_img[i]
    def update_coord_label(self,event):
        self.coord_x_y.set('(x,y)=( , )')
    def update_coord_label_xy(self,event):
        self.coord_x_y.set("(x,y)=("+str(event.x)+","+str(event.y)+")")
    
    def create_ui(self):
        #creating top frame
        self.topframe=Frame(self.root,height=700,padx=2)
        self.topframe.grid(row=0)

        #making icons toolbar
        self.icon_frame = Frame(self.topframe,borderwidth=3, relief="sunken",padx=1,height=700)
        self.icon_frame.columnconfigure(0, weight=1)
        self.icon_frame.columnconfigure(1, weight=7)
        
        self.icons=["pen","line","square","rectangle","oval","circle","polygon","polyline","move","cut","copy","paste","save","open","undo","redo","group","ungroup"]
        self.icons_img=[ImageTk.PhotoImage(Image.open('icons/'+i+'.png').resize((20,20))) for i in self.icons]
        self.icon_buttons=[0]*len(self.icons)

        for i in range(len(self.icons)):
            self.icon_buttons[i]=Button(self.icon_frame,image=self.icons_img[i],command=lambda m=i: self.update_mode(m),borderwidth=0,width=40,height=40,padx=10,pady=10)
            self.icon_buttons[i].grid(column=i%2,row=int(i/2),sticky=["e","w"][i%2],padx=0,pady=0,ipadx=0,ipady=0)
        self.icon_frame.grid(row=0,column=0,sticky="nw")
        #making pen as default mode 
        self.previous_button_clicked=0
        self.icon_buttons[self.previous_button_clicked]['state']='disabled'
        self.mode=self.icons[self.previous_button_clicked]

        #making canvas frame
        self.canvas_frame=Frame(self.topframe,borderwidth=3, relief="groove",padx=0,width=1200,height=600)
        self.canvas=tkinter.Canvas(self.canvas_frame,width=1200,height=600,background="white")
        self.canvas.pack(side=LEFT)
        self.canvas_frame.grid(row=0,column=1,sticky="nw")

        #making color palette frame
        self.color_palette_frame=Frame(self.root,borderwidth=2,padx=10,pady=10,relief="groove",width=1200,height=100)
        self.color_palette_frame.grid(row=1,column=0,columnspan=2,sticky="nsew")
        self.colors=["black","snow","maroon","cadetblue","dimgray","indigo","salmon","thistle","darkcyan","blanchedalmond","gold","red","olive","gainsboro","ivory","purple","lawngreen","fuchsia","teal","aqua","silver","crimson","mediumblue","moccasin"]
        
        self.color_palette=Frame(self.color_palette_frame,borderwidth=1, relief="sunken",padx=1,width=600)
        self.color_palette.columnconfigure(0, weight=1)
        self.color_palette.columnconfigure(1, weight=1)
        self.color_img=[ImageTk.PhotoImage(Image.new('RGB',(95,95),ImageColor.getrgb(i))) for i in self.colors]
        
        self.main_color_frame=Frame(self.color_palette_frame,borderwidth=1, relief="sunken",padx=7,pady=7,width=600)
        self.main_color_frame.pack(side=LEFT)
        self.main_color_frame.columnconfigure(0, weight=1)
        self.main_color_frame.columnconfigure(1, weight=1)
        self.main_color=Button(self.main_color_frame,image=self.color_img[0],relief="ridge",borderwidth=1,width=20,height=20,padx=10,pady=10)
        self.main_color.grid(row=0,column=0,padx=0,ipadx=0,ipady=0)

        self.color_buttons=[0]*len(self.colors)
        for i in range(len(self.colors)):
                self.color_buttons[i]=Button(self.color_palette,image=self.color_img[i],relief="ridge",command=lambda color_code=i: self.update_color(color_code),borderwidth=2,width=10,height=10,padx=1,pady=1)
                self.color_buttons[i].grid(column=2+int(i/2),row=int(i%2),sticky=["e","w"][i%2],padx=1,pady=1,ipadx=0,ipady=0)
        self.color_palette.pack(side=LEFT)

        #making bottom frame having coordinates and current mode and notes

        self.bottom_frame=Frame(self.root,borderwidth=2, relief="ridge",width=1200,height=50,padx=0)
        self.coord_frame = Frame(self.bottom_frame,borderwidth=1, relief="ridge",width=150,height=30,padx=0)
        self.mode_hints = Frame(self.bottom_frame,borderwidth=0, relief="ridge",width=100,height=30)
        self.mode_status = Frame(self.bottom_frame,borderwidth=1, relief="ridge",width=120,height=30)
        self.coord_img=ImageTk.PhotoImage(Image.open('icons/coord.png'))
        self.coord_icon=Label(self.coord_frame,image=self.coord_img)
        self.coord_icon.pack(side=LEFT,padx=0)
        self.coord_x_y = StringVar()
        self.coord_x_y.set('(x,y)=( , )')

        self.mode_status_var=StringVar()
        self.mode_status_var.set(self.mode)
        self.mode_status_label=Label(self.mode_status,textvariable=self.mode_status_var)
        self.mode_status_label.pack(side=LEFT)

        self.mode_hints_var=StringVar()
        self.mode_hints_var.set("choose the mode")
        self.mode_hints_label=Label(self.mode_hints,textvariable=self.mode_hints_var)
        self.mode_hints_label.pack(side=LEFT)
        
        self.coord_label = Label(self.coord_frame, textvariable=self.coord_x_y)
        self.coord_label.pack(side=LEFT)

        self.bottom_frame.grid(row=2,column=0,columnspan=2,sticky="nsew")
        self.coord_frame.pack_propagate(False)
        self.mode_status.pack_propagate(False)
        self.mode_hints.pack(side=LEFT,expand=False,fill=NONE)
        self.mode_status.pack(side=RIGHT,fill=BOTH,padx=1,expand=False)
        self.coord_frame.pack(side=RIGHT,expand=False,fill=NONE,padx=0)

    def setup(self):
        self.first=None
        self.last=None
        self.item=()
        self.data_dictionary=[]
        self.groups=[]
        self.cords_=[]
        self.l=[]
        self.events=[]
        self.old_x = None
        self.old_y = None
        self.line_width = 1
        self.color = self.colors[0]
        self.eraser_on = False
        self.copied=[]
        self.copied_tag_list=[]
        self.group_found=False
        self.selected=False
        self.previos_mode=None
        self.cut_action=False
        self.pasted=False
        self.grouping_started=False
        self.moving_tag_list=[]
        self.grouping_list=[]
        self.polygon_start_point_saved=False
        self.polygon_tag=[]
        self.previous_point_poly=[]
        self.start_polygon=[]
        self.previouscolor=self.color
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button>',self.activate)
        self.canvas.bind('<Leave>',self.update_coord_label)
        self.canvas.bind('<Motion>',self.update_coord_label_xy)

    def activate(self,event):
        self.first=event
        self.start=event
        #print(self.mode)
        tag="r"+str(1+len(self.l))
        if self.mode=="pen":
            self.old_x=event.x
            self.old_y=event.y
        elif self.mode=="rectangle":
            self.rect = self.canvas.create_rectangle(self.start.x, self.start.y, self.start.x+1, self.start.y+1,outline = self.color, fill="",tags=tag)
        elif self.mode=="square":
            self.sqr = self.canvas.create_rectangle(self.start.x, self.start.y, self.start.x+1, self.start.y+1,outline = self.color, fill="",tags=tag)
        elif self.mode=="line":
            self.line = self.canvas.create_line(self.start.x, self.start.y, self.start.x+1, self.start.y+1,fill = self.color,tags=tag)
        elif self.mode=="oval":
            self.oval = self.canvas.create_oval(self.start.x, self.start.y, self.start.x+1, self.start.y+1,outline = self.color, fill="",tags=tag)
        elif self.mode=="circle":
            self.circle = self.canvas.create_oval(self.start.x, self.start.y, self.start.x+1, self.start.y+1,outline = self.color, fill="",tags=tag)
        elif self.mode=="polygon" or self.mode=="polyline":
            if self.polygon_start_point_saved==False :
                self.start_polygon=[event.x,event.y]
                self.polygon_start_point_saved=True
                self.polygon_tag=tag
                self.previous_point_poly=event
                self.poly = self.canvas.create_line(self.start.x, self.start.y, self.start.x+1, self.start.y+1,fill = self.color,tags=self.polygon_tag)
            else:
                self.poly = self.canvas.create_line(self.previous_point_poly.x, self.previous_point_poly.y, event.x, event.y,fill = self.color,tags=self.polygon_tag)
                self.previous_point_poly=event
                self.poly = self.canvas.create_line(self.previous_point_poly.x, self.previous_point_poly.y, event.x+1, event.y+1,fill = self.color,tags=self.polygon_tag)
            
        elif self.mode=="group":
            if self.grouping_started==False:
                self.item=self.canvas.find_closest(event.x, event.y)
                self.cords_=self.canvas.coords(self.item[0])
                self.item=self.canvas.gettags(self.item[0])[0]
                for t in self.canvas.find_withtag(self.item):
                    self.grouping_list.append(t) 
                    self.canvas.itemconfig(t,dash=(3,5))
                self.grouping_started=True
            else:
                self.item=self.canvas.find_closest(event.x, event.y)
                self.cords_=self.canvas.coords(self.item[0])
                self.item=self.canvas.gettags(self.item[0])[0]
                for t in self.canvas.find_withtag(self.item):
                    if t in self.grouping_list:
                        self.canvas.itemconfig(t,dash=(255,255))
                        self.grouping_list.remove(t)
                    else:
                        self.grouping_list.append(t) 
                        self.canvas.itemconfig(t,dash=(3,5))
        elif self.mode=="ungroup":
            if self.group_found==False:
                self.item = self.canvas.find_closest(event.x, event.y)
                self.cords_=self.canvas.coords(self.item[0])
                self.item=self.canvas.gettags(self.item[0])[0]
                self.copied_tag_list=[ele for ele in self.canvas.find_withtag(self.item)]
                for temp_group in self.groups:
                    for ele in temp_group:
                        if ele in self.copied_tag_list:
                            for elem in temp_group:
                                self.group_found=True
                                if elem not in self.copied_tag_list:
                                    self.copied_tag_list.append(elem)
                
                for t in self.copied_tag_list:
                    self.canvas.itemconfig(t,dash=(3,5))
            else:
                for t in self.copied_tag_list:
                    self.canvas.itemconfig(t,dash=(255,255))
                self.item = self.canvas.find_closest(event.x, event.y)
                self.cords_=self.canvas.coords(self.item[0])
                self.item=self.canvas.gettags(self.item[0])[0]
                self.copied_tag_list=[ele for ele in self.canvas.find_withtag(self.item)]
                for temp_group in self.groups:
                    for ele in temp_group:
                        if ele in self.copied_tag_list:
                            del self.groups[self.groups.index(temp_group)]

                
                for t in self.copied_tag_list:
                    self.canvas.itemconfig(t,dash=(3,5))
                


        
        elif self.mode=="copy" or self.mode=="cut":
            self.item = self.canvas.find_closest(event.x, event.y)
            self.cords_=self.canvas.coords(self.item[0])
            self.item=self.canvas.gettags(self.item[0])[0]
            self.copied_tag_list=[ele for ele in self.canvas.find_withtag(self.item)]
            for temp_group in self.groups:
                for ele in temp_group:
                    if ele in self.copied_tag_list:
                        for elem in temp_group:
                            if elem not in self.copied_tag_list:
                                self.copied_tag_list.append(elem)
            
            for t in self.copied_tag_list:
                self.canvas.itemconfig(t,dash=(3,5))
            
            #self.canvas.itemconfig(self.item,dash=(3,5))
            self.copied=[[i,self.canvas.coords(i)] for i in set(self.copied_tag_list)]
            self.pasted=False
            if self.mode=="cut":
                self.cut_action=True 

        elif self.mode=="paste":
            if self.pasted==False and self.cut_action==False:
                tag="r"+str(1+len(self.l))
                self.l.append(tag)
                for ele in self.copied: 
                    self.item=ele[0]
                    self.cords_=ele[1]
                #self.cords_=self.copied[1]
                    diffx=(self.cords_[2]-self.cords_[0])/2
                    diffy=(self.cords_[3]-self.cords_[1])/2
                    diffx=self.last.x-event.x
                    diffy=self.last.y-event.y
                
                    #item_type=self.canvas.type(self.copied[0])
                    item_type=self.canvas.type(self.item)
                    if item_type=="rectangle":
                        self.item = self.canvas.create_rectangle(self.cords_[0],self.cords_[1],self.cords_[2],self.cords_[3],outline = self.color, fill="",tags=tag)
                    elif item_type=="line":
                        self.item = self.canvas.create_line(self.cords_[0],self.cords_[1],self.cords_[2],self.cords_[3],fill = self.color,tags=tag)
                    elif item_type=="oval":
                        self.item = self.canvas.create_oval(self.cords_[0],self.cords_[1],self.cords_[2],self.cords_[3],outline = self.color, fill="",tags=tag)
                    else:
                        print("error in paste when clicked") 
                    #self.canvas.coords(self.item,event.x-diffx,event.y-diffy,event.x+diffx,event.y+diffy)
                    self.canvas.coords(self.item,int(self.cords_[0])-diffx,int(self.cords_[1])-diffy,int(self.cords_[2])-diffx,int(self.cords_[3])-diffy)
                    #self.copied=[]
                    #self.cords_=self.canvas.coords(self.item)
                self.pasted=False
            elif self.cut_action==True:
                self.cut_action=False
                for ele in self.copied: 
                    self.item=ele[0]
                    self.cords_=ele[1]
                    diffx=self.last.x-event.x
                    diffy=self.last.y-event.y
                #self.canvas.coords(self.item,10+self.copied[1][0],10+self.copied[1][1],10+self.copied[1][2],10+self.copied[1][3])
                    self.canvas.coords(self.item,int(self.cords_[0])-diffx,int(self.cords_[1])-diffy,int(self.cords_[2])-diffx,int(self.cords_[3])-diffy)
                    self.canvas.itemconfig(self.item,state='normal')

            else:
                self.selected=True
                self.item = self.canvas.find_closest(event.x, event.y)
                self.cords_=self.canvas.coords(self.item[0])
                self.canvas.itemconfig(self.item,dash=(3,5))
            
                #self.canvas.itemconfig(self.item,dash=(3,5))
                #self.cords_=self.canvas.coords(self.item)

        elif self.mode=="move":
            self.item = self.canvas.find_closest(event.x, event.y)
            self.last=event
            for t in self.moving_tag_list:
                self.canvas.itemconfig(t,dash=(255,255))
            #self.canvas.itemconfig(self.item,dash=(3,5))
            self.item=self.canvas.gettags(self.item[0])[0]
            self.moving_tag_list=[ele for ele in self.canvas.find_withtag(self.item)]
        
            for temp_group in self.groups:
                for ele in temp_group:
                    if ele in self.moving_tag_list:
                        for elem in temp_group:
                            if elem not in self.copied_tag_list:
                                self.moving_tag_list.append(elem)
            for t in set(self.moving_tag_list):
                self.canvas.itemconfig(t,dash=(3,5))
            self.moving_tag_list=set(self.moving_tag_list)
            #self.cords_=self.canvas.coords(self.item)
        
        else:
            pass    
    
    def use_redo(self):
        data_dict=self.data_dictionary.pop()
        for i in range(len(data_dict["tags"])):
            x,y,x2,y2=int(data_dict["coord"][i][0]),int(data_dict["coord"][i][1]),int(data_dict["coord"][i][2]),int(data_dict["coord"][i][3])
            temp_tag=data_dict["tags"][i]
            temp_fill=data_dict["outline"][i]
            
            if(data_dict["type"][i]=="line"):
                temp_item=self.canvas.create_line(x,y,x2,y2,fill=temp_fill,tags=temp_tag)
            elif(data_dict["type"][i]=="rectangle"): 
                temp_item=self.canvas.create_rectangle(x,y,x2,y2,outline=temp_fill,tags=temp_tag,fill="")
            elif(data_dict["type"][i]=="oval"): 
                temp_item=self.canvas.create_oval(x,y,x2,y2,outline=temp_fill,tags=temp_tag)
            else:
                pass
            if temp_tag not in self.l:
                self.l.append(temp_tag)
    def use_undo(self):
        id=self.l.pop()
        tdata_dict={}
        tdata_dict["tags"]=[]
        tdata_dict["coord"]=[]
        tdata_dict["type"]=[]
        tdata_dict["outline"]=[]
        tdata_dict["group"]=self.groups
        for t in self.canvas.find_withtag(id):
            tdata_dict["tags"].append(self.canvas.itemcget(t,"tags"))
            tdata_dict["coord"].append(self.canvas.coords(t))
            tdata_dict["type"].append(self.canvas.type(t))
            if self.canvas.type(t)!="line":
                tdata_dict["outline"].append(self.canvas.itemcget(t,"outline"))
            else:
                tdata_dict["outline"].append(self.canvas.itemcget(t,"fill"))
        self.data_dictionary.append(tdata_dict)
        self.canvas.delete(id)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]


    def paint(self, event):
        paint_color =self.color
        self.coord_x_y.set("(x,y)=("+str(event.x)+","+str(event.y)+")")
        self.mode_status_var.set("(\u0394x,\u0394y)=("+str(-self.start.x+event.x)+","+str(-self.start.y+event.y)+")")
        if self.old_x and self.old_y and self.mode=="pen":
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,width=self.line_width, fill=paint_color,capstyle=ROUND, smooth=TRUE, splinesteps=36,tags="r"+str(1+len(self.l)))
        if self.mode=="line":
            self.canvas.coords(self.line, self.start.x, self.start.y, event.x, event.y)
        elif self.mode=="polygon" or self.mode=="polyline":
            self.canvas.coords(self.poly, self.previous_point_poly.x, self.previous_point_poly.y, event.x, event.y)
        elif self.mode=="oval":
            self.canvas.coords(self.oval, self.start.x, self.start.y, event.x, event.y)
        elif self.mode=="rectangle":
            self.canvas.coords(self.rect, self.start.x, self.start.y, event.x, event.y)
        elif self.mode=="square":
            diffx=event.x-self.start.x
            diffy=event.y-self.start.y
            self.canvas.coords(self.sqr, self.start.x, self.start.y,self.start.x+max(diffx,diffy),self.start.y+max(diffx,diffy))
        elif self.mode=="circle":
            diffx=event.x-self.start.x
            diffy=event.y-self.start.y
            self.canvas.coords(self.circle, self.start.x, self.start.y,self.start.x+max(diffx,diffy),self.start.y+max(diffx,diffy))
        elif self.mode=="move":
            diffx=self.last.x-event.x
            diffy=self.last.y-event.y
            tp=set(self.moving_tag_list)
            for t in tp:
                self.cords_=self.canvas.coords(t)
                self.canvas.coords(t,int(self.cords_[0])-diffx,int(self.cords_[1])-diffy,int(self.cords_[2])-diffx,int(self.cords_[3])-diffy)
        elif self.mode=="paste":
            diffx=self.start.x-event.x
            diffy=self.start.y-event.y
            #self.canvas.moveto(self.item,event.x,event.y)
            self.canvas.coords(self.item,int(self.cords_[0])-diffx,int(self.cords_[1])-diffy,int(self.cords_[2])-diffx,int(self.cords_[3])-diffy)
            #self.canvas.move(self.item,-diffx,-diffy)
        else:
            pass
            
        self.old_x = event.x
        self.old_y = event.y
        self.last=event


    def reset(self, event):
        if self.mode=="polygon" or self.mode=="polyline":
            self.previous_point_poly=event
            return
        self.mode_status_var.set(self.mode)
        if self.mode in ["rectangle","line","square","oval","circle","pen"]:
            self.old_x, self.old_y = None, None
            tag="r"+str(1+len(self.l))
            if -2<(self.start.x-event.x)<2 and -2<(self.start.y-event.y)<2:
                self.canvas.delete(tag)
            else:
                self.l.append(tag)
            # print(self.l)
            #self.canvas.bind(tag,'<Button>',self.activate)
            # self.canvas.bind(tag,'<B1-Motion>', self.paint)
            # self.canvas.bind(tag,'<ButtonRelease-1>', self.reset)
        
        if self.mode=="copy" :
            #self.canvas.itemconfig(self.item,dash=(255,255))
            for t in self.copied_tag_list:
                self.canvas.itemconfig(t,dash=(255,255))
            self.last=event
        if self.mode=="cut":
            #res=messagebox.askquestion('askquestion', 'do you want to cut '+str(self.canvas.type(self.item))+'?')
            #if res=="yes":
                
            #self.previouscolor=self.canvas.itemcget(self.item, "outline")
            #self.canvas.itemconfig(self.item,outline='white')
            for t in self.copied_tag_list:
                self.canvas.itemconfig(t,state='hidden')
                self.canvas.itemconfig(t,dash=(255,255))

        if self.mode=="move" or self.mode=="paste":
            try:
                for t in self.copied_tag_list:
                    self.canvas.itemconfig(t,dash=(255,255))
                for t in self.moving_tag_list:
                    self.canvas.itemconfig(t,dash=(255,255))
            except:
                pass
            self.selected=False
    def load(self):
        filename=filedialog.askopenfilename()
        with open(filename,"rb") as fp:
            data_dict=pickle.load(fp)
        for t in self.canvas.find_all():
            self.canvas.delete(t)
        self.groups=data_dict["group"]
        for i in range(len(data_dict["tags"])):
            x,y,x2,y2=int(data_dict["coord"][i][0]),int(data_dict["coord"][i][1]),int(data_dict["coord"][i][2]),int(data_dict["coord"][i][3])
            temp_tag=data_dict["tags"][i]
            temp_fill=data_dict["outline"][i]
            
            if(data_dict["type"][i]=="line"):
                temp_item=self.canvas.create_line(x,y,x2,y2,fill=temp_fill,tags=temp_tag)
            elif(data_dict["type"][i]=="rectangle"): 
                temp_item=self.canvas.create_rectangle(x,y,x2,y2,outline=temp_fill,tags=temp_tag,fill="")
            elif(data_dict["type"][i]=="oval"): 
                temp_item=self.canvas.create_oval(x,y,x2,y2,outline=temp_fill,tags=temp_tag)
            else:
                print("error in loading")
            if temp_tag not in self.l:
                self.l.append(temp_tag)
        data_dict=[]
        
        
    def save_canvas(self):

        #filename=filedialog.SaveFileDialog()
        fp=filedialog.asksaveasfile(mode='w', defaultextension="")
        filename=fp.name
        fp.close()
        with open(filename,"wb") as fp:
            data_dict={}
            data_dict["tags"]=[]
            data_dict["coord"]=[]
            data_dict["type"]=[]
            data_dict["outline"]=[]
            data_dict["group"]=self.groups
            for t in self.canvas.find_all():
                data_dict["tags"].append(self.canvas.itemcget(t,"tags"))
                data_dict["coord"].append(self.canvas.coords(t))
                data_dict["type"].append(self.canvas.type(t))
                if self.canvas.type(t)!="line":
                    data_dict["outline"].append(self.canvas.itemcget(t,"outline"))
                else:
                    data_dict["outline"].append(self.canvas.itemcget(t,"fill"))
    
            pickle.dump(data_dict,fp)

        ps = self.canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(filename+'.jpg')
        
        
if __name__ == '__main__':
    Paint()
