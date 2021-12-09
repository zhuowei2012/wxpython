# -*- coding: utf-8 -*-

"""

Created on Tue Mar 17 14:31:37 2020

@author: liyan

"""

import wx
import os
from Crypto.Cipher import AES



class Aescrypt():
    def __init__(self, key, model):
        self.key = self.add_16(key)
        self.model = model
        self.iv = b'0000000000000000'

    def add_16(self, par):
        if type(par) == str:
            par = par.encode()
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self, text):
        text = self.add_16(text)
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key, self.model, self.iv)
        elif self.model == AES.MODE_ECB:
            self.aes = AES.new(self.key, self.model)
        self.encrypt_text = self.aes.encrypt(text)
        return self.encrypt_text

    def aesdecrypt(self, text):
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key, self.model, self.iv)
        elif self.model == AES.MODE_ECB:
            self.aes = AES.new(self.key, self.model)
        self.decrypt_text = self.aes.decrypt(text)
        self.decrypt_text = self.decrypt_text.strip(b"\x00")
        return self.decrypt_text

    def encrypt_file(self, filepath, encrypt_filepath=''):
        # 加载数据
        with open(filepath, 'rb') as f:
            data = f.read()
        # 加密数据
        data = self.aesencrypt(data)
        # 夹加密好的数据写到加密文件上
        if not encrypt_filepath:
            filepath = os.path.split(filepath)
            encrypt_filepath = filepath[0] + '/encrypt_' + filepath[1]
        with open(encrypt_filepath, 'wb') as f:
            f.write(data)

    def decrypt_file(self, encrypt_filepath, decrypt_filepath=''):
        # 加载数据
        with open(encrypt_filepath, 'rb') as f:
            data = f.read()
        # 加密数据
        data = self.aesdecrypt(data)
        # 夹加密好的数据写到加密文件上
        if not decrypt_filepath:
            encrypt_filepath = os.path.split(encrypt_filepath)
            decrypt_filepath = encrypt_filepath[0] + '/decrypt_' + encrypt_filepath[1]
        with open(decrypt_filepath, 'wb') as f:
            f.write(data)
        return decrypt_filepath

passwd = "123456781234567"
aescryptor = Aescrypt(passwd, AES.MODE_CBC)  # CBC模式

class picLog(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self,None,title='picLog',size=(1320,960))

        self.SelBtn = wx.Button(self,label='请选择加密图片',pos=(305,5),size=(180,25))

        self.SelBtn.Bind(wx.EVT_BUTTON,self.OnOpenFile)

        self.OkBtn = wx.Button(self,label='解密并显示',pos=(525,5),size=(180,25))

        self.OkBtn.Bind(wx.EVT_BUTTON,self.Onpic)

        self.FileName = wx.TextCtrl(self,pos=(5,5),size=(230,25))
        self.FileName.SetEditable(False)

        self.panel = wx.Panel(self,pos=(5,30),size=(1285,960))

    def OnOpenFile(self,event):

        wildcard = 'All files(*.*)|*.*'

        dialog = wx.FileDialog(None,'select',os.getcwd(),'',wildcard,wx.FD_OPEN)  #####这个部分新旧版本有变化

        if dialog.ShowModal() == wx.ID_OK:

            self.FileName.SetValue(dialog.GetPath())

            dialog.Destroy


    def Onpic(self,event):

        panel=wx.Panel(self,pos=(30,30),size=(1320,960))

        try:
            decrypt_filepath = aescryptor.decrypt_file(self.FileName.GetValue())

            img3= wx.Image(decrypt_filepath, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            show3=wx.StaticBitmap(self.panel, -1, img3, pos=(8, 0),size=(1285,960))
        except:
            toastone = wx.MessageDialog(None, "图片打开失败，请确认选择的是加密后的图片!", "错误信息提示", wx.YES_DEFAULT | wx.ICON_QUESTION)
            if toastone.ShowModal() == wx.ID_YES:  # 如果点击了提示框的确定按钮
                toastone.Destroy()  # 则关闭提示框




if __name__=='__main__':

    app = wx.App()

    SiteFrame = picLog()

    SiteFrame.Show()

    app.MainLoop()