from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], includes = ["re"], excludes = [])

executables = [
    Executable('mclient.pyw', base = 'Win32GUI', icon = 'icon_64x64_mclient.ico', targetName = 'mclient.exe')
]

setup(name='mclient.pyw',
      version = '4.5.2',
      description = 'Multitran Online Client',
      options = dict(build_exe = buildOptions),
      executables = executables)
