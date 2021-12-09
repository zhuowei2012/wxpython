#!/usr/bin/env python
"""Hello, wxPython! program."""
import wx


class Frame(wx.Frame):
    """Frame class that displays an image."""

    def __init__(self, image, parent=None, id=-1,
                 pos=wx.DefaultPosition,
                 title='Hello, wxPython!'):
        """Create a Frame instance and display image."""

        temp = image.ConvertToBitmap()
        size = temp.GetWidth(), temp.GetHeight()
        wx.Frame.__init__(self, parent, id, title, pos, size)
        self.bmp = wx.StaticBitmap(parent=self, bitmap=temp)


class App(wx.App):
    """Application class."""

    def OnInit(self):
        #image = wx.Image('1.jpg', wx.BITMAP_TYPE_JPEG)
        #self.frame = Frame(image)
        #self.frame.Show()
        #self.SetTopWindow(self.frame)

        self.frame = wx.Frame(None, title="Gui Test Editor", pos=(1000, 200), size=(500, 400))

        panel = wx.Panel(self.frame)
        path_text = wx.TextCtrl(panel)
        open_button = wx.Button(panel, label="打开")

        save_button = wx.Button(panel, label="保存")

        content_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        #  wx.TE_MULTILINE可以实现以滚动条方式多行显示文本,若不加此功能文本文档显示为一行

        box = wx.BoxSizer()  # 不带参数表示默认实例化一个水平尺寸器
        box.Add(path_text, proportion=5, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件
        # proportion：相对比例
        # flag：填充的样式和方向,wx.EXPAND为完整填充，wx.ALL为填充的方向
        # border：边框
        box.Add(open_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件
        box.Add(save_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

        v_box = wx.BoxSizer(wx.VERTICAL)  # wx.VERTICAL参数表示实例化一个垂直尺寸器
        v_box.Add(box, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件
        v_box.Add(content_text, proportion=5, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

        panel.SetSizer(v_box)  # 设置主尺寸器



        self.frame.Show()
        self.SetTopWindow(self.frame)


        return True


def main():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()