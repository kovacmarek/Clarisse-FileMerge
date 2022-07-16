from asyncio.windows_events import NULL
import os.path
import re

from pathlib import Path

targetPath = None
try:
    targetPath = ix.selection.get(0)
except:
    pass

result = {'rangeStart' : 0, 'rangeEnd' : 5, "filePath" : "/path/file._sep_.####.vdb", "separator": "_sep_"}
sel = ix.application.get_selection()


class EventRewire(ix.api.EventObject):
    def rangeStart(self, sender, evtid):
        result['rangeStart'] = sender.get_value()

    def rangeEnd(self, sender, evtid):
        result['rangeEnd'] = sender.get_value()

    def filePath(self, sender, evtid):
        result['filePath'] = sender.get_value()

    def separator(self, sender, evtid):
        result['separator'] = sender.get_value()

    def cancel(self, sender, evtid):
        sender.get_window().hide()

    def run(self, sender, evtid):
        origName = "file"
        rangeS = int(rangeStart.get_value())
        rangeE = int(rangeEnd.get_value())
        global targetPath
        missedFiles = []

        for i in range(rangeS, rangeE):
            name = origName + "_" + str(i)
            path = filePath.get_filename().replace(separator.get_filename(), str(i))
            pathMatch = re.match("[\w\W]*[\\|\/]([^#]*)(\.#{1,5})?\.[\w]{1,10}", path)
            strippedFilename = pathMatch.group(1)

            existingFileList = os.listdir(str(Path(path).parent))
            isCreated = False
            for existingFile in existingFileList:
                if (existingFile.startswith(strippedFilename)):
                    file = ix.cmds.CreateObject(name, "GeometryVolumeFile", "Global", targetPath)
                    file.attrs.filename[0] = path
                    isCreated = True
                    break
            if(isCreated == False):
                missedFiles.append(path)

        print("------" + "\n" + "Files Missed:")
        for i in range(len(missedFiles)):
            print( str(missedFiles[i]))
        print("------")

        if len(missedFiles) == 0:
            windowMissing = ix.api.GuiMessageBox(clarisse_win, 600, 400, "Info", "Import succesfull!")
        else:
            windowMissing = ix.api.GuiMessageBox(clarisse_win, 600, 400, "Warning", "Some files were not imported (Check logs)")
        
        windowMissing.show()
        while windowMissing.is_shown():    ix.application.check_for_events()
        windowMissing.destroy()

        sender.get_window().hide()

            
#Window creation
clarisse_win = ix.application.get_event_window()
window = ix.api.GuiWindow(clarisse_win, 600, 400, 500, 160)
window.set_title('Set values...')

#Main widget creation
panel = ix.api.GuiPanel(window, 0, 0, window.get_width(), window.get_height())
panel.set_constraints(ix.api.GuiWidget.CONSTRAINT_LEFT, ix.api.GuiWidget.CONSTRAINT_TOP, ix.api.GuiWidget.CONSTRAINT_RIGHT, ix.api.GuiWidget.CONSTRAINT_BOTTOM)

#Form generation
rangeStart = ix.api.GuiNumberField(panel, 79, 10, 151, "Range Start :  ")

rangeEnd = ix.api.GuiNumberField(panel, 79, 30, 151, "Range End : ")

filePath = ix.api.GuiFilenameField(panel, 79, 70, 400, "File Path : ")
filePath.set_mode(1)

separator = ix.api.GuiFilenameField(panel, 79, 90, 150, "Separator : ")
separator.set_mode(1)
cancelBtn = ix.api.GuiPushButton(panel, 10, 130, 100, 22, "Cancel")
runBtn = ix.api.GuiPushButton(panel, 130, 130, 100, 22, "Run")

#init values
rangeStart.set_value(result['rangeStart'])
rangeEnd.set_value(result['rangeEnd'])
filePath.set_filename(result['filePath'])
separator.set_filename(result['separator'])


#Connect to function
event_rewire = EventRewire()

event_rewire.connect(rangeStart, 'EVT_ID_NUMBER_FIELD_VALUE_CHANGING', event_rewire.rangeStart)
event_rewire.connect(rangeStart, 'EVT_ID_NUMBER_FIELD_VALUE_CHANGED', event_rewire.rangeStart)
event_rewire.connect(rangeEnd, 'EVT_ID_NUMBER_FIELD_VALUE_CHANGING', event_rewire.rangeEnd)
event_rewire.connect(rangeEnd, 'EVT_ID_NUMBER_FIELD_VALUE_CHANGED', event_rewire.rangeEnd)
event_rewire.connect(filePath, 'EVT_ID_NUMBER_FIELD_VALUE_CHANGING', event_rewire.filePath)
event_rewire.connect(filePath, 'EVT_ID_NUMBER_FIELD_VALUE_CHANGED', event_rewire.filePath)
event_rewire.connect(separator, 'EVT_ID_NUMBER_FIELD_VALUE_CHANGING', event_rewire.separator)
event_rewire.connect(separator, 'EVT_ID_NUMBER_FIELD_VALUE_CHANGED', event_rewire.separator)
event_rewire.connect(cancelBtn, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.cancel)
event_rewire.connect(runBtn, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.run)

#Send all info to clarisse to generate window
if(ix.selection.is_empty()):
    windowError = ix.api.GuiMessageBox(clarisse_win, 600, 400, "Missing Selection", "Please, select target Context folder")
    windowError.show()
    while windowError.is_shown():    ix.application.check_for_events()
    windowError.destroy()
else:
    window.show()
    while window.is_shown():    ix.application.check_for_events()
    window.destroy()
    
