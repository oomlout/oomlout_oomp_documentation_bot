import oom_kicad

import os

def document_project(**kwargs):
    github = kwargs.get('github', None)
    #get the eagle board file from the kwargs
    eagle_board_file_src = kwargs.get('eagle_board_file_src', None)
    #get the eagle schematic file from the kwargs
    eagle_schematic_file_src = kwargs.get('eagle_schematic_file_src', None)
    #get the kicas src directory from the kwargs
    kicad_src_directory = kwargs.get('kicad_src_directory', None)

    ##figure out directory
    #get the github user name from the web address
    github_user = github.split('/')[3]
    kwargs['github_user'] = github_user
    #get the github project name from the web address
    github_project = github.split('/')[4]
    kwargs['github_project'] = github_project
    directory = f'projects/{github_user}/{github_project}/'
    kwargs['directory'] = directory
    #set directory_oomp

    #do git clone or pull    
    kwargs = git_project(**kwargs)

    #create a /oomp directory in the project directory
    if not os.path.exists(f'{directory}/oomp'):
        os.makedirs(f'{directory}/oomp')
    #if oomp/src doesn't exist create it
    if not os.path.exists(f'{directory}/oomp/src'):
        os.makedirs(f'{directory}/oomp/src')

    if eagle_board_file_src:
        for key in eagle_board_file_src:
            #make the directory with key
            if not os.path.exists(f'{directory}/oomp/src/{key}'):
                os.makedirs(f'{directory}/oomp/src/{key}')
            #copy the eagle board file to the /oomp/eagle directory 
            eagle_board_file_dst = f'{directory}/oomp/src/{key}/working.brd'
            eagle_board_file_src_c = f'{directory}/git/{eagle_board_file_src[key]}'
            #copy file using os
            import shutil
            shutil.copyfile(eagle_board_file_src_c, eagle_board_file_dst)
        
            #do the same for the schematic
            eagle_schematic_file_dst = f'{directory}/oomp/src/{key}/working.sch'
            eagle_schematic_file_src_c = f'{directory}/git/{eagle_schematic_file_src[key]}'
            #copy using os
            shutil.copyfile(eagle_schematic_file_src_c, eagle_schematic_file_dst)
        
    #copy the kicad source diretory to src/working
    ###### untested
    if kicad_src_directory:
        #copy the kicad source directory to src/working
        kicad_src_directory_dst = f'{directory}/oomp/src/working'
        kicad_src_directory_src = f'{directory}/git/{kicad_src_directory}'
        #copy all files in the source directory to the destination directory using os
        import shutil
        shutil.copytree(kicad_src_directory_src, kicad_src_directory_dst)
        #rename all the files in the destination directory to working
        #find the name of the file with the .kicad_pcb extension in the dst directory
        for file in os.listdir(kicad_src_directory_dst):
            if file.endswith('.kicad_pcb'):
                file_prefix = file.replace('.kicad_pcb', '')
        #rename every file in the dst directory with the file_prefix to working
        for file in os.listdir(kicad_src_directory_dst):
            if file.startswith(file_prefix):
                os.rename(f'{kicad_src_directory_dst}/{file}', f'{kicad_src_directory_dst}/working{file.replace(file_prefix, "")}')
        #add the eagle schematic file to the kwargs
        kwargs['kicad_directory'] = kicad_src_directory_dst

    #### if eagle sorc files convert to kicad
    if eagle_board_file_src:
        #go through each directory in {directory}oomp/src
        for dir in os.listdir(f'{directory}/oomp/src'):
            #call oomp_kicad.eagle_to_kicad with the board file
            eagle_board_file = f'{directory}/oomp/src/{dir}/working.brd'
            kicad_directory = f'{directory}/oomp/src/{dir}/working'
            #if kicad directory doesn't exist create it
            if not os.path.exists(kicad_directory):
                os.makedirs(kicad_directory)
            #check if src/dir/working/working.kicad_pcb exists if it does don't call this
            if not os.path.exists(f'{kicad_directory}/working.kicad_pcb'):
                oom_kicad.eagle_to_kicad(eagle_file=eagle_board_file,kicad_directory=kicad_directory)
            else:
                print(f'kicad file already exists for {kicad_directory}' )

    #### by this point a kicad directory should exist in src copy this to oomp directory with the version name like current
    #go through each directory in {directory}oomp/src
    for dir in os.listdir(f'{directory}/oomp/src'):
        #if there's a directory called working in dir copy it to base and dir
        if os.path.exists(f'{directory}/oomp/src/{dir}/working'):
            #copy the working directory to the base directory
            import shutil
            src = f'{directory}/oomp/src/{dir}/working'
            dst = f'{directory}/oomp/{dir}/working'
            #copy files across if a check if each file exists if it does overwrite it
            for file in os.listdir(src):
                #replace doub
                if os.path.exists(f'{dst}/{file}'):
                    os.remove(f'{dst}/{file}')
                src_file = f'{src}/{file}'
                dst_file = f'{dst}/{file}'
                #replace double slashes with single slashes
                dst_file = dst_file.replace('//', '/')
                src_file = src_file.replace('//', '/')
                #if destination directory doesn't exist create it
                if not os.path.exists(dst):
                    os.makedirs(dst)
                shutil.copyfile(src_file, dst_file)
                
            
            
    #generate all the kicad files
    oom_kicad.generate_outputs(board_file = f'{directory}/oomp/current/working/working.kicad_pcb', **kwargs)

    #generate the readme
    # copy kwargs to readme_kwargs
    kwargs["oomp_in_output"] = True
    oom_kicad.generate_readme(**kwargs)


    #dump a json file of the kwargs to /oomp directory
    import json
    with open(f'{directory}/oomp/oomp.json', 'w') as outfile:
        json.dump(kwargs, outfile)

    


def git_project(**kwargs):
    github = kwargs.get('github', None)
    directory = kwargs.get('directory', None)
    #check if the project has already been cloned into directory/git using the git library
    
    if not os.path.exists(f'{directory}/git/'):                
        #add a print to say what's happening
        print(f'Cloning {github} into {directory}/git/')
        #clone the project into directory/src/git without using git library check the output for error 443 if it is there retry upto 5 times
        import subprocess
        import time
        for i in range(5):
            try:
                subprocess.check_output(['git', 'clone', github, f'{directory}/git'])
                break
            except:
                print('Error 443, retrying in 5 seconds')
                time.sleep(5)

        
        
        #print the result
        print(f'Cloned {github} into {directory}/git')
    #if it has been cloned pull it to update it
    else:
        # print a message to say what's happening
        print('pulling not currently working')
        #pull the project into directory/git
        import subprocess
        #check for error 443 if it is there retry upto 5 times

        command_string = f'git -C {directory}/ pull'
        #run the command using os.system
        #os.system(command_string)
        #os.system(command_string)
        #os.system(command_string)
        #os.system(command_string)


    
    
    #add other git details to the kwargs

    return kwargs
    

    
