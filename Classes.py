from tkinter import*
from math import*
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Segment:
    segment_name: str
    segment_no: int
    size: int
    base: int
    process_no: int
    verified: bool
    type: bool  # 0 for first and 1 for best

    def __init__(self, name, size, base, process_no, type_m):
        self.segment_name = name
        self.size = size
        self.base = base
        self.process_no = process_no
        self.verified = False
        self.type = type_m
        self.segment_no = 0


class SegmentTable:
    segment_list: list
    process_no: int
    segment_counter: int

    def __init__(self, process_no):
        self.segment_list = []
        self.process_no = process_no
        self.segment_counter = 0


    def verify(self):
        for i in range(len(self.segment_list)):
            self.segment_list[i].verified = True

    def delete_not_verified(self):
        for i in range(len(self.segment_list)):
            if not self.segment_list[i].verified:
                self.segment_list.pop(i)

    def draw_segment_table(self):

        data = np.empty([len(self.segment_list), 4], dtype='object_')
        rowtext = []
        self.order_segment_no()

        fig, table = plt.subplots()

        collabeL = ["Segment Number", "Segment Name", "Base Address", "Segment Size"]


        for i in range(len(self.segment_list)):
            rowtext.append(str(self.segment_list[i].segment_no))
            rowtext.append(self.segment_list[i].segment_name)
            rowtext.append(str(self.segment_list[i].base))
            rowtext.append(str(self.segment_list[i].size))
            data[i] = rowtext
            rowtext.clear()

        fig.patch.set_visible(False)
        table.axis('off')
        table.axis('tight')
        df = pd.DataFrame(data, columns=collabeL)
        table.table(cellText=df.values, colLabels=df.columns, loc='center')
        fig.tight_layout()
        plt.savefig("Seg_Table.png")
        plt.show()

    def order_segment(self):
        for i in range(len(self.segment_list)):
            for j in range(i + 1, len(self.segment_list)):
                if self.segment_list[i].base > self.segment_list[j].base:
                    swap_positions(self.segment_list, i, j)

    def order_segment_no(self):
        for i in range(len(self.segment_list)):
            for j in range(i + 1, len(self.segment_list)):
                if self.segment_list[i].segment_no > self.segment_list[j].segment_no:
                    swap_positions(self.segment_list, i, j)

    def add_segment(self, segment):
        segment.segment_no = self.segment_counter   # zawedt hena 7war el segment no dah
        self.segment_counter += 1
        self.segment_list.append(segment)
        self.order_segment()  #hena shelt self

    # def draw_segment_table(self):


class Hole:
    size: int
    base: int

    def __init__(self, size, base):
        self.size = size
        self.base = base


class HolesTable:
   # Holes_list: list
   # Holes_list = []

    def __init__(self):
        self.Holes_list = []


    # for first fit base
    def order_hole_first(self):
        for i in range(len(self.Holes_list)):
            for j in range(i + 1, len(self.Holes_list)):
                if self.Holes_list[i].base > self.Holes_list[j].base:
                    swap_positions(self.Holes_list, i, j)

    # for the best fit size
    def order_hole_best(self):
        for i in range(len(self.Holes_list)):
            for j in range(i + 1, len(self.Holes_list)):
                if self.Holes_list[i].size > self.Holes_list[j].size:
                    swap_positions(self.Holes_list, i, j)

    def add_hole(self, hole):
        self.Holes_list.append(hole)

    def remove_hole(self, base_m):
        hole_size = 0
        for i in range(len(self.Holes_list)):
            if self.Holes_list[i].base == base_m:
                hole_size = self.Holes_list[i].size
                self.Holes_list.pop(i)
                break
        return hole_size




def swap_positions(mylist, pos1, pos2):
    mylist[pos1], mylist[pos2] = mylist[pos2], mylist[pos1]
    return mylist


