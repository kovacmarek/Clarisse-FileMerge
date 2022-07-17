# Clarisse FileMerge
Houdini's FileMerge node recreated inside Clarisse

![image](https://user-images.githubusercontent.com/30508711/179374192-4c978b97-53dc-4a26-9ce6-e49ebd540a0b.png)

- Creating the shelf tool

![image](https://user-images.githubusercontent.com/30508711/179374391-725d821a-f590-477b-b9c1-85d016118d69.png)

![image](https://user-images.githubusercontent.com/30508711/179374371-d5b1252f-1aca-4bf5-b460-fb7cad655ed8.png)


### Steps:

1. Select Context folder

2. Run script

3. Set range of variations / wedges

4. Select first file of the sequence and replace `1001` with `####` & same goes for separator (called $SLICE in Houdini).


### Add. info:

- If you set range to 0-10, but your geometry is only 0-5, it will import files available on disk and report missing geometries in Logs (6-10 missing in this case).
- For still frames, exclude `####` from the file name.
- In it's current state, this tool is not setting `Frame Range` & `Frame Rate`. It's neccessary to press CTRL+A and set these values on all the sims manually (with detect range button) after successful script execution.
