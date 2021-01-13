import tkinter
from tkinter import *
from tkinter import ttk

import tkinter as tk

from Classes import*
from tkinter.ttk import Combobox

combo = 0
proc_list = ["choose"]
# root1:
mem_size = 0
update_var_gui = 0
our_memory=Memory(mem_size)

mem_size_root = Tk()
mem_size_root.title("Memory Size")
mem_size_root.geometry("300x200")

container1 = Frame(mem_size_root)
container1.pack()

label_size = Label(container1, text="Please enter Memory Size")
label_size.grid(row=1, column=1, padx=10, pady=15)

entry_size = Entry(container1)
entry_size.grid(row=2, column=1, pady=15)

# root2
hole_info_root =Tk()
hole_info_root.title("Hole Info")
hole_info_root.geometry("450x250")

label_info = Label(hole_info_root, text="Please enter Hole Info : ")
label_info.grid(row=1, column=1, padx=5, pady=5)

label_hole_size = Label(hole_info_root, text="  Size  : ")
label_hole_size.grid(row=2, column=1, padx=50, pady=20)

entry_hole_size = Entry(hole_info_root)
entry_hole_size.grid(row=2, column=2, padx=10)

label_base = Label(hole_info_root, text="  Base  : ")
label_base.grid(row=3, column=1, padx=50, pady=25)

entry_hole_base = Entry(hole_info_root)
entry_hole_base.grid(row=3, column=2, padx=10)

hole_info_root.withdraw()


# root3
add_or_show_root =Tk()
add_or_show_root.title("Add Process-Show Table")
add_or_show_root.geometry("350x250")

container3 = Frame(add_or_show_root)
container3.pack()
add_or_show_root.withdraw()


current_var=StringVar()
# current_var.set("Process 000")



# root4
no_of_seg_root = Tk()
no_of_seg_root.title("Segments Number")
no_of_seg_root.geometry("200x200")

container2 = Frame(no_of_seg_root)
container2.pack()

label_no = Label(container2, text="Number of Segments ")
label_no.grid(row=1, column=2, padx=10, pady=15)

entry_seg_no = Entry(container2)
entry_seg_no.grid(row=2, column=2, pady=15)

no_of_seg_root.withdraw()

# root5
seg_info_root = Tk()
seg_info_root.title("Segments Info")
seg_info_root.geometry("400x250")

label_info = Label(seg_info_root, text="Enter Segment info : ")
label_info.grid(row=1, column=1, padx=10, pady=15)

label_seg_name = Label(seg_info_root, text="Name : ")
label_seg_name.grid(row=2, column=1, padx=10, pady=15)

entry_seg_name = Entry(seg_info_root)
entry_seg_name.grid(row=2, column=2, pady=15)

label_seg_size = Label(seg_info_root, text="Size : ")
label_seg_size.grid(row=3, column=1, padx=10, pady=15)

entry_seg_size = Entry(seg_info_root)
entry_seg_size.grid(row=3, column=2, pady=15)

label_seg_type = Label(seg_info_root, text="Type : ")
label_seg_type.grid(row=4, column=1, padx=10, pady=15)

# entry_seg_type = Entry(seg_info_root)
# entry_seg_type.grid(row=4, column=2, pady=15)

seg_info_root.withdraw()

seg_name_list=[]
seg_size_list=[]
seg_type_list=[]

# counter_var=IntVar()
# counter_var.set(0)
counter=0
flag=False

chosen_type=StringVar()


def add_holes():
    global our_memory
    global mem_size
    global entry_hole_size
    global entry_hole_base

    hole_size=int(entry_hole_size.get())
    hole_base= int(entry_hole_base.get())

    print("add holes fn")
    print(entry_hole_size.get())

    our_memory.add_hole(hole_size,hole_base)

    entry_hole_size.delete(0, 'end')
    entry_hole_base.delete(0, 'end')

    hole_info_root.update()
    hole_info_root.deiconify()
    # our_memory.draw_memory()


def holes():
    print("hoooles")
    global hole_info_root
    global entry_hole_size
    global entry_hole_base

    btn_ok = Button(hole_info_root, text="    OK    ", command=lambda: [add_holes(),holes()])
    btn_ok.grid(row=4, column=2)

    btn_done = Button(hole_info_root, text="    Done    ",command=lambda :[redraw_memory(),add_or_show()])
    btn_done.grid(row=4, column=3)

    hole_info_root.update()
    hole_info_root.deiconify()


    # hole_info_root.mainloop()

def redraw_memory():
    global our_memory
    global mem_size
    global entry_hole_size
    global entry_hole_base

    hole_size = int(entry_hole_size.get())
    hole_base = int(entry_hole_base.get())
    our_memory.add_hole(hole_size, hole_base)

    our_memory.initialize_memory()
    our_memory.unify_holes()
    our_memory.draw_memory()
    print("drawn")


