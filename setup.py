import cx_Freeze

executables  = [cx_Freeze.Executable("Batgame.py")]

cx_Freeze.setup(
    name = "Bat's Hunt",
    options = {"build_exe": {"packages":["pygame"],
                              "include_files":["bat.png","batsilver.png","bg.jpg","bgforwhite.jpg","bghelp.jpg","bgm.wav",
                                               "bgmain.jpg","bgstart.jpg","end.wav","fly.gif","icon.png","perfecto.gif","start.wav"]}},
               executables = executables
    )
    
    
