from token_bucket import TokenBucket
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import scrolledtext



def btn_empezar():
    tb.set_pattern(my_pattern)
    tb.mode = radio_var.get()
    tb.begin()

    #Paquetes enviados
    x = []
    y = []

    #Cubo
    ycubo = []
    dis_delayed = []
    totalins = []
    cubo2 = []

    for r in tb.result:
        y.append(r[0])
        ycubo.append(r[2])
        dis_delayed.append(r[1])
        totalins.append(r[3])

        if tb.mode == 3:
            cubo2.append(r[5])

    x = range(0,len(y))
   
    if tb.mode != 3:
        fig, (sub1, sub2, sub3, sub4) = plt.subplots(4,gridspec_kw={'hspace': 0.7})
    else:
        fig, (sub1, sub2, sub3, sub4, sub5) = plt.subplots(5,gridspec_kw={'hspace': 0.8})

    sub1.plot(x,totalins)
    sub2.plot(x,y)
    sub3.plot(x,ycubo)
    sub4.scatter(x,dis_delayed)

    if tb.mode == 3:
        sub5.plot(x,cubo2)
    

    sub1.set_title("Paquetes enviados")
    sub1.set(xlabel="Segundos", ylabel = "Bytes")
    sub2.set_title("Paquetes reenviados")
    sub2.set(xlabel="Segundos", ylabel = "Bytes")
    sub3.set_title("Cubo")
    sub3.set(xlabel="Segundos", ylabel = "Tokens")
    sub4.set_title("Descartados/Retrasados")
    sub4.set(xlabel="Segundos", ylabel = "Bytes")
    if tb.mode == 3:
        sub5.set_title("Cubo2")
        sub5.set(xlabel="Segundos", ylabel = "Tokens")

    plt.show()

def btn_limpiar():
    scrolled_text.configure(state = 'normal')
    scrolled_text.delete(1.0,END)
    scrolled_text.configure(state = 'disabled') 
  
    global my_pattern
    my_pattern = []
    tb.set_pattern(my_pattern)

def btn_aniadir():
    n = int(en_n.get())
    t = int(en_t.get())

    my_pattern.append( (n,t) )
    scrolled_text.configure(state = 'normal')

    scrolled_text.insert('insert', '[*]  ' + str(n) + ' Paquetes de ' + str(t) + ' bytes' + '\n')
    scrolled_text.configure(state = 'disabled')    

if __name__ == '__main__':
    tb = TokenBucket()
    #tb.set_pattern([(800,8),(600,28),(500,6),(500,25),(2000,8),(400,25)])
    my_pattern = []

    window = Tk()
    window.title("Token Bucket")
    window.geometry('1000x400')

    numero_de_paquetes = 0
    radio_var = IntVar()

    btn = Button(window, text="Empezar",command=btn_empezar)
    btn.grid(column=90, row=90)
    
    lbl_aue = Label(window, text="Añade un elemento:", font='Helvetica 18 bold',pady=7, padx=7)
    lbl_aue.grid(column=5, row=10)

    lbl_p = Label(window, text="Numero")
    lbl_p.grid(column=5, row=11)
    lbl_n = Label(window, text="Tamaño")
    lbl_n.grid(column=5, row=12)

    btn = Button(window, text="Añadir",command=btn_aniadir)
    btn.grid(column=5, row=13)

    btn2 = Button(window, text="Limpiar",command=btn_limpiar)
    btn2.grid(column=6, row=13)

    en_n = Entry(window,width=10)
    en_n.grid(column=6,row=11)

    en_t = Entry(window,width=10)
    en_t.grid(column=6,row=12)

    rad1 = Radiobutton(window,text='Policing',value=1,variable=radio_var)
    rad2 = Radiobutton(window,text='Shaping',value=2,variable=radio_var)
    rad3 = Radiobutton(window,text="Dual Bucket",value=3,variable=radio_var)

    rad1.invoke()

    rad1.grid(column=25, row=10)
    rad2.grid(column=25, row=11)
    rad3.grid(column=25, row=12)

    scrolled_text = scrolledtext.ScrolledText(window,width=50,height=10)
    scrolled_text.grid(column=7, row=40)
    scrolled_text.configure(state = 'disabled')
    

    window.mainloop()