def add_or_show():
    global our_memory
    global mem_size
    global add_or_show_root
    global current_var
    global proc_list
    global update_var_gui
    global combo
    global seg_type_list
    global seg_size_list
    global seg_name_list
    global flag

    print("add")
    seg_info_root.withdraw()
    hole_info_root.withdraw()
    our_memory.print_memory_content()

    add_or_show_root.bind('<Double-Button-1>',update_add)

    seg_type_list.clear()
    seg_size_list.clear()
    seg_name_list.clear()
    flag = False

    # if update_var_gui > 0:
     # print("3lalal esht3'l bas")
      # update_add()

    print("7tet awl process")
    our_memory.print_memory_content()

    btn_add = Button(container3, text=" Add Process  ",command=number_of_seg)
    btn_add.grid(row=1, column=2,padx=30, pady=60)

    proc_list = ["choose"]
    for i in range(len(our_memory.seg_table_list)):
        temp_str = "Process  " + str(our_memory.seg_table_list[i].process_no)
        print(f"ady ya3m el list {temp_str}")
        proc_list.append(temp_str)

    current_var.set(proc_list[1])
    print("current :"+str(current_var.get()))
    # combo=apply(OptionMenu,(container3, current_var)+list(proc_list))
    combo = ttk.OptionMenu(container3,current_var, *proc_list)
    # current_var.set(proc_list[0])

    combo.grid(row=2,column=2)
    # combo.focus()

    btn_ok = Button(container3, text="    OK    ",command=view_table)
    btn_ok.grid(row=3, column=2, pady=15)

    add_or_show_root.update()
    add_or_show_root.deiconify()


def update_add(event):
    global proc_list
    global combo
    global current_var
    print("da5lt aho ya3m ")
    proc_list = ["choose"]
    current_var.set(' ')
    combo['menu'].delete(0,'end')
    for i in range(len(our_memory.seg_table_list)):
        temp_str = "Process  " + str(our_memory.seg_table_list[i].process_no)
        print(f"ady ya3m el list ya 3m ell 7ag {temp_str}")
        proc_list.append(temp_str)
        for choice in str(our_memory.seg_table_list[i].process_no):
            combo['menu'].add_command(label=choice, command=tkinter._setit(current_var, choice))
    combo = ttk.OptionMenu(container3, current_var, *proc_list)
    combo.grid(row=2, column=2)
    combo.update()
    add_or_show_root.update()


def add_show():
    add_or_show_root.withdraw()
    add_or_show()


def view_table():
    global current_var
    req_index=-1
    current_var.get()
    print("pront table :"+str(current_var.get()))
    for i in range(len(our_memory.seg_table_list)):
        temp_str = "Process  " + str(our_memory.seg_table_list[i].process_no)
        print(temp_str)
        if current_var.get() == temp_str:
            print("sa7 aho")
            req_index=i
            break
        print("el index :" + str(req_index))
    our_memory.seg_table_list[req_index].draw_segment_table()


def view_memory():
    global our_memory
    global mem_size

    # global entry_size
    print("button clicked")
    print(entry_size.get())
    if str(entry_size.get()).isnumeric():
        mem_size = int(entry_size.get())
    our_memory = Memory(mem_size)
    # our_memory.add_hole(mem_size,0)
    # our_memory.draw_memory()
    print("here")
    # our_memory.remove_hole(0)

    mem_size_root.destroy()


def number_of_seg():
    global no_of_seg_root
    global add_or_show_root

    print("number of seg")

    add_or_show_root.withdraw()

    btn_size_ok = Button(container2, text="    OK    ",command=seg_info)
    btn_size_ok.grid(row=3, column=2, pady=15)

    no_of_seg_root.update()
    no_of_seg_root.deiconify()


def seg_info():
    global our_memory
    global seg_info_root
    global entry_seg_size
    global entry_seg_size
    global entry_seg_no
    global seg_name_list
    global seg_size_list
    global seg_type_list
    global entry_seg_name
    global entry_seg_type
    global counter

    counter=int(entry_seg_no.get())

    seg_type_list.clear()
    seg_size_list.clear()
    seg_name_list.clear()

    entry_seg_no.delete(0,'end')
    no_of_seg_root.withdraw()
    call_OK_btn()


   # btn_ok = Button(seg_info_root, text="    OK    ",command=add_segment)
    # btn_ok.grid(row=5, column=2, pady=15)

    # seg_info_root.update()
    # seg_info_root.deiconify()

    # seg_info_root.mainloop()


