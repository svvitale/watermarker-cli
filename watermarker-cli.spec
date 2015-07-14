# -*- mode: python -*-
a = Analysis(['watermarker-cli\\watermarker-cli.py'],
             pathex=['watermarker-cli'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + [
            ('Qwigley-Regular.ttf', 'watermarker-cli\\Qwigley-Regular.ttf', 'DATA')
          ],
          name='watermarker-cli.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