class Memory:
    size: int
    process_counter: int
    #hole_table: HolesTable  # to declare global
    seg_table_list = []
    memorydraw = Tk()
    memorydraw.withdraw()


    def __init__(self, size):
        self.size = size
        self.process_counter = 1
        self.hole_table = HolesTable()
        self.memorydraw.withdraw()
        #self.elroot_ely_3mlto.withdraw()
        #temp_hole_table=HolesTable()
        #self.hole_table = temp_hole_table
        #self.hole_table.Holes_list= []

    def print_memory_content(self):
        self.hole_table.order_hole_first()
        ordered_seg_list = []

        for i in range(len(self.hole_table.Holes_list)):
            print("Hole no" + str(i) + "  ->  base: " + str(self.hole_table.Holes_list[i].base)+"    size: "+ str(self.hole_table.Holes_list[i].size))

        for i in range(len(self.seg_table_list)):
            print("process no "+ str(self.seg_table_list[i].process_no))
            for j in range(len(self.seg_table_list[i].segment_list)):
                print("segment "+ str(j) + "   -> base: " + str(self.seg_table_list[i].segment_list[j].base) + "   size: " + str(self.seg_table_list[i].segment_list[j].size))

    def find_seg_by_range(self,x,y,x_shift):

        if x_shift <= x <= (x_shift + 300):   # 300 is mem width
            for i in range(len(self.seg_table_list)):
                for j in range(len(self.seg_table_list[i].segment_list)):
                    if self.seg_table_list[i].segment_list[j].base <= y <= \
                            (self.seg_table_list[i].segment_list[j].base +
                             self.seg_table_list[i].segment_list[j].size):
                        temp_segment = self.seg_table_list[i].segment_list[j]
                        return temp_segment
        temp = Segment("Error1",0,0,0,0)
        return temp

    def draw_memory(self):

        def deallocate_process_when_pressed(event):   # m7tag tazbet kter
            global current_row
            x, y = getxy(event)
            y = (y * self.size)/var_x
            x_shift = text_width + 50
            temorary_seg = Segment("TEMP",0,0,0,0)
            temorary_seg = self.find_seg_by_range(x, y, x_shift)
            print(f"y is base is: {y}")
            hole_or_not = self.is_hole_range(y)
            if not hole_or_not and x >= x_shift:
                print("ha deallocate 7ader aho")
                self.deallocate_process(temorary_seg.process_no)
                self.unify_holes()

            current_row = 0
            self.memorydraw.option_clear()
            self.memorydraw.withdraw()
            self.draw_memory()
            print("done") # confirmation

        def getxy(event):
            x = self.memorydraw.winfo_pointerx()
            y = self.memorydraw.winfo_pointery()
            abs_coord_x = self.memorydraw.winfo_pointerx() - self.memorydraw.winfo_rootx()
            abs_coord_y = self.memorydraw.winfo_pointery() - self.memorydraw.winfo_rooty()
            print(f"({abs_coord_x},{abs_coord_y})")
            return abs_coord_x,abs_coord_y



        current_base = 0
        hole_or_seg = False
        hole_size = 0
        mem_width = 300
        text_width = 11 * int((log10(self.size)))
        text_width += int(0.1 * text_width)
        total_width = text_width + mem_width + 100
        current_row = 0
        var_x = 500
        self.memorydraw.deiconify()
        self.memorydraw.geometry(f"{total_width}x550")
        self.memorydraw.resizable(True,True)
        memory = Frame(self.memorydraw, height=var_x, width=mem_width)
        text = Frame(self.memorydraw, height=var_x, width=text_width)
        self.memorydraw.bind('<Button-1>', deallocate_process_when_pressed)
        memory.place(x=text_width + 50, y=0) # text_width + 50 is x shifting for memory
        text.place(x=0, y=0)

        while current_base <= self.size:
            hole_or_seg, hole_size = self.is_hole(current_base)

            if hole_or_seg:
                F1 = Frame(text, height=((var_x * hole_size) / self.size), width=text_width, border=5).pack(side=TOP)
                info = Label(F1, text=f"{current_base}",fg="red").place(x=0, y=((var_x * current_base) / self.size))
                f = Frame(memory, bg="green", height=((var_x * hole_size) / self.size), width=mem_width, bd=5, relief="sunken").pack(side=TOP)
                # y is current base mapped height from top of window
                current_base += hole_size
                current_row += 1
            elif not hole_or_seg and current_base != self.size:
                temp_seg = self.find_seg(current_base)
                seg_size = temp_seg.size

                F1 = Frame(text, height=((var_x * seg_size) / self.size), width=text_width, border=5).pack(side=TOP)
                info = Label(F1, text=f"{current_base}",fg="red").place(x=0, y=((var_x * current_base) / self.size))
                FMEM = Frame(memory, height=((var_x * seg_size) / self.size), width=mem_width, bg="blue", border=5,relief="raised").pack(side=TOP)
                str = f"Process {temp_seg.process_no} / {temp_seg.segment_name} Segment"
                proc_label = Label(FMEM, bg="blue",text=str).place(x= (int((log10(self.size)))-50) + int((0.5* mem_width)-(0.5 * len(str))) ,
                                                        y=int(((var_x * current_base) / self.size) + ((var_x * seg_size) / self.size)/2)-10)
                current_row += 1
                current_base += temp_seg.size
            elif current_base == self.size:
                F1 = Frame(text, height=20, width=text_width, bg="red", border=5).pack(side=TOP)

                info = Label(F1, text=f"{current_base}",fg="red").place(x=0, y=var_x)  # y is current base mapped height from top of window
                break

        self.memorydraw.update()
        self.memorydraw.deiconify()

    def add_hole(self, hole_size, hole_base):
        temp_hole = Hole(hole_size, hole_base)
        self.hole_table.add_hole(temp_hole)
        self.unify_holes()

    def remove_hole(self, base):
        self.hole_table.remove_hole(base)

    def find_first_hole(self, seg_size):
        self.hole_table.order_hole_first()
        for i in range(len(self.hole_table.Holes_list)):
            if self.hole_table.Holes_list[i].size >= seg_size:
                return self.hole_table.Holes_list[i].base
        return -1

    def find_best_hole(self, seg_size):
        self.hole_table.order_hole_best()
        for i in range(len(self.hole_table.Holes_list)):
            if self.hole_table.Holes_list[i].size >= seg_size:
                return self.hole_table.Holes_list[i].base
        return -1

    def add_process(self, number_of_seg, seg_name_list, seg_size_list, seg_type_list):
        self.unify_holes()
        temp_seg_table = SegmentTable(self.process_counter)
        hole_list_temp = []
        for i in range(number_of_seg):
            if not seg_type_list[i]:
                temp_base = self.find_first_hole(seg_size_list[i])
            elif seg_type_list[i]:
                temp_base = self.find_best_hole(seg_size_list[i])

            if temp_base == -1:  # dah m3nah en manf3sh a3ml allocate

                for k in range(len(hole_list_temp)):
                    self.add_hole(hole_list_temp[k].size,hole_list_temp[k].base)

                self.unify_holes()
                return False, int(i)

            temp_seg = Segment(seg_name_list[i], seg_size_list[i], temp_base, self.process_counter, seg_type_list[i])

            hole_size = self.hole_table.remove_hole(temp_base)
            temp_hole = Hole(seg_size_list[i],temp_base)
            hole_list_temp.append(temp_hole)


            if hole_size - seg_size_list[i] > 0:
                temp_hole = Hole((hole_size - seg_size_list[i]), (temp_base + seg_size_list[i]))
                self.hole_table.add_hole(temp_hole)
            temp_seg_table.add_segment(temp_seg)
            self.unify_holes()
        self.seg_table_list.append(temp_seg_table)
        self.process_counter += 1
        return True, int(1)

    def deallocate_process(self, process_no_deallocate):
        for i in range(len(self.seg_table_list)):
            if self.seg_table_list[i].process_no == process_no_deallocate:
                print("done_deallocate")  # confirmation
                for j in range(len(self.seg_table_list[i].segment_list)):
                    temp_hole = Hole(self.seg_table_list[i].segment_list[j].size,
                                     self.seg_table_list[i].segment_list[j].base)
                    self.hole_table.add_hole(temp_hole)
                self.seg_table_list.pop(i)
                self.unify_holes()
                break

    def is_hole(self, base):
        for i in range(len(self.hole_table.Holes_list)):
            if self.hole_table.Holes_list[i].base == base:
                return True, self.hole_table.Holes_list[i].size
        return False, -1

    def is_hole_range(self,base):
        for i in range(len(self.hole_table.Holes_list)):
            if self.hole_table.Holes_list[i].base <= base <= \
                    (self.hole_table.Holes_list[i].base +
                     self.hole_table.Holes_list[i].size):
                return True
        return False

    def find_seg(self, base):
        for i in range(len(self.seg_table_list)):
            for j in range(len(self.seg_table_list[i].segment_list)):
                if self.seg_table_list[i].segment_list[j].base == base:
                    temp_segment=self.seg_table_list[i].segment_list[j]
                    return temp_segment
        temp = Segment("Error",0,0,0,0)
        return temp

    def unify_holes(self):
        initial_hole_number = len(self.hole_table.Holes_list)
        self.hole_table.order_hole_first()
        i = 0
        if initial_hole_number > 2:
            while i < initial_hole_number-1 and initial_hole_number != 2:
                if self.hole_table.Holes_list[i+1].base == (self.hole_table.Holes_list[i].base
                                                            + self.hole_table.Holes_list[i].size):
                    temp_hole = Hole((self.hole_table.Holes_list[i].size
                                      + self.hole_table.Holes_list[i+1].size), self.hole_table.Holes_list[i].base)
                    self.remove_hole(self.hole_table.Holes_list[i].base)
                    self.remove_hole(self.hole_table.Holes_list[i].base)
                    self.add_hole(temp_hole.size,temp_hole.base)
                    self.hole_table.order_hole_first()
                    initial_hole_number -= 1
                    initial_hole_number = len(self.hole_table.Holes_list)
                    if len(self.hole_table.Holes_list) <= 2:
                        break
                elif not self.hole_table.Holes_list[i+1].base == \
                         (self.hole_table.Holes_list[i].base + self.hole_table.Holes_list[i].size):
                    i += 1

        elif initial_hole_number == 2:
            if self.hole_table.Holes_list[1].base == (
                    self.hole_table.Holes_list[0].base + self.hole_table.Holes_list[0].size):
                temp_hole = Hole((self.hole_table.Holes_list[0].size + self.hole_table.Holes_list[1].size),
                                 self.hole_table.Holes_list[0].base)
                self.remove_hole(self.hole_table.Holes_list[0].base)
                self.remove_hole(self.hole_table.Holes_list[0].base)
                self.add_hole(temp_hole.size, temp_hole.base)
                self.hole_table.order_hole_first()
        if len(self.hole_table.Holes_list) == 2:
            if self.hole_table.Holes_list[1].base == (
                    self.hole_table.Holes_list[0].base + self.hole_table.Holes_list[0].size):
                temp_hole = Hole((self.hole_table.Holes_list[0].size + self.hole_table.Holes_list[1].size),
                                 self.hole_table.Holes_list[0].base)
                self.remove_hole(self.hole_table.Holes_list[0].base)
                self.remove_hole(self.hole_table.Holes_list[0].base)
                self.add_hole(temp_hole.size, temp_hole.base)
                self.hole_table.order_hole_first()

    def initialize_memory(self):
        current_base = 0
        full = True
        i = 0
        proc_segment_ini_counter = 0
        self.hole_table.order_hole_first()

        while current_base < self.size:
            if i < len(self.hole_table.Holes_list):
                if self.hole_table.Holes_list[i].base == current_base:
                    current_base += self.hole_table.Holes_list[i].size
                    i += 1
                else:
                    temp_seg = Segment("UNKNOWN", (self.hole_table.Holes_list[i].base
                                                   - current_base), current_base,
                                       proc_segment_ini_counter, 0)
                    current_base = self.hole_table.Holes_list[i].base
                    temp_seg_table = SegmentTable(proc_segment_ini_counter)
                    temp_seg_table.add_segment(temp_seg)
                    self.seg_table_list.append(temp_seg_table)
                    proc_segment_ini_counter -= 1
            else:
                temp_seg = Segment("UNKNOWN", self.size - current_base,
                                   current_base, proc_segment_ini_counter, 0)
                current_base = self.size
                temp_seg_table = SegmentTable(proc_segment_ini_counter)
                temp_seg_table.add_segment(temp_seg)
                self.seg_table_list.append(temp_seg_table)
                proc_segment_ini_counter -= 1