def call_OK_btn():
    global our_memory
    global seg_info_root
    global entry_seg_size
    global entry_seg_no
    global seg_name_list
    global seg_size_list
    global seg_type_list
    global entry_seg_name
    global entry_seg_type
    global counter
    global chosen_type

    entry_seg_name.delete(0,'end')
    entry_seg_size.delete(0,'end')

    option_seg_type =ttk.OptionMenu(seg_info_root, chosen_type, "choose", "First Fit", "Best Fit")
    chosen_type.set("First Fit")

    option_seg_type.grid(row=4, column=2)

    print("Waiting for ok to be pressed.....")
    btn_ok = Button(seg_info_root, text="    OK    ", command=add_segment)
    btn_ok.grid(row=5, column=2, pady=10)

    btn_cancel = Button(seg_info_root, text="    Cancel    ", command=add_or_show)
    btn_cancel.grid(row=5, column=3, pady=10 )

    seg_info_root.update()
    seg_info_root.deiconify()


def clear_lists():
    global seg_type_list
    global seg_size_list
    global seg_name_list
    global flag

    seg_type_list.clear()
    seg_size_list.clear()
    seg_name_list.clear()
    flag = False
# def counter_inc():
    # global counter_var
    # counter_var.set(counter_var.get()-1)
    # counter.set(counter.get()-1)
    # print("counter dec Function ->  new counter :  "+str(counter_var.get()))


def add_segment():
    global our_memory
    global seg_info_root
    global entry_seg_size
    global seg_name_list
    global seg_size_list
    global seg_type_list
    global entry_seg_name
    global entry_seg_type
    global counter
    global flag
    global chosen_type
    # global number_of_seg

    our_memory.print_memory_content()

    t=chosen_type.get()
    print(t)
    # counter_var.set(counter_var.get()-1)
    if counter > 1 :
        print("loop counter :" +str(counter))

        seg_name=str(entry_seg_name.get())
        seg_size=int(entry_seg_size.get())
        # seg_type=int(chosen_type.get())
        if t=="First Fit" :
            seg_type =0
        elif t=="Best Fit":
            seg_type=1
        print("Added seg" + str(seg_name)+str(seg_size)+str(seg_type))

        seg_name_list.append(seg_name)
        seg_size_list.append(seg_size)
        seg_type_list.append(seg_type)
        entry_seg_name.delete(0,'end')
        entry_seg_size.delete(0, 'end')
        # entry_seg_type.delete(0, 'end')
        counter = counter - 1
        call_OK_btn()

    elif counter == 1 and flag==False:
        seg_name = str(entry_seg_name.get())
        seg_size = int(entry_seg_size.get())
        # seg_type = int(chosen_type.get())
        if t == "First Fit":
            seg_type = 0
        elif t == "Best Fit":
            seg_type = 1

        print("Added seg" + str(seg_name) + str(seg_size) + str(seg_type))
        seg_name_list.append(seg_name)
        seg_size_list.append(seg_size)
        seg_type_list.append(seg_type)
        entry_seg_name.delete(0, 'end')
        entry_seg_size.delete(0, 'end')
        # entry_seg_type.delete(0, 'end')
        flag = True

        seg_info_root.withdraw()

        checK,failed_seg=our_memory.add_process(len(seg_name_list),seg_name_list,seg_size_list,seg_type_list)
        print(checK)
        if checK is False:
            error = Tk()
            error.withdraw()
            tkinter.messagebox.showinfo('Error', 'Not enough space to allocate segment number :' + str(
                failed_seg) +' Deallocate or cancel ')
            call_OK_btn()

        elif checK is True:
            print("finished")
            seg_type_list.clear()
            seg_size_list.clear()
            seg_name_list.clear()
            flag=False
            # our_memory.initialize_memory()
            our_memory.draw_memory()
            add_or_show()

    elif counter == 1 and flag==True:
        checK, failed_seg = our_memory.add_process(len(seg_name_list), seg_name_list, seg_size_list, seg_type_list)
        print(checK)
        if checK is False:
            error = Tk()
            error.withdraw()
            tkinter.messagebox.showinfo('Error', 'Not enough space to allocate segment number :' + str(
                failed_seg) + ' Deallocate or cancel ')
            call_OK_btn()


        elif checK is True:
            print("finished")
            # our_memory.initialize_memory()
            seg_type_list.clear()
            seg_size_list.clear()
            seg_name_list.clear()
            flag=False
            our_memory.draw_memory()
            add_or_show()


btn_size_ok = Button(container1, text="    OK    ", command = lambda: [view_memory(),holes()])
btn_size_ok.grid(row=3, column=1, pady=15)

mem_size_root.mainloop()












