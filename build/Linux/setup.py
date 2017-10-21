from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict (packages = []
                    ,includes = ["re"]
                    ,excludes = []
                    )

executables = [Executable ('mclient.py'
                          ,base = 'Console'
                          ,icon = 'resources/icon_64x64_mclient.gif'
                          ,targetName = 'mclient'
                          )
              ]

setup (name        = 'MClient'
      ,version     = '5'
      ,description = 'Multitran Online Client'
      ,options     = dict(build_exe=buildOptions)
      ,executables = executables
      )
