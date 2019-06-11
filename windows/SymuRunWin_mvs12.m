clear

oldFolder = cd('C:\MyDropbox\Dropbox\DEV_PLATEFORME_SYMUVIA\SymubruitDLL\Release\x64')

if not(libisloaded('SymuVia'))
    loadlibrary('SymuVia.dll','SymExpC.h')    
end

libfunctions SymuVia -full

sInput = 'C:\Tmp\LafayetteITS2.xml';
calllib('SymuVia', 'SymRunEx', sInput)

unloadlibrary SymuVia;

cd(oldFolder)
