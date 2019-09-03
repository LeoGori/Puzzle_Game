import cx_Freeze

executables = [cx_Freeze.Executable("MenuLoop.py")]

cx_Freeze.setup(
    name = "Puzzle Game",
    options = { "build_exe": {"packages": ["pygame", "stopwatch"],
        "include_files":["Risorse", "img"]}},
        executables = executables
)