oldpath = path;
addpath( 'C:\MyDropbox\Dropbox\DEV_PLATEFORME_SYMUVIA\SymubruitDLL\Release\x64' )

if not(libisloaded('SymuVia'))
    loadlibrary('SymuVia.dll','SymExpC.h')
end

libfunctions('SymuVia')

calllib('SymuVia', 'SymRunEx', 'C:\Tmp\LafayetteITS.xml');

unloadlibrary('SymuVia')

path = oldpath