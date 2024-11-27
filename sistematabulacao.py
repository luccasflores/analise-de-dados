import customtkinter as ctk
from tkinter import *
from tkinter import messagebox, filedialog, ttk
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin.exceptions import FirebaseError
import sys
import os
import tkinter as tk
import os
import sys
from firebase_admin import auth as admin_auth
import matplotlib.pyplot as plt
import threading
import time
import pyperclip
from datetime import datetime
import pandas as pd
from PIL import Image as PilImage, ImageTk
from datetime import datetime
import urllib.parse
import os
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from tkinter import messagebox
import os
from email.mime.application import MIMEApplication
from firebase_admin import auth
import pyrebase



import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

config = {
    "apiKey": "YOUR_APIKEY",
    "authDomain": "YOUR-AUTH",
    "databaseURL": "YOUR-URL",
    "projectId": "mehsolucoes",
    "storageBucket": "mehsolucoes.appspot.com",
    "messagingSenderId": "SEU_MESSAGING_SENDER_ID",
    "appId": "YOUR_APPID",
    "measurementId": "SEU_MEASUREMENT_ID"
}




usuarios = {
    "email@email.com": {"smtp_server": "smtp.servidor.com", "smtp_port": 587, "smtp_user": "email@email.com", "smtp_password": "senha", "nome": "Carol", "assinatura": "assinaturacarol.png"},
}
# Credenciais Firebase
credenciais = {
    "apiKey": "YOUR_APIKEY",
    "authDomain": "YOUR-AUTH",
    "databaseURL": "YOUR-URL",
    "projectId": "mehsolucoes",
    "storageBucket": "mehsolucoes.appspot.com",
    "messagingSenderId": "SEU_MESSAGING_SENDER_ID",
    "appId": "YOUR_APPID",
    "measurementId": "SEU_MEASUREMENT_ID"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
# Inicializar Firebase
cred = credentials.Certificate(credenciais)
firebase_admin.initialize_app(cred)
db = firestore.client()

class Application:
    def __init__(self):
        self.janela = ctk.CTk()
        self.tema()
        self.tela()
        self.imagem()
        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')
        self.tela_login()
        self.janela.mainloop()

    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.primary_color = "#804bb5"
        self.janela.configure(bg=self.primary_color)

    def tela(self):
        self.janela.attributes('-topmost', True)
        self.janela.title("M&H Soluções")
        # Remova a linha abaixo para evitar o erro de bitmap
        # self.janela.iconbitmap("icone.ico")

    def imagem(self):
        def update_image(event=None):
            window_width = self.janela.winfo_width()
            window_height = self.janela.winfo_height()

            # Carregue a imagem como ícone
            icon = PilImage.open(resource_path("icone.png"))
            icon = ImageTk.PhotoImage(icon)
            self.janela.tk.call('wm', 'iconphoto', self.janela._w, icon)

            img = PilImage.open(resource_path('icone.png'))
            aspect_ratio = img.width / img.height
            new_width = window_width // 2
            new_height = int(new_width / aspect_ratio)

            img = img.resize((new_width, new_height), PilImage.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            label_img.configure(image=img_tk)
            label_img.image = img_tk  # Manter a referência à imagem

        label_img = ctk.CTkLabel(master=self.janela, text=None)
        label_img.place(x=5, y=15)

        self.janela.bind('<Configure>', update_image)
        update_image()


    def tela_login(self):
        if hasattr(self, 'frame'):
            self.frame.pack_forget()

        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        label = ctk.CTkLabel(master=self.frame, text="Bem-vindo à M&H Tabula!", font=('Horizon', 20, 'bold'),
                             text_color='white')
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky='w')

        self.entry1 = ctk.CTkEntry(master=self.frame, placeholder_text="Digite seu E-mail", width=300,
                                   font=("Horizon", 14))
        self.entry1.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky='w')

        label1 = ctk.CTkLabel(master=self.frame, text="Campo de caráter obrigatório", text_color="#804bb5",
                              font=("Horizon", 14))
        label1.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky='w')

        self.entry2 = ctk.CTkEntry(master=self.frame, placeholder_text="Senha do Usuário", width=300,
                                   font=("Horizon", 14), show='*')
        self.entry2.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky='w')

        label2 = ctk.CTkLabel(master=self.frame, text="Campo de caráter obrigatório", text_color="#804bb5",
                              font=("Horizon", 14))
        label2.grid(row=4, column=0, columnspan=2, padx=20, pady=5, sticky='w')

        self.checkbox = ctk.CTkCheckBox(master=self.frame, text="Lembrar de mim sempre")
        self.checkbox.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky='w')

        button = ctk.CTkButton(master=self.frame, text="Login", width=100, hover_color='#804bb5', fg_color='#804bb5',
                               command=self.login_efetuado)
        button.grid(row=6, column=0, columnspan=2, padx=20, pady=10)

    def login_efetuado(self):
        email = self.entry1.get()
        senha = self.entry2.get()

        try:
            # Autentica o usuário com email e senha
            user = auth.sign_in_with_email_and_password(email, senha)
            self.user_id = user['localId']  # ID do usuário autenticado
            self.email = email

            self.frame.pack_forget()

            if email == "luccasflores@mehsolucoes.com":
                self.tela_master()
            else:
                self.tela_principal()  # Certifique-se que este método está implementado corretamente

        except Exception as e:
            messagebox.showerror(title="Erro de login", message=f"Erro ao autenticar usuário, confira o login e senha.")

    def tela_principal(self):
        login_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        login_frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        label = ctk.CTkLabel(master=login_frame, text="Lista de Empresas", font=('Horizon', 20, 'bold'),
                             text_color='white')
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky='w')

        self.button_empresas = ctk.CTkButton(master=login_frame, text="Campanha", width=100, hover_color='#804bb5',
                                             fg_color='#804bb5', command=self.tela_empresas)
        self.button_empresas.grid(row=1, column=0, padx=20, pady=10)

        self.button_empresas2 = ctk.CTkButton(master=login_frame, text="Misto", width=100, hover_color='#804bb5',
                                              fg_color='#804bb5', command=self.tela_empresas2)
        self.button_empresas2.grid(row=2, column=0, padx=20, pady=10)

        self.button_personalizado = ctk.CTkButton(master=login_frame, text="Personalizado", width=100,
                                                  hover_color='#804bb5',
                                                  fg_color='#804bb5', command=self.tela_personalizado)
        self.button_personalizado.grid(row=3, column=0, padx=20, pady=10)

        button_wpp4 = ctk.CTkButton(master=login_frame, text="Deslogar", width=100, hover_color='#3984cf',
                                    fg_color='#3984cf', command=self.logout_usuario)
        button_wpp4.grid(row=4, column=0, padx=20, pady=10)

    def tela_personalizado(self):
        self.frame.pack_forget()
        nova_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        nova_frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        self.label_banco = ctk.CTkLabel(master=nova_frame, text="", font=('Horizon', 14))
        self.label_banco.grid(row=0, column=0, padx=20, pady=(20, 10), sticky='w')

        self.index_cliente = 0
        self.carregar_cliente_personalizado()

    def carregar_cliente_personalizado(self):
        try:
            colecao_ref = db.collection(f'{self.email}_personalizado')  # Coleção personalizada
            docs = colecao_ref.stream()
            self.clientes = [{'id': doc.id, **doc.to_dict()} for doc in docs]

            if self.clientes:
                self.mostrar_cliente_personalizado(self.clientes[self.index_cliente])
            else:
                self.label_banco.configure(text="Nenhum cliente encontrado.")
        except Exception as e:
            print(f"Erro ao carregar cliente: {e}")

    def mostrar_cliente_personalizado(self, cliente):
        if not self.label_banco.winfo_exists():
            return

        # Limpar o conteúdo anterior
        for widget in self.label_banco.winfo_children():
            widget.destroy()

        # Exibir o nome da empresa como título e permitir cópia ao clicar
        nome_empresa = cliente.get('Nome da Empresa', 'N/A')
        nome_label = ctk.CTkLabel(self.label_banco, text=nome_empresa, font=('Horizon', 18, 'bold'), text_color='white')
        nome_label.grid(sticky="w", padx=5, pady=(0, 10))
        nome_label.bind("<Button-1>", lambda e, text=nome_empresa: self.copiar_para_area_de_transferencia(text))

        # Exibir outras informações do cliente e permitir cópia ao clicar
        info = {
            "CNPJ": cliente.get('CNPJ', 'N/A'),
            "Email": cliente.get('Email', 'N/A'),
            "Telefone": cliente.get('Telefone', 'N/A'),
            "Data de Início": cliente.get('Data de inicio', 'N/A'),
            "Estado": cliente.get('Estado', 'N/A')
        }

        for key, value in info.items():
            label = ctk.CTkLabel(self.label_banco, text=f"{key}: {value}", text_color="white", anchor="w")
            label.grid(sticky="w", padx=5, pady=(0, 2))
            label.bind("<Button-1>", lambda e, text=value: self.copiar_para_area_de_transferencia(text))

        # Adicionar o combobox para selecionar a opção de tabulação
        texto_selecao = ctk.CTkLabel(self.label_banco, text="Selecione uma Opção:", font=('Horizon', 14),
                                     text_color='white')
        texto_selecao.grid(sticky="w", padx=5, pady=(10, 5))

        self.select_var = StringVar()
        self.select_box = ttk.Combobox(self.label_banco, textvariable=self.select_var, width=30)
        self.select_box['values'] = (
            "Ligação + Whatsapp", "Apenas Ligação", "Sem Telefone Cadastrado", "Sem Interesse",
            "Negociação em Andamento", "Cliente Fechado", "Só Whatsapp", "Email enviado", "Email + Whatsapp"
        )
        self.select_box['state'] = 'readonly'
        self.select_box.grid(sticky="w", padx=10, pady=(0, 10))
        self.select_box.bind("<<ComboboxSelected>>", self.habilitar_proximo)

        # Adicionar os botões "Próximo", "Limpar", "Whatsapp" e "Email" abaixo do selectbox
        button_frame = ctk.CTkFrame(self.label_banco)
        button_frame.grid(sticky="w", padx=10, pady=(10, 0))

        self.proximo_button = ctk.CTkButton(button_frame, text="Próximo", width=100, hover_color='#804bb5',
                                            fg_color='#804bb5', command=self.proximo_cliente_personalizado)
        self.proximo_button.grid(row=0, column=0, padx=5, pady=5)
        self.proximo_button.configure(state="disabled")

        self.limpar_button = ctk.CTkButton(button_frame, text="Limpar", width=100, hover_color='#9a7d61',
                                           fg_color='#9a7d61', command=self.limpar_informacoes)
        self.limpar_button.grid(row=0, column=1, padx=5, pady=5)

        self.whatsapp_button = ctk.CTkButton(button_frame, text="Whatsapp", width=100, hover_color='#804bb5',
                                             fg_color='#804bb5', command=self.enviar_whatsapp_personalizado)
        self.whatsapp_button.grid(row=1, column=0, padx=5, pady=10)

        self.email_button = ctk.CTkButton(button_frame, text="Email", width=100, hover_color='#804bb5',
                                          fg_color='#804bb5', command=self.enviar_email_personalizado)
        self.email_button.grid(row=1, column=1, padx=5, pady=10)

        self.telefone_button = ctk.CTkButton(button_frame, text="Ligar", width=100, hover_color='#804bb5',
                                             fg_color='#804bb5', command=self.fazer_ligacao_personalizado)
        self.telefone_button.grid(row=1, column=2, padx=5, pady=10)

    def proximo_cliente_personalizado(self):
        cliente_atual = self.clientes[self.index_cliente]
        tabulacao_selecionada = self.select_var.get()

        if tabulacao_selecionada:
            try:
                # Adicionando dados de tabulação na coleção "tabulados"
                dados_tabulados = {
                    "Nome da Empresa": cliente_atual.get('Nome da Empresa', 'N/A'),
                    "CNPJ": cliente_atual.get('CNPJ', 'N/A'),
                    "Email": cliente_atual.get('Email', 'N/A'),
                    "Telefone": cliente_atual.get('Telefone', 'N/A'),
                    "Data de Início": cliente_atual.get('Data de inicio', 'N/A'),
                    "Estado": cliente_atual.get('Estado', 'N/A'),
                    "Tabulação": tabulacao_selecionada,
                    "Usuário": self.email,  # Adiciona o e-mail do usuário que tabulou
                    "Data da Tabulação": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # Adiciona a data e hora da tabulação
                }

                # Enviar para a coleção "tabulados"
                db.collection('tabulados').add(dados_tabulados)
                messagebox.showinfo("Sucesso", "Dados tabulados com sucesso!")

                # Verificar e excluir o documento da coleção personalizada após a tabulação
                if 'id' in cliente_atual:
                    try:
                        # Excluindo o documento do Firebase
                        db.collection(f'{self.email}_personalizado').document(cliente_atual['id']).delete()
                        print(
                            f"Documento {cliente_atual['id']} excluído com sucesso da coleção {self.email}_personalizado.")
                    except Exception as e:
                        print(f"Erro ao excluir o documento {cliente_atual['id']}: {str(e)}")
                else:
                    print("Erro: ID do documento não encontrado.")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar tabulação: {str(e)}")

        self.index_cliente = (self.index_cliente + 1) % len(self.clientes)
        self.mostrar_cliente_personalizado(self.clientes[self.index_cliente])

    def enviar_email_personalizado(self):
        cliente_atual = self.clientes[self.index_cliente]
        destinatario = cliente_atual.get('Email', '')

        if not destinatario:
            messagebox.showwarning("Aviso", "Email não disponível para o cliente atual.")
            return

        # Obter dados do usuário autenticado
        usuario_atual = usuarios.get(self.email)

        if not usuario_atual:
            messagebox.showerror("Erro", "Usuário não encontrado para envio de e-mail.")
            return

        smtp_server = usuario_atual["smtp_server"]
        smtp_port = usuario_atual["smtp_port"]
        smtp_user = usuario_atual["smtp_user"]
        smtp_password = usuario_atual["smtp_password"]
        nome_usuario = usuario_atual["nome"]
        assinatura = usuario_atual["assinatura"]

        # Corpo do email com conteúdo HTML personalizado
        # Corpo do email com conteúdo HTML personalizado
        corpo_email = f"""
                <!DOCTYPE html>
                <html lang="pt-BR">
                <head>
                  <meta charset="UTF-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <title>Olá,</title>
                </head>
                <body>
                  <table align="center" width="600" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; border-collapse: collapse;">
                    <tr>
                      <td style="padding: 20px 0; text-align: center; background-color: #8c52ff;">
                        <img src="cid:logo" alt="M&H Soluções" style="max-width: 100%; height: auto; width: 200px;">
                      </td>
                    </tr>
                    <tr>
                      <td style="padding: 20px; text-align: left;">
                        <p>Boa tarde,</p>
                        <p>Sou {nome_usuario} da <strong>M&amp;H Soluções</strong>, e temos uma grande novidade para compartilhar com você.</p>
                        <p>A M&H Soluções agora está em parceria com a <strong>Pontocom Gráfica</strong> (antiga COOPTEI), uma especialista renomada em impressão de campanhas eleitorais. Estamos unindo forças para oferecer a você não apenas serviços digitais de alta qualidade, mas também soluções completas de impressão para suas campanhas.</p>
                        <p>Com essa parceria, você pode contar com uma gama completa de serviços que vão desde o desenvolvimento e gestão de campanhas digitais até a impressão de materiais eleitorais de alta qualidade, garantindo a melhor apresentação possível para suas campanhas.</p>
                        <p>Gostaríamos de convidá-lo a solicitar um orçamento e conhecer mais sobre como podemos ajudar a impulsionar suas campanhas com nossas soluções integradas.</p>
                        <p>Para mais informações, visite nosso site em <a href="http://mehsolucoes.com" target="_blank" style="color: #8c52ff; text-decoration: none;">mehsolucoes.com</a> ou responda a este e-mail. Estamos à disposição para ajudá-lo a escolher as melhores opções para suas necessidades.</p>

                        <p>Atenciosamente,</p>
                        <p><img src="cid:assinatura" alt="Assinatura" style="width: 600px; height: 300px;"></p>
                      </td>
                    </tr>
                  </table>
                </body>
                </html>
                """

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.set_debuglevel(1)

            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = destinatario
            msg['Subject'] = "Vamos conversar sobre sua campanha?"

            # Adicionando o corpo do email
            msg.attach(MIMEText(corpo_email, 'html'))

            # Anexando a imagem da logo
            with open(resource_path("logo.png"), 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<logo>')
                img.add_header('Content-Disposition', 'inline', filename='logo.png')
                msg.attach(img)

            # Anexando a assinatura
            with open(resource_path(assinatura), 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<assinatura>')
                img.add_header('Content-Disposition', 'inline', filename=assinatura)
                msg.attach(img)

            # Anexando o PDF da apresentação
            with open(resource_path("Apresentacao.pdf"), 'rb') as pdf_file:
                pdf = MIMEApplication(pdf_file.read())
                pdf.add_header('Content-Disposition', 'attachment', filename="Apresentacao.pdf")
                msg.attach(pdf)

            server.sendmail(smtp_user, destinatario, msg.as_string())
            server.quit()
            messagebox.showinfo("Sucesso", f"Email enviado para {destinatario}")
        except Exception as e:
            messagebox.showerror("Erro", f'Erro ao enviar email para {destinatario}: {str(e)}')
    def fazer_ligacao_personalizado(self):
        cliente_atual = self.clientes[self.index_cliente]
        telefone = cliente_atual.get('Telefone', '')

        if not telefone:
            messagebox.showwarning("Aviso", "Telefone não disponível para o cliente atual.")
            return

        # Preparar mensagem de ligação
        mensagem = f"Você está prestes a fazer uma ligação para o cliente: {cliente_atual.get('Nome', '')} com o número: {telefone}."
        if messagebox.askyesno("Confirmar Ligação", mensagem):
            try:
                # Aqui, você pode integrar a funcionalidade de chamada real se disponível
                # Exemplo: usar uma API de telefonia ou apenas fazer uma simulação
                print(f"Realizando ligação para {telefone}")
                messagebox.showinfo("Sucesso", f"Ligação iniciada para {telefone}")
            except Exception as e:
                messagebox.showerror("Erro", f'Erro ao iniciar a ligação para {telefone}: {str(e)}')

    def enviar_whatsapp_personalizado(self):
        # Mapeamento de e-mails para nomes
        usuarios = {
            "email@email.com": "Carol",

        }

        # Obter o nome do usuário autenticado
        nome_usuario = usuarios.get(self.email, "M&H Soluções")

        cliente_atual = self.clientes[self.index_cliente]
        telefone = cliente_atual.get('Telefone', '')
        telefone = str(telefone).replace(' ', '').replace('-', '')
        mensagem = f"Olá! Sou {nome_usuario} da M&H Soluções. Podemos conversar?"

        if telefone:
            url = f"https://web.whatsapp.com/send?phone=55{telefone}&text={urllib.parse.quote(mensagem)}"
            os.system(f'start {url}')  # Isso abre o link no navegador padrão
        else:
            messagebox.showwarning("Aviso", "Telefone não disponível para o cliente atual.")

    def tela_empresas2(self):
        self.frame.pack_forget()
        nova_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        nova_frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        self.label_banco = ctk.CTkLabel(master=nova_frame, text="", font=('Horizon', 14))
        self.label_banco.grid(row=0, column=0, padx=20, pady=(20, 10), sticky='w')

        self.index_cliente = 0
        self.carregar_cliente2()

    def carregar_cliente2(self):
        try:
            colecao_ref = db.collection(f'{self.email}_empresas2')  # Alteração no nome da coleção
            docs = colecao_ref.stream()
            self.clientes = [{'id': doc.id, **doc.to_dict()} for doc in docs]

            if self.clientes:
                self.mostrar_cliente2(self.clientes[self.index_cliente])
            else:
                self.label_banco.configure(text="Nenhum cliente encontrado.")
        except Exception as e:
            print(f"Erro ao carregar cliente: {e}")

    def mostrar_cliente2(self, cliente):
        if not self.label_banco.winfo_exists():
            return

        # Limpar o conteúdo anterior
        for widget in self.label_banco.winfo_children():
            widget.destroy()

        # Exibir o nome da empresa como título e permitir cópia ao clicar
        nome_empresa = cliente.get('Nome da Empresa', 'N/A')
        nome_label = ctk.CTkLabel(self.label_banco, text=nome_empresa, font=('Horizon', 18, 'bold'), text_color='white')
        nome_label.grid(sticky="w", padx=5, pady=(0, 10))
        nome_label.bind("<Button-1>", lambda e, text=nome_empresa: self.copiar_para_area_de_transferencia(text))

        # Exibir outras informações do cliente e permitir cópia ao clicar
        info = {
            "CNPJ": cliente.get('CNPJ', 'N/A'),
            "Email": cliente.get('Email', 'N/A'),
            "Telefone": cliente.get('Telefone', 'N/A'),
            "Data de Início": cliente.get('Data de inicio', 'N/A'),
            "Estado": cliente.get('Estado', 'N/A')
        }

        for key, value in info.items():
            label = ctk.CTkLabel(self.label_banco, text=f"{key}: {value}", text_color="white", anchor="w")
            label.grid(sticky="w", padx=5, pady=(0, 2))
            label.bind("<Button-1>", lambda e, text=value: self.copiar_para_area_de_transferencia(text))

        # Adicionar o combobox para selecionar a opção de tabulação
        texto_selecao = ctk.CTkLabel(self.label_banco, text="Selecione uma Opção:", font=('Horizon', 14),
                                     text_color='white')
        texto_selecao.grid(sticky="w", padx=5, pady=(10, 5))

        self.select_var = StringVar()
        self.select_box = ttk.Combobox(self.label_banco, textvariable=self.select_var, width=30)
        self.select_box['values'] = (
            "Ligação + Whatsapp", "Apenas Ligação", "Sem Telefone Cadastrado", "Sem Interesse",
            "Negociação em Andamento", "Cliente Fechado", "Só Whatsapp", "Email enviado", "Email + Whatsapp"
        )
        self.select_box['state'] = 'readonly'
        self.select_box.grid(sticky="w", padx=10, pady=(0, 10))
        self.select_box.bind("<<ComboboxSelected>>", self.habilitar_proximo)

        button_frame = ctk.CTkFrame(self.label_banco)
        button_frame.grid(sticky="w", padx=10, pady=(10, 0))

        self.proximo_button = ctk.CTkButton(button_frame, text="Próximo", width=100, hover_color='#804bb5',
                                            fg_color='#804bb5', command=self.proximo_cliente2)
        self.proximo_button.grid(row=0, column=0, padx=5, pady=5)
        self.proximo_button.configure(state="disabled")

        self.limpar_button = ctk.CTkButton(button_frame, text="Limpar", width=100, hover_color='#9a7d61',
                                           fg_color='#9a7d61', command=self.limpar_informacoes)
        self.limpar_button.grid(row=0, column=1, padx=5, pady=5)

        self.whatsapp_button = ctk.CTkButton(button_frame, text="Whatsapp", width=100, hover_color='#804bb5',
                                             fg_color='#804bb5', command=self.enviar_whatsapp2)
        self.whatsapp_button.grid(row=1, column=0, padx=5, pady=10)

        self.email_button = ctk.CTkButton(button_frame, text="Email", width=100, hover_color='#804bb5',
                                          fg_color='#804bb5', command=self.enviar_email2)
        self.email_button.grid(row=1, column=1, padx=5, pady=10)

    def proximo_cliente2(self):
        cliente_atual = self.clientes[self.index_cliente]
        self.index_cliente = (self.index_cliente + 1) % len(self.clientes)
        self.mostrar_cliente2(self.clientes[self.index_cliente])

    def enviar_whatsapp2(self):
        # Mapeamento de e-mails para nomes
        usuarios = {
            "email@email.com": "Carol",
        }

        # Obter o nome do usuário autenticado
        nome_usuario = usuarios.get(self.email, "M&H Soluções")

        cliente_atual = self.clientes[self.index_cliente]
        telefone = cliente_atual.get('Telefone', '')
        telefone = str(telefone).replace(' ', '').replace('-', '')
        mensagem = f"Olá! Sou {nome_usuario} da M&H Soluções. Podemos conversar?"

        if telefone:
            url = f"https://web.whatsapp.com/send?phone=55{telefone}&text={urllib.parse.quote(mensagem)}"
            os.system(f'start {url}')  # Isso abre o link no navegador padrão
        else:
            messagebox.showwarning("Aviso", "Telefone não disponível para o cliente atual.")

    def enviar_email2(self):
        cliente_atual = self.clientes[self.index_cliente]
        destinatario = cliente_atual.get('Email', '')

        if not destinatario:
            messagebox.showwarning("Aviso", "Email não disponível para o cliente atual.")
            return

        # Obter dados do usuário autenticado
        usuario_atual = usuarios.get(self.email)

        if not usuario_atual:
            messagebox.showerror("Erro", "Usuário não encontrado para envio de e-mail.")
            return

        smtp_server = usuario_atual["smtp_server"]
        smtp_port = usuario_atual["smtp_port"]
        smtp_user = usuario_atual["smtp_user"]
        smtp_password = usuario_atual["smtp_password"]
        nome_usuario = usuario_atual["nome"]
        assinatura = usuario_atual["assinatura"]

        # Corpo do email com conteúdo HTML personalizado
        corpo_email = f"""
                <!DOCTYPE html>
                <html lang="pt-BR">
                <head>
                  <meta charset="UTF-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <title>Olá,</title>
                </head>
                <body>
                  <table align="center" width="600" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; border-collapse: collapse;">
                    <tr>
                      <td style="padding: 20px 0; text-align: center; background-color: #8c52ff;">
                        <img src="cid:logo" alt="M&H Soluções" style="max-width: 100%; height: auto; width: 200px;">
                      </td>
                    </tr>
                    <tr>
                      <td style="padding: 20px; text-align: left;">
                        <p>Boa tarde,</p>
                        <p>Sou {nome_usuario} da <strong>M&amp;H Soluções</strong>, e temos uma grande novidade para compartilhar com você.</p>
                        <p>A M&H Soluções agora está em parceria com a <strong>Pontocom Gráfica</strong> (antiga COOPTEI), uma especialista renomada em impressão de campanhas eleitorais. Estamos unindo forças para oferecer a você não apenas serviços digitais de alta qualidade, mas também soluções completas de impressão para suas campanhas.</p>
                        <p>Com essa parceria, você pode contar com uma gama completa de serviços que vão desde o desenvolvimento e gestão de campanhas digitais até a impressão de materiais eleitorais de alta qualidade, garantindo a melhor apresentação possível para suas campanhas.</p>
                        <p>Gostaríamos de convidá-lo a solicitar um orçamento e conhecer mais sobre como podemos ajudar a impulsionar suas campanhas com nossas soluções integradas.</p>
                        <p>Para mais informações, visite nosso site em <a href="http://mehsolucoes.com" target="_blank" style="color: #8c52ff; text-decoration: none;">mehsolucoes.com</a> ou responda a este e-mail. Estamos à disposição para ajudá-lo a escolher as melhores opções para suas necessidades.</p>

                        <p>Atenciosamente,</p>
                        <p><img src="cid:assinatura" alt="Assinatura" style="width: 600px; height: 300px;"></p>
                      </td>
                    </tr>
                  </table>
                </body>
                </html>
                """
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.set_debuglevel(1)

            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = destinatario
            msg['Subject'] = "Vamos agendar uma conversa sobre sua campanha?"

            # Adicionando o corpo do email
            msg.attach(MIMEText(corpo_email, 'html'))

            # Anexando a imagem da logo
            with open(resource_path("logo.png"), 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<logo>')
                img.add_header('Content-Disposition', 'inline', filename='logo.png')
                msg.attach(img)

            # Anexando a assinatura
            with open(resource_path(assinatura), 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<assinatura>')
                img.add_header('Content-Disposition', 'inline', filename=assinatura)
                msg.attach(img)

            server.sendmail(smtp_user, destinatario, msg.as_string())
            server.quit()
            messagebox.showinfo("Sucesso", f"Email enviado para {destinatario}")
        except Exception as e:
            messagebox.showerror("Erro", f'Erro ao enviar email para {destinatario}: {str(e)}')

    def tela_empresas(self):
        self.frame.pack_forget()
        nova_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        nova_frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        self.label_banco = ctk.CTkLabel(master=nova_frame, text="", font=('Horizon', 14))
        self.label_banco.grid(row=0, column=0, padx=20, pady=(20, 10), sticky='w')

        self.index_cliente = 0
        self.carregar_cliente()

    def mostrar_tela_limpeza(self):
        if hasattr(self, 'frame') and self.frame:
            self.frame.pack_forget()  # Ocultar o frame atual

        # Recriar o frame para evitar conflitos
        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        # Centralizar a grid
        self.frame.grid_columnconfigure(0, weight=1)

        # Adicionar label centralizado
        label = ctk.CTkLabel(master=self.frame, text="Selecione a Ação de Limpeza", font=('Horizon', 20, 'bold'))
        label.grid(row=0, column=0, padx=20, pady=20, sticky='n')

        # Botões de limpeza
        btn_limpar_campanha = ctk.CTkButton(master=self.frame, text="Limpar Campanha", hover_color='#804bb5',
                                            fg_color='#804bb5', command=self.limpar_campanha)
        btn_limpar_campanha.grid(row=1, column=0, padx=20, pady=10, sticky='n')

        btn_limpar_misto = ctk.CTkButton(master=self.frame, text="Limpar Misto", hover_color='#804bb5',
                                         fg_color='#804bb5', command=self.limpar_misto)
        btn_limpar_misto.grid(row=2, column=0, padx=20, pady=10, sticky='n')

        # Select box para selecionar usuário
        label_usuario = ctk.CTkLabel(master=self.frame, text="Selecione o usuário para Limpar Personalizado",
                                     font=('Horizon', 14))
        label_usuario.grid(row=3, column=0, padx=20, pady=(20, 10), sticky='n')

        usuarios_list = [user.email for user in firebase_admin.auth.list_users().iterate_all()]
        self.select_usuario_var = StringVar()
        self.select_usuario_box = ttk.Combobox(self.frame, textvariable=self.select_usuario_var, values=usuarios_list,
                                               state='readonly')
        self.select_usuario_box.grid(row=4, column=0, padx=20, pady=10, sticky='n')

        btn_limpar_personalizado = ctk.CTkButton(master=self.frame, text="Limpar Personalizado", hover_color='#804bb5',
                                                 fg_color='#804bb5', command=self.limpar_personalizado)
        btn_limpar_personalizado.grid(row=5, column=0, padx=20, pady=10, sticky='n')

        # Botão para "Limpar" a tela atual
        btn_limpar_tela = ctk.CTkButton(master=self.frame, text="Limpar Tela", hover_color='#804bb5',
                                        fg_color='#804bb5', command=self.limpar_tela)
        btn_limpar_tela.grid(row=6, column=0, padx=20, pady=10, sticky='n')

        self.progress_bar = ctk.CTkProgressBar(master=self.frame)
        self.progress_bar.grid(row=7, column=0, padx=20, pady=10)
        self.progress_bar.grid_remove()  # Ocultar a barra inicialmente

    def limpar_campanha(self):
        self.limpar_dados('_empresas')

    def limpar_misto(self):
        self.limpar_dados('_empresas2')

    def limpar_personalizado(self):
        usuario_selecionado = self.select_usuario_var.get()
        if usuario_selecionado:
            self.limpar_dados(f'{usuario_selecionado}_personalizado')
        else:
            messagebox.showerror("Erro", "Por favor, selecione um usuário.")

    def limpar_dados(self, colecao_sufixo):
        try:
            self.progress_bar.grid(row=0, column=0, pady=10, sticky="ew")  # Usando grid ao invés de pack
            self.progress_bar.set(0)

            # Contar total de documentos
            total_docs = sum(1 for _ in db.collection(colecao_sufixo).stream())

            if total_docs == 0:
                messagebox.showinfo("Informação", "Nenhum dado encontrado para limpar.")
                self.progress_bar.grid_forget()  # Usando grid_forget ao invés de pack_forget
                return

            processed_docs = 0

            # Processar a limpeza
            for doc in db.collection(colecao_sufixo).stream():
                db.collection(colecao_sufixo).document(doc.id).delete()
                processed_docs += 1
                self.progress_bar.set(processed_docs / total_docs)

            messagebox.showinfo("Sucesso", f"Dados de {colecao_sufixo} limpos com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar banco de dados: {str(e)}")
        finally:
            self.progress_bar.grid_forget()  # Usando grid_forget ao invés de pack_forget

    def tela_master(self):
        master_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        master_frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        label = ctk.CTkLabel(master=master_frame, text="M&H Master", font=('Horizon', 20, 'bold'),
                             text_color='white')
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky='w')

        btn_inserir_empresas = ctk.CTkButton(master=master_frame, text="Inserir Lead Campanha", width=150,
                                             hover_color='#804bb5', fg_color='#804bb5',
                                             command=self.mostrar_upload_empresas)
        btn_inserir_empresas.grid(row=1, column=0, padx=20, pady=10)

        btn_inserir_empresas2 = ctk.CTkButton(master=master_frame, text="Inserir Lead Misto", width=150,
                                              hover_color='#804bb5', fg_color='#804bb5',
                                              command=self.mostrar_upload_empresas2)
        btn_inserir_empresas2.grid(row=2, column=0, padx=20, pady=10)

        btn_inserir_personalizado = ctk.CTkButton(master=master_frame, text="Inserir Lead Personalizado", width=150,
                                                  hover_color='#804bb5', fg_color='#804bb5',
                                                  command=self.mostrar_upload_personalizado)
        btn_inserir_personalizado.grid(row=3, column=0, padx=20, pady=10)

        btn_limpar_bd = ctk.CTkButton(master=master_frame, text="Limpar Leads", width=150,
                                      hover_color='#804bb5', fg_color='#804bb5', command=self.mostrar_tela_limpeza)
        btn_limpar_bd.grid(row=4, column=0, padx=20, pady=10)

        btn_dashboard = ctk.CTkButton(master=master_frame, text="Criar Dashboard", width=150,
                                      hover_color='#804bb5', fg_color='#804bb5', command=self.criar_dashboard)
        btn_dashboard.grid(row=5, column=0, padx=20, pady=10)

        btn_deslogar = ctk.CTkButton(master=master_frame, text="Deslogar", hover_color='#3984cf', fg_color='#3984cf',
                                     command=self.logout_usuario)
        btn_deslogar.grid(row=6, column=0, padx=20, pady=10)

    def mostrar_tela_limpeza(self):
        self.frame.pack_forget()  # Ocultar o frame atual

        # Recriar o frame para evitar conflitos
        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        # Centralizar a grid
        self.frame.grid_columnconfigure(0, weight=1)

        # Adicionar label centralizado
        label = ctk.CTkLabel(master=self.frame, text="Selecione a Ação de Limpeza", font=('Horizon', 20, 'bold'))
        label.grid(row=0, column=0, padx=20, pady=20, sticky='n')

        # Botões de limpeza
        btn_limpar_campanha = ctk.CTkButton(master=self.frame, text="Limpar Campanha", hover_color='#804bb5',
                                            fg_color='#804bb5', command=self.limpar_campanha)
        btn_limpar_campanha.grid(row=1, column=0, padx=20, pady=10, sticky='n')

        btn_limpar_misto = ctk.CTkButton(master=self.frame, text="Limpar Misto", hover_color='#804bb5',
                                         fg_color='#804bb5', command=self.limpar_misto)
        btn_limpar_misto.grid(row=2, column=0, padx=20, pady=10, sticky='n')

        # Select box para selecionar usuário
        label_usuario = ctk.CTkLabel(master=self.frame, text="Selecione o usuário para Limpar Personalizado",
                                     font=('Horizon', 14))
        label_usuario.grid(row=3, column=0, padx=20, pady=(20, 10), sticky='n')

        usuarios_list = [user.email for user in firebase_admin.auth.list_users().iterate_all()]
        self.select_usuario_var = StringVar()
        self.select_usuario_box = ttk.Combobox(self.frame, textvariable=self.select_usuario_var, values=usuarios_list,
                                               state='readonly')
        self.select_usuario_box.grid(row=4, column=0, padx=20, pady=10, sticky='n')

        btn_limpar_personalizado = ctk.CTkButton(master=self.frame, text="Limpar Personalizado", hover_color='#804bb5',
                                                 fg_color='#804bb5', command=self.limpar_personalizado)
        btn_limpar_personalizado.grid(row=5, column=0, padx=20, pady=10, sticky='n')

        # Botão para "Limpar" a tela atual
        btn_limpar_tela = ctk.CTkButton(master=self.frame, text="Limpar Tela", hover_color='#804bb5',
                                        fg_color='#804bb5', command=self.limpar_tela)
        btn_limpar_tela.grid(row=6, column=0, padx=20, pady=10, sticky='n')

        self.progress_bar = ctk.CTkProgressBar(master=self.frame)
        self.progress_bar.grid(row=7, column=0, padx=20, pady=10)
        self.progress_bar.grid_remove()  # Ocultar a barra inicialmente

    def limpar_tela(self):
        for widget in self.frame.winfo_children():
            widget.grid_forget()

    def mostrar_upload_personalizado(self):
        if hasattr(self, 'frame') and self.frame:
            self.frame.pack_forget()

        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        label = ctk.CTkLabel(master=self.frame, text="Upload de Planilha Personalizada", font=('Horizon', 20, 'bold'),
                             text_color='white')
        label.pack(pady=20)

        # Selecionar o usuário destino
        label_usuario = ctk.CTkLabel(master=self.frame, text="Selecione o usuário", font=('Horizon', 14, 'bold'),
                                     text_color='white')
        label_usuario.pack(pady=(10, 0))

        # Aqui estamos usando o admin_auth do firebase_admin para listar usuários
        usuarios_list = [user.email for user in admin_auth.list_users().iterate_all()]
        self.select_usuario_var = StringVar()
        self.select_usuario_box = ttk.Combobox(self.frame, textvariable=self.select_usuario_var, values=usuarios_list,
                                               state='readonly')
        self.select_usuario_box.pack(pady=10)

        self.btn_upload = ctk.CTkButton(master=self.frame, text="Escolher Planilha", hover_color='#d1934e',
                                        fg_color='#d1934e', command=self.upload_file_personalizado)
        self.btn_upload.pack(pady=10)

        self.btn_enviar = ctk.CTkButton(master=self.frame, text="Enviar", state=DISABLED, hover_color='#d1934e',
                                        fg_color='#d1934e', command=self.enviar_dados_personalizado)
        self.btn_enviar.pack(pady=10)

        self.btn_voltar = ctk.CTkButton(master=self.frame, text="Voltar", hover_color='#d1934e', fg_color='#d1934e',
                                        command=self.voltar)
        self.btn_voltar.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(master=self.frame)
        self.progress_bar.pack_forget()  # Ocultar a barra inicialmente

    def upload_file_personalizado(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        if self.file_path:
            try:
                planilha_personalizada = pd.read_excel(self.file_path)

                if planilha_personalizada.empty:
                    raise ValueError("A planilha está vazia.")

                colunas_necessarias = {'CNPJ', 'Nome da Empresa', 'Endereço', 'Telefone', 'Email'}
                colunas_faltando = colunas_necessarias - set(planilha_personalizada.columns)
                if colunas_faltando:
                    raise ValueError(f"As seguintes colunas estão faltando: {', '.join(colunas_faltando)}")

                self.btn_enviar.configure(state=NORMAL)

            except Exception as e:
                self.file_path = None
                self.btn_enviar.configure(state=DISABLED)
                messagebox.showerror("Erro", f"Erro ao processar a planilha: {str(e)}")

    def enviar_dados_personalizado(self):
        if self.file_path and self.select_usuario_var.get():
            thread = threading.Thread(target=self.process_file_personalizado, args=(self.file_path,))
            thread.start()

    def process_file_personalizado(self, file_path):
        try:
            self.btn_enviar.configure(state=DISABLED)
            self.btn_voltar.configure(state=DISABLED)
            self.progress_bar.pack(pady=10)
            self.progress_bar.set(0)

            planilha_personalizada = pd.read_excel(file_path)
            dados_personalizados = planilha_personalizada.to_dict('records')
            total_dados = len(dados_personalizados)

            usuario_destino = self.select_usuario_var.get()

            for i, item in enumerate(dados_personalizados):
                cnpj = item.get('CNPJ')
                if self.empresa_duplicada(cnpj):
                    continue

                empresa_ref = db.collection(f'{usuario_destino}_personalizado').document(f'documento_{i}')
                empresa_ref.set(item)

                self.progress_bar.set((i + 1) / total_dados)
                time.sleep(0.1)

            messagebox.showinfo("Sucesso", "Dados personalizados distribuídos com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a planilha: {str(e)}")
        finally:
            self.btn_enviar.configure(state=NORMAL)
            self.btn_voltar.configure(state=NORMAL)
            self.progress_bar.pack_forget()

    def mostrar_upload_empresas(self):
        self.frame.pack_forget()

        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        label = ctk.CTkLabel(master=self.frame, text="Upload de Planilha de Empresas", font=('Horizon', 20, 'bold'),
                             text_color='white')
        label.pack(pady=20)

        self.btn_upload = ctk.CTkButton(master=self.frame, text="Escolher Planilha", hover_color='#d1934e',
                                        fg_color='#d1934e', command=self.upload_file_empresas)
        self.btn_upload.pack(pady=10)

        self.btn_enviar = ctk.CTkButton(master=self.frame, text="Enviar", state=DISABLED, hover_color='#d1934e',
                                        fg_color='#d1934e', command=self.enviar_dados_empresas)
        self.btn_enviar.pack(pady=10)

        self.btn_voltar = ctk.CTkButton(master=self.frame, text="Voltar", hover_color='#d1934e', fg_color='#d1934e',
                                        command=self.voltar)
        self.btn_voltar.pack(pady=10)

        # Adiciona uma barra de progresso
        self.progress_bar = ctk.CTkProgressBar(master=self.frame)
        self.progress_bar.pack_forget()  # Ocultar a barra inicialmente

    def mostrar_upload_empresas2(self):
        if hasattr(self, 'frame') and self.frame:  # Verifique se o frame existe e não é None
            self.frame.pack_forget()

        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        label = ctk.CTkLabel(master=self.frame, text="Upload de Planilha de Empresas2", font=('Horizon', 20, 'bold'),
                             text_color='white')
        label.pack(pady=20)

        self.btn_upload = ctk.CTkButton(master=self.frame, text="Escolher Planilha", hover_color='#d1934e',
                                        fg_color='#d1934e', command=self.upload_file_empresas2)
        self.btn_upload.pack(pady=10)

        self.btn_enviar = ctk.CTkButton(master=self.frame, text="Enviar", state=DISABLED, hover_color='#d1934e',
                                        fg_color='#d1934e', command=self.enviar_dados_empresas2)
        self.btn_enviar.pack(pady=10)

        self.btn_voltar = ctk.CTkButton(master=self.frame, text="Voltar", hover_color='#d1934e', fg_color='#d1934e',
                                        command=self.voltar)
        self.btn_voltar.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(master=self.frame)
        self.progress_bar.pack_forget()  # Ocultar a barra inicialmente

    def upload_file_empresas(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        if self.file_path:
            try:
                # Carregar a planilha
                planilha_empresas = pd.read_excel(self.file_path)

                # Verificar se a planilha está vazia
                if planilha_empresas.empty:
                    raise ValueError("A planilha está vazia.")

                # Verificar se as colunas necessárias estão presentes
                colunas_necessarias = {'CNPJ', 'Nome da Empresa', 'Endereço', 'Telefone', 'Email'}
                colunas_faltando = colunas_necessarias - set(planilha_empresas.columns)
                if colunas_faltando:
                    raise ValueError(f"As seguintes colunas estão faltando: {', '.join(colunas_faltando)}")

                # Se tudo estiver correto, habilitar o botão de enviar
                self.btn_enviar.configure(state=NORMAL)

            except Exception as e:
                self.file_path = None
                self.btn_enviar.configure(state=DISABLED)
                messagebox.showerror("Erro", f"Erro ao processar a planilha: {str(e)}")

    def upload_file_empresas2(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        if self.file_path:
            try:
                planilha_empresas = pd.read_excel(self.file_path)

                if planilha_empresas.empty:
                    raise ValueError("A planilha está vazia.")

                colunas_necessarias = {'CNPJ', 'Nome da Empresa', 'Endereço', 'Telefone', 'Email'}
                colunas_faltando = colunas_necessarias - set(planilha_empresas.columns)
                if colunas_faltando:
                    raise ValueError(f"As seguintes colunas estão faltando: {', '.join(colunas_faltando)}")

                self.btn_enviar.configure(state=NORMAL)

            except Exception as e:
                self.file_path = None
                self.btn_enviar.configure(state=DISABLED)
                messagebox.showerror("Erro", f"Erro ao processar a planilha: {str(e)}")

    def enviar_dados_empresas2(self):
        if self.file_path:
            thread = threading.Thread(target=self.process_file_empresas2, args=(self.file_path,))
            thread.start()

    def process_file_empresas2(self, file_path):
        try:
            self.btn_enviar.configure(state=DISABLED)
            self.btn_voltar.configure(state=DISABLED)
            self.progress_bar.pack(pady=10)
            self.progress_bar.set(0)

            planilha_empresas = pd.read_excel(file_path)
            dados_empresas = planilha_empresas.to_dict('records')
            total_dados = len(dados_empresas)

            usuarios = auth.list_users().users

            for i, item in enumerate(dados_empresas):
                cnpj = item.get('CNPJ')
                if self.empresa_duplicada(cnpj):
                    continue

                for usuario in usuarios:
                    email = usuario.email
                    if email != "luccasflores@mehsolucoes.com":
                        empresa_ref = db.collection(f'{email}_empresas2').document(f'documento_{i}')
                        empresa_ref.set(item)

                self.progress_bar.set((i + 1) / total_dados)
                time.sleep(0.1)

            messagebox.showinfo("Sucesso", "Dados das empresas2 distribuídos com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a planilha: {str(e)}")
        finally:
            self.btn_enviar.configure(state=NORMAL)
            self.btn_voltar.configure(state=NORMAL)
            self.progress_bar.pack_forget()

    def enviar_dados_empresas(self):
        if self.file_path:
            thread = threading.Thread(target=self.process_file_empresas, args=(self.file_path,))
            thread.start()

    def enviar_dados_empresas(self):
        if self.file_path:
            thread = threading.Thread(target=self.process_file_empresas, args=(self.file_path,))
            thread.start()

    def process_file_empresas(self, file_path):
        try:
            print(f"Processando o arquivo: {file_path}")  # Debug

            # Desabilitar o botão de envio enquanto o processo ocorre
            self.btn_enviar.configure(state=DISABLED)
            self.btn_voltar.configure(state=DISABLED)
            self.progress_bar.pack(pady=10)
            self.progress_bar.set(0)  # Resetar a barra de progresso

            # Carregar a planilha
            planilha_empresas = pd.read_excel(file_path)
            print(f"Planilha carregada: {planilha_empresas.head()}")  # Debug

            dados_empresas = planilha_empresas.to_dict('records')
            total_dados = len(dados_empresas)
            print(f"Total de registros a processar: {total_dados}")  # Debug

            usuarios = admin_auth.list_users().iterate_all()  # Obtém todos os usuários do Firebase

            for i, item in enumerate(dados_empresas):
                cnpj = item.get('CNPJ')
                if self.empresa_duplicada(cnpj):
                    print(f"Empresa duplicada encontrada: {cnpj}")  # Debug
                    continue

                for usuario in usuarios:
                    email = usuario.email
                    if email != "luccasflores@email.com":
                        try:
                            empresa_ref = db.collection(f'{email}_empresas').document(f'documento_{i}')
                            empresa_ref.set(item)
                            print(f"Dados enviados para Firestore para o CNPJ: {cnpj} no usuário: {email}")  # Debug
                        except Exception as e:
                            print(f"Erro ao enviar dados para {email}: {str(e)}")  # Debug de erro

                # Atualizar a barra de progresso
                self.progress_bar.set((i + 1) / total_dados)
                time.sleep(0.1)  # Adicionar uma pequena pausa para que a barra de progresso seja visível

            # Mensagem de sucesso após o processamento
            messagebox.showinfo("Sucesso", "Dados das empresas distribuídos com sucesso.")
        except Exception as e:
            # Mensagem de erro em caso de falha
            messagebox.showerror("Erro", f"Erro ao processar a planilha: {str(e)}")
            print(f"Erro ao processar a planilha: {str(e)}")  # Debug
        finally:
            # Reabilitar os botões e ocultar a barra de progresso
            self.btn_enviar.configure(state=NORMAL)
            self.btn_voltar.configure(state=NORMAL)
            self.progress_bar.pack_forget()

    def empresa_duplicada(self, cnpj):
        try:
            docs = db.collection('empresas').where('CNPJ', '==', cnpj).stream()
            duplicada = any(docs)
            print(f"Empresa {cnpj} duplicada: {duplicada}")  # Debug
            return duplicada
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar duplicação: {str(e)}")
            return False

    def mostrar_opcoes_limpar(self):
        self.frame.pack_forget()

        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        label = ctk.CTkLabel(master=self.frame, text="Limpar Banco de Dados", font=('Horizon', 20, 'bold'),
                             text_color='white')
        label.pack(pady=20)

        self.btn_limpar_empresas = ctk.CTkButton(master=self.frame, text="Limpar Empresas", hover_color='#804bb5', fg_color='#804bb5', command=self.limpar_dados_empresas)
        self.btn_limpar_empresas.pack(pady=10)

        self.btn_voltar = ctk.CTkButton(master=self.frame, text="Cancelar", hover_color='#804bb5', fg_color='#804bb5', command=self.voltar)
        self.btn_voltar.pack(pady=10)

    def limpar_dados_empresas(self):
        try:
            usuarios = auth.list_users().users
            for usuario in usuarios:
                email = usuario.email
                if email:
                    empresa_docs = db.collection(f'{email}_empresas').stream()
                    for doc in empresa_docs:
                        db.collection(f'{email}_empresas').document(doc.id).delete()

            messagebox.showinfo("Sucesso", "Banco de dados Empresas limpo!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar banco de dados Empresas: {str(e)}")
        finally:
            self.voltar()

    def criar_dashboard(self):
        if hasattr(self, 'frame') and self.frame:
            self.frame.pack_forget()

        self.frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.frame.pack(side=RIGHT, padx=10, pady=10, fill='y')

        label = ctk.CTkLabel(master=self.frame, text="Criar Dashboard", font=('Horizon', 20, 'bold'),
                             text_color='white')
        label.pack(pady=20)

        # Adicionar o ComboBox para selecionar o usuário ou "Geral"
        label_usuario = ctk.CTkLabel(master=self.frame, text="Selecione o Usuário ou Geral:", font=('Horizon', 14),
                                     text_color='white')
        label_usuario.pack(pady=(10, 5))

        usuarios_list = [user.email for user in firebase_admin.auth.list_users().iterate_all()]
        usuarios_list.append("Geral")  # Adicionar a opção "Geral"

        self.select_usuario_var = StringVar()
        self.select_usuario_box = ttk.Combobox(self.frame, textvariable=self.select_usuario_var, values=usuarios_list,
                                               state='readonly')
        self.select_usuario_box.pack(pady=10)

        btn_criar_dashboard = ctk.CTkButton(master=self.frame, text="Criar", hover_color='#804bb5', fg_color='#804bb5',
                                            command=self.gerar_dashboard)
        btn_criar_dashboard.pack(pady=10)

        btn_gerar_grafico = ctk.CTkButton(master=self.frame, text="Gerar Gráfico", hover_color='#804bb5',
                                          fg_color='#804bb5',
                                          command=self.gerar_grafico)
        btn_gerar_grafico.pack(pady=10)

        btn_voltar = ctk.CTkButton(master=self.frame, text="Voltar", hover_color='#804bb5', fg_color='#804bb5',
                                   command=self.voltar)
        btn_voltar.pack(pady=10)

    def gerar_grafico(self):
        try:
            usuario_selecionado = self.select_usuario_var.get().strip()  # Remover espaços em branco

            if usuario_selecionado == "Geral":
                # Buscar todos os documentos na coleção "tabulados"
                tabulados_docs = db.collection('tabulados').stream()
                clientes_tabulações = [doc.to_dict() for doc in tabulados_docs]
            else:
                # Filtrar os documentos pelo usuário selecionado
                tabulados_docs = db.collection('tabulados').where('Usuário', '==', usuario_selecionado).stream()
                clientes_tabulações = [doc.to_dict() for doc in tabulados_docs]

            if not clientes_tabulações:
                messagebox.showinfo("Informação",
                                    f"Nenhum dado encontrado para o usuário '{usuario_selecionado}' na coleção 'tabulados'.")
                return

            df = pd.DataFrame(clientes_tabulações)

            # Agrupar os dados por 'Tabulação' e 'Usuário'
            tabulacao_counts = df.groupby(['Tabulação', 'Usuário']).size().unstack(fill_value=0)

            # Gerar gráfico de pizza
            fig, ax = plt.subplots()
            tabulacao_counts.sum(axis=1).plot(kind='pie', ax=ax, colors=['#804bb5'] * len(tabulacao_counts),
                                              autopct='%1.1f%%', startangle=90)
            ax.set_ylabel('')

            ax.set_title('Distribuição das Tabulações')

            # Salvar o gráfico
            nome_grafico = f"grafico_tabulacao_{usuario_selecionado.replace('@', '_').replace('.', '_')}.png"
            plt.savefig(nome_grafico)
            plt.show()

            messagebox.showinfo("Sucesso", f"Gráfico criado com sucesso! Arquivo: {nome_grafico}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar gráfico: {str(e)}")
            print(e)

    def gerar_dashboard(self):
        try:
            usuario_selecionado = self.select_usuario_var.get().strip()  # Remover espaços em branco

            if usuario_selecionado == "Geral":
                # Buscar todos os documentos na coleção "tabulados"
                tabulados_docs = db.collection('tabulados').stream()
                clientes_tabulações = [doc.to_dict() for doc in tabulados_docs]
            else:
                # Filtrar os documentos pelo usuário selecionado
                tabulados_docs = db.collection('tabulados').where('Usuário', '==', usuario_selecionado).stream()
                clientes_tabulações = [doc.to_dict() for doc in tabulados_docs]

            if not clientes_tabulações:
                messagebox.showinfo("Informação",
                                    f"Nenhum dado encontrado para o usuário '{usuario_selecionado}' na coleção 'tabulados'.")
                return

            # Convertendo datetimes com timezone para timezone unaware
            for item in clientes_tabulações:
                for key, value in item.items():
                    if isinstance(value, pd.Timestamp):
                        item[key] = value.tz_localize(None)
                    elif isinstance(value, datetime):
                        item[key] = value.replace(tzinfo=None)

            df = pd.DataFrame(clientes_tabulações)

            nome_arquivo = f"dashboard_tabulados_{usuario_selecionado.replace('@', '_').replace('.', '_')}.xlsx"
            df.to_excel(nome_arquivo, index=False)
            messagebox.showinfo("Sucesso", f"Dashboard criado com sucesso! Arquivo: {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar dashboard: {str(e)}")
            print(e)

    def carregar_cliente(self):
        try:
            colecao_ref = db.collection(f'{self.email}_empresas')
            docs = colecao_ref.stream()
            self.clientes = [{'id': doc.id, **doc.to_dict()} for doc in docs]

            if self.clientes:
                self.mostrar_cliente(self.clientes[self.index_cliente])
            else:
                self.label_banco.configure(text="Nenhum cliente encontrado.")
        except Exception as e:
            print(f"Erro ao carregar cliente: {e}")

    def mostrar_cliente(self, cliente):
        if not self.label_banco.winfo_exists():
            return

        # Limpar o conteúdo anterior
        for widget in self.label_banco.winfo_children():
            widget.destroy()

        # Exibir o nome da empresa como título e permitir cópia ao clicar
        nome_empresa = cliente.get('Nome da Empresa', 'N/A')
        nome_label = ctk.CTkLabel(self.label_banco, text=nome_empresa, font=('Horizon', 18, 'bold'), text_color='white')
        nome_label.grid(sticky="w", padx=5, pady=(0, 10))  # Reduzi o padding vertical aqui
        nome_label.bind("<Button-1>", lambda e, text=nome_empresa: self.copiar_para_area_de_transferencia(text))

        # Exibir outras informações do cliente e permitir cópia ao clicar
        info = {
            "CNPJ": cliente.get('CNPJ', 'N/A'),
            "Email": cliente.get('Email', 'N/A'),
            "Telefone": cliente.get('Telefone', 'N/A'),
            "Data de Início": cliente.get('Data de inicio', 'N/A'),
            "Estado": cliente.get('Estado', 'N/A')
        }

        for key, value in info.items():
            label = ctk.CTkLabel(self.label_banco, text=f"{key}: {value}", text_color="white", anchor="w")
            label.grid(sticky="w", padx=5, pady=(0, 2))  # Reduzi o padding vertical aqui
            label.bind("<Button-1>", lambda e, text=value: self.copiar_para_area_de_transferencia(text))

        # Adicionar o combobox para selecionar a opção de tabulação
        texto_selecao = ctk.CTkLabel(self.label_banco, text="Selecione uma Opção:", font=('Horizon', 14),
                                     text_color='white')
        texto_selecao.grid(sticky="w", padx=5, pady=(10, 5))

        self.select_var = StringVar()
        self.select_box = ttk.Combobox(self.label_banco, textvariable=self.select_var, width=30)
        self.select_box['values'] = (
            "Ligação + Whatsapp", "Apenas Ligação", "Sem Telefone Cadastrado", "Sem Interesse",
            "Negociação em Andamento", "Cliente Fechado", "Só Whatsapp", "Email enviado", "Email + Whatsapp"
        )
        self.select_box['state'] = 'readonly'  # Impede que o usuário digite no ComboBox
        self.select_box.grid(sticky="w", padx=10, pady=(0, 10))
        self.select_box.bind("<<ComboboxSelected>>", self.habilitar_proximo)

        # Adicionar os botões "Próximo", "Limpar", "Whatsapp" e "Email" abaixo do selectbox
        button_frame = ctk.CTkFrame(self.label_banco)
        button_frame.grid(sticky="w", padx=10, pady=(10, 0))

        self.proximo_button = ctk.CTkButton(button_frame, text="Próximo", width=100, hover_color='#804bb5',
                                            fg_color='#804bb5', command=self.proximo_cliente)
        self.proximo_button.grid(row=0, column=0, padx=5, pady=5)
        self.proximo_button.configure(state="disabled")

        self.limpar_button = ctk.CTkButton(button_frame, text="Limpar", width=100, hover_color='#9a7d61',
                                           fg_color='#9a7d61', command=self.limpar_informacoes)
        self.limpar_button.grid(row=0, column=1, padx=5, pady=5)

        self.whatsapp_button = ctk.CTkButton(button_frame, text="Whatsapp", width=100,
                                             hover_color='#804bb5', fg_color='#804bb5', command=self.enviar_whatsapp)
        self.whatsapp_button.grid(row=1, column=0, padx=5, pady=10)

        self.email_button = ctk.CTkButton(button_frame, text="Email", width=100, hover_color='#804bb5',
                                          fg_color='#804bb5', command=self.enviar_email)
        self.email_button.grid(row=1, column=1, padx=5, pady=10)
        self.telefone_button = ctk.CTkButton(button_frame, text="Ligar", width=100, hover_color='#804bb5',
                                             fg_color='#804bb5', command=self.fazer_ligacao)
        self.telefone_button.grid(row=1, column=2, padx=5, pady=10)

    def fazer_ligacao(self):
        cliente_atual = self.clientes[self.index_cliente]
        telefone = cliente_atual.get('Telefone', '')

        if telefone:
            telefone_formatado = str(telefone).replace(' ', '').replace('-', '')  # Remover espaços e traços
            # Exemplo para abrir o Skype
            url = f"skype:{telefone_formatado}?call"
            os.system(f'start {url}')
        else:
            messagebox.showwarning("Aviso", "Telefone não disponível para o cliente atual.")
    def habilitar_proximo(self, event):
        self.proximo_button.configure(state="normal")

    def proximo_cliente(self):
        cliente_atual = self.clientes[self.index_cliente]
        tabulacao_selecionada = self.select_var.get()

        if tabulacao_selecionada:
            try:
                # Adicionando dados de tabulação na coleção "tabulados"
                dados_tabulados = {
                    "Nome da Empresa": cliente_atual.get('Nome da Empresa', 'N/A'),
                    "CNPJ": cliente_atual.get('CNPJ', 'N/A'),
                    "Email": cliente_atual.get('Email', 'N/A'),
                    "Telefone": cliente_atual.get('Telefone', 'N/A'),
                    "Data de Início": cliente_atual.get('Data de inicio', 'N/A'),
                    "Estado": cliente_atual.get('Estado', 'N/A'),
                    "Tabulação": tabulacao_selecionada,
                    "Usuário": self.email,  # Adiciona o e-mail do usuário que tabulou
                    "Data da Tabulação": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # Adiciona a data e hora da tabulação
                }

                # Enviar para a coleção "tabulados"
                db.collection('tabulados').add(dados_tabulados)
                messagebox.showinfo("Sucesso", "Dados tabulados com sucesso!")

                # Excluir o documento da coleção personalizada após a tabulação
                db.collection(f'{self.email}_empresas').document(cliente_atual['id']).delete()
                self.clientes.pop(self.index_cliente)  # Remover o cliente da lista local

                # Se todos os clientes foram tabulados, exibir mensagem e resetar o index
                if not self.clientes:
                    messagebox.showinfo("Informação", "Todos os clientes foram tabulados.")
                    self.index_cliente = 0
                else:
                    # Avançar para o próximo cliente na lista
                    self.index_cliente = (self.index_cliente + 1) % len(self.clientes)
                    self.mostrar_cliente(self.clientes[self.index_cliente])

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar tabulação: {str(e)}")

    def limpar_informacoes(self):
        for widget in self.janela.winfo_children():
            widget.pack_forget()
        self.login_efetuado()

    def copiar_para_area_de_transferencia(self, texto):
        if isinstance(texto, datetime):
            texto = texto.strftime('%d/%m/%Y')
        pyperclip.copy(texto)

    def enviar_whatsapp(self):
        # Mapeamento de e-mails para nomes
        usuarios = {
            "email@email.com": "Carol",
        }

        # Obter o nome do usuário autenticado
        nome_usuario = usuarios.get(self.email,
                                    "M&H Soluções")  # 'M&H Soluções' é o padrão caso o e-mail não seja encontrado

        cliente_atual = self.clientes[self.index_cliente]
        telefone = cliente_atual.get('Telefone', '')
        telefone = str(telefone).replace(' ', '').replace('-', '')
        mensagem = f"Olá! Sou {nome_usuario} da M&H Soluções. Podemos conversar?"

        if telefone:
            url = f"https://web.whatsapp.com/send?phone=55{telefone}&text={urllib.parse.quote(mensagem)}"
            os.system(f'start {url}')  # Isso abre o link no navegador padrão
        else:
            messagebox.showwarning("Aviso", "Telefone não disponível para o cliente atual.")

    def enviar_email(self):
        cliente_atual = self.clientes[self.index_cliente]
        destinatario = cliente_atual.get('Email', '')

        if not destinatario:
            messagebox.showwarning("Aviso", "Email não disponível para o cliente atual.")
            return

        # Obter dados do usuário autenticado
        usuario_atual = usuarios.get(self.email)

        if not usuario_atual:
            messagebox.showerror("Erro", "Usuário não encontrado para envio de e-mail.")
            return

        smtp_server = usuario_atual["smtp_server"]
        smtp_port = usuario_atual["smtp_port"]
        smtp_user = usuario_atual["smtp_user"]
        smtp_password = usuario_atual["smtp_password"]
        nome_usuario = usuario_atual["nome"]
        assinatura = usuario_atual["assinatura"]

        # Corpo do email com conteúdo HTML personalizado
        # Corpo do email com conteúdo HTML personalizado
        corpo_email = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Olá,</title>
        </head>
        <body>
          <table align="center" width="600" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; border-collapse: collapse;">
            <tr>
              <td style="padding: 20px 0; text-align: center; background-color: #8c52ff;">
                <img src="cid:logo" alt="M&H Soluções" style="max-width: 100%; height: auto; width: 200px;">
              </td>
            </tr>
            <tr>
              <td style="padding: 20px; text-align: left;">
                <p>Boa tarde,</p>
                <p>Sou {nome_usuario} da <strong>M&amp;H Soluções</strong>, uma empresa dedicada a oferecer soluções de software para facilitar e otimizar a gestão de escritórios.</p>
                <p>Gostaríamos de apresentar a você o nosso software, projetado para simplificar suas tarefas diárias, melhorar a organização e aumentar a produtividade da sua equipe. Com ele, você pode gerenciar contatos, enviar e-mails e mensagens, e acessar relatórios detalhados para acompanhar o desempenho do seu negócio.</p>
                <p>Estamos confiantes de que o M&H Soluções pode trazer grandes benefícios para sua empresa. Podemos agendar uma breve demonstração para mostrar como ele funciona?</p>
                <p>Deixei uma breve apresentação em anexo. Visite nosso site em <a href="http://mehsolucoes.com" target="_blank" style="color: #8c52ff; text-decoration: none;">mehsolucoes.com</a> para saber mais, ou responda este e-mail para agendar uma <strong>consulta gratuita</strong>.</p>

                <p>Atenciosamente,</p>
                <p><img src="cid:assinatura" alt="Assinatura" style="width: 600px; height: 300px;"></p>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.set_debuglevel(1)

            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = destinatario
            msg['Subject'] = "Vamos agendar uma demonstração?"

            # Adicionando o corpo do email
            msg.attach(MIMEText(corpo_email, 'html'))

            # Anexando a imagem da logo
            with open(resource_path("logo.png"), 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<logo>')
                img.add_header('Content-Disposition', 'inline', filename='logo.png')
                msg.attach(img)

            # Anexando a assinatura
            with open(resource_path(assinatura), 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<assinatura>')
                img.add_header('Content-Disposition', 'inline', filename=assinatura)
                msg.attach(img)

            # Anexando o PDF da apresentação
            with open(resource_path("Apresentacao.pdf"), 'rb') as pdf_file:
                pdf = MIMEApplication(pdf_file.read())
                pdf.add_header('Content-Disposition', 'attachment', filename="Apresentacao.pdf")
                msg.attach(pdf)

            server.sendmail(smtp_user, destinatario, msg.as_string())
            server.quit()
            messagebox.showinfo("Sucesso", f"Email enviado para {destinatario}")
        except Exception as e:
            messagebox.showerror("Erro", f'Erro ao enviar email para {destinatario}: {str(e)}')

    def logout_usuario(self):
        try:
            self.usuario_atual = None
            for widget in self.janela.winfo_children():
                widget.pack_forget()
            messagebox.showinfo(title="Logout", message="Você foi deslogado com sucesso!")
            self.tela_login()

        except Exception as e:
            messagebox.showerror(title="Erro", message=f"Erro ao deslogar: {str(e)}")

    def voltar(self):
        if hasattr(self, 'frame'):
            self.frame.pack_forget()  # Remove o frame da tela, o que esconde tudo relacionado a ele
            self.frame = None  # Opcional: libere o frame da memória, se necessário


if __name__ == "__main__":
    app = Application()
#   s i s t e m a - t a b u l a c a o  
 