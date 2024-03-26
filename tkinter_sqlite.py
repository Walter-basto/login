import customtkinter as ctk
from tkinter  import *
import sqlite3
from tkinter import messagebox

class App_db():
    def conecta_db(self):
        self.conn=sqlite3.connect("Sistema_Cadastros.db")
        self.cursor=self.conn.cursor()
        print("banco de dados conectado com sucesso")
         
    def  desconecta_db(self):
        self.conn.close()
        print("banco de dados desconectado")
    
    def cria_tabela(self):
        self.conecta_db()
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Usuarios
               (Id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email    TEXT NOT NULL,
                senha    TEXT NOT NULL,
                confirma_senha TEXT NOT NULL
               );""")
        self.conn.commit()
        print("tabela criada com sucesso")
        self.desconecta_db()
    
    def cadastrar_usuario(self):
         self.username_cadastro=self.username_frame_cadastro.get()
         self.email_cadastro=self.email_frame_cadastro.get()
         self.senha_cadastro=self.senha_frame_cadastro.get()
         self.confirma_senha_cadastro=self.confirma_senha_frame_cadastro.get()
         self.conecta_db()
         self.cursor.execute(""" INSERT INTO  Usuarios(username,email,senha,confirma_senha)
            VALUES(?,?,?,?)""",(self.username_cadastro,self.email_cadastro,self.senha_cadastro,self.confirma_senha_cadastro))
         try:
             if(self.username_cadastro =="" or self.email_cadastro =="" or self.senha_cadastro =="" or self.confirma_senha_cadastro ==""):
                messagebox.showerror(title="sistema de login",message="ERRO!!!\npor favor precisa preencher todos campos!")
             elif(len(self.username_cadastro)<4):
                   messagebox.showwarning(title="sistema de login",message="nome de usuario deve  ser pelo menos 4 caracteres")
             #elif(int(self.username_cadastro)!=self.username_cadastro):
             #   messagebox.showerror(title="sistema de login",message="não aceita numero")
             elif(len(self.senha_cadastro)<4):
                   messagebox.showwarning(title="sistema de login",message="a senha deve  ser pelo menos 4 caracteres")       
             elif(self.senha_cadastro!= self.confirma_senha_cadastro):
                  messagebox.showerror(title="sistema de login",message="ERROR!!,senhas incompativeis,por favor faça novamente")   
             
             else:
                 self.conn.commit()
                 messagebox.showinfo(title="sistema de login",message=f"parabens {self.username_cadastro},\nos seus dados foram cadastrados com sucesso!!")
                 self.frame_cadastro.place_forget()
                 self.tela_de_login()
         except:
             messagebox.showerror(title="sistema de login",message="error no processamento do seu cadastro!!, por favor tente novamente")  
             self.desconecta_db()  
             
                 
    def verifica_login(self):
         self.username_login=self.username_frame_login.get()
         self.senha_login=self.senha_frame_login.get()
         self.conecta_db()
         self.cursor.execute("""SELECT * FROM Usuarios WHERE(username = ? AND senha = ?)""",(self.username_login,self.senha_login))
         self.verifica_dados=self.cursor.fetchone()#percorrendo na tabela Usuarios
         try:
             if(self.username_login=="" or self.senha_login==""):
                messagebox.showwarning(title="sistema de login",message="ERRO!\n  ,por favor preencher todos campos")
             elif( self.username_cadastro in self.verifica_dados and self.senha_login in self.verifica_dados ):
                  messagebox.showinfo(title="Sistema de Login",message=f"parabens{self.username_login},\n login feito com sucesso!!")
                  self.conn.commit()
                  self.desconecta_db()
                  self.limpa_tela_de_login()
         except:
             messagebox.showerror(title="Sistema de Login",message="ERROR!!,Dados não encontrado no sistema\n por favor verifique se os seus dados estão correto  ou cadastre no nosso sistema")                           
             self.desconecta_db()
    
    
    
class App(ctk.CTk,App_db):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()
    #configurando a janela principal
    def  configuracoes_da_janela_inicial(self):
        self.geometry('700x400')
        self.title("Sistema de login")
        self.resizable(False,False)
        self.attributes("-alpha",0.9)
    def tela_de_login(self):
        # titulo da nossa plataforma
        self.label=ctk.CTkLabel(self,text=" seja bem vindo,\naos nossos serviços".upper(),font=("Century Gothic bold",18))
        self.label.grid(row=0,columns=1,pady=50,padx=30)
        
        # trabahando com imagem
        self.img_login=PhotoImage(file="logi-img.png")
        self.img_login_label=ctk.CTkLabel(self,text=None,image=self.img_login)
        self.img_login_label.grid(row=1,column=0,padx=25)    
       
        #criar frame do formulario login 
        self.frame_login=ctk.CTkFrame(self,width=350,height=380)
        self.frame_login.place(x=350,y=10)
        #colocando widgets dentro de frame- formulario do login
        self.label_frame_login=ctk.CTkLabel(self.frame_login,text="faça o seu login".upper(),font=("Century Gothic bold",22))
        self.label_frame_login.grid(row=0,columns=1,padx=10,pady=10)
        
        self.username_frame_login=ctk.CTkEntry(self.frame_login,width=300,placeholder_text="seu nome de usuario",font=("Century Gothic bold",16),corner_radius=20,border_color="blue")
        self.username_frame_login.grid(row=1,columns=1,padx=10,pady=10)
     
        self.senha_frame_login=ctk.CTkEntry(self.frame_login,width=300,placeholder_text="senha do usuario",font=("Century Gothic bold",16),corner_radius=20,border_color="blue",show="*")
        self.senha_frame_login.grid(row=2,columns=1,padx=10,pady=10)

        self.ver_senha=ctk.CTkButton(self.frame_login,text="clique para ver a senha",font=("Century Gothic bold",14),corner_radius=20,hover_color="green")
        self.ver_senha.grid(row=3,columns=1,padx=10,pady=10)
        
        self.btn_login=ctk.CTkButton(self.frame_login,width=300,text=" fazer login".upper(),font=("Century Gothic bold",16),corner_radius=20,hover_color="dark blue",command=self.verifica_login)
        self.btn_login.grid(row=4,columns=1,padx=10,pady=10)
      
        
        self.span=ctk.CTkLabel(self.frame_login,width=300,text="se não houver conta,\ncadastre-se no nosso sistema abaixo:".upper(),font=("Century Gothic bold",10))
        self.span.grid(row=5,columns=1,padx=10,pady=10)

        self.btn_cadastrar=ctk.CTkButton(self.frame_login,width=300,text=" fazer cadastro".upper(),font=("Century Gothic bold",16),corner_radius=20,fg_color="green",hover_color="blue",command=self.tela_de_cadastro)
        self.btn_cadastrar.grid(row=6,columns=1,padx=10,pady=10)
    
    def limpa_tela_de_login(self):
         self.username_frame_login.delete(0,END)
         self.senha_frame_login.delete(0,END)
         
         
    def tela_de_cadastro(self):
        #remover o login
         self.frame_login.place_forget()
        #criar frame do cadastro login 
         self.frame_cadastro=ctk.CTkFrame(self,width=350,height=380)
         self.frame_cadastro.place(x=350,y=10)
         #colocando widgets dentro de frame- cadastro do login
         self.label_frame_cadastro=ctk.CTkLabel(self.frame_cadastro,text="faça o seu cadastro".upper(),font=("Century Gothic bold",22))
         self.label_frame_cadastro.grid(row=0,columns=1,padx=10,pady=10)
         
         #criar wigtget da tela de cadastro
         self.username_frame_cadastro=ctk.CTkEntry(self.frame_cadastro,width=300,placeholder_text="Seu nome de usuario",font=("Century Gothic bold",16),corner_radius=20,border_color="blue")
         self.username_frame_cadastro.grid(row=1,columns=1,padx=10,pady=10)
     
         self.email_frame_cadastro=ctk.CTkEntry(self.frame_cadastro,width=300,placeholder_text="Ex:Email@gmail.com",font=("Century Gothic bold",16),corner_radius=20,border_color="blue")
         self.email_frame_cadastro.grid(row=2,columns=1,padx=10,pady=10)
         
         self.senha_frame_cadastro=ctk.CTkEntry(self.frame_cadastro,width=300,placeholder_text="senha do usuario",font=("Century Gothic bold",16),corner_radius=20,border_color="blue")
         self.senha_frame_cadastro.grid(row=3,columns=1,padx=10,pady=10)

         self.confirma_senha_frame_cadastro=ctk.CTkEntry(self.frame_cadastro,width=300,placeholder_text="Confirma a senha do usuario",font=("Century Gothic bold",16),corner_radius=20,border_color="blue")
         self.confirma_senha_frame_cadastro.grid(row=4,columns=1,padx=10,pady=10)
    
         self.btn_cadastrar_user=ctk.CTkButton(self.frame_cadastro,width=300,text=" fazer cadastro".upper(),font=("Century Gothic bold",16),corner_radius=20,hover_color="dark blue",command=self.cadastrar_usuario)
         self.btn_cadastrar_user.grid(row=6,columns=1,padx=10,pady=10)
         
         self.btn_voltalogin_frame_cadastro=ctk.CTkButton(self.frame_cadastro,width=300,text=" volta a login".upper(),font=("Century Gothic bold",16),corner_radius=20,fg_color="green",hover_color="dark blue",command=self.tela_de_login)
         self.btn_voltalogin_frame_cadastro.grid(row=7,columns=1,padx=10,pady=10)
         
    def  limpa_entry_cadastro(self):
         self.username_frame_cadastro.delete(0,END)
         self.email_frame_cadastro.delete(0,END)
         self.senha_frame_cadastro.delete(0,END)
         self.confirma_senha_frame_cadastro.delete(0,END)

if __name__=="__main__":
    app=App()
    app.mainloop()    
