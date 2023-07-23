import oom_kicad

import os

def document_project(**kwargs):


    #make a deep copy of the original kwargs
    kwargs_config = kwargs.copy()


    github = kwargs.get('github', None)
    #get the eagle board file from the kwargs
    eagle_board_file_src = kwargs.get('eagle_board_file_src', None)
    #get the eagle schematic file from the kwargs
    eagle_schematic_file_src = kwargs.get('eagle_schematic_file_src', None)
    #get the kicas src directory from the kwargs
    #if no eagle board file then kicad_src_directory is the kicad source directory
    if not eagle_board_file_src:
        kicad_src_directory = kwargs.get('kicad_src_directory', "oomp/current/working")
        #update kwargs
        kwargs['kicad_src_directory'] = kicad_src_directory
    else:
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





    ######
    ###### directory section
    ######

    #create a /oomp directory in the project directory
    if not os.path.exists(f'{directory}/oomp'):
        os.makedirs(f'{directory}/oomp')
    #if oomp_documentation/src doesn't exist create it
    if not os.path.exists(f'{directory}/oomp_documentation/src'):
        os.makedirs(f'{directory}/oomp_documentation/src')

    #######
    ####### git section
    #######

    #do git clone or pull    
    kwargs = git_project(**kwargs)

    #######
    ####### eagle conversion section
    #######

    if eagle_board_file_src:
        #if eagle board sile is a string convert it to a dict with the string value as version_current
        if isinstance(eagle_board_file_src, str):
            eagle_board_file_src = {'version_current': eagle_board_file_src}
            kwargs['eagle_board_file_src'] = eagle_board_file_src
        for key in eagle_board_file_src:
            #make the directory with key
            if not os.path.exists(f'{directory}/oomp_documentation/src/{key}'):
                os.makedirs(f'{directory}/oomp_documentation/src/{key}')
            #copy the eagle board file to the /oomp_documentation/eagle directory 
            eagle_board_file_dst = f'{directory}/oomp_documentation/src/{key}/working.brd'
            eagle_board_file_src_c = f'{directory}/git/{eagle_board_file_src[key]}'
            #copy file using os
            import shutil
            shutil.copyfile(eagle_board_file_src_c, eagle_board_file_dst)
        
            #if eagle_board_file_source isnt defined get it from board source just chage suffix to .sch
            if not eagle_schematic_file_src:
                eagle_schematic_file_src = {}
                eagle_schematic_file_src[key] = eagle_board_file_src[key].replace('.brd', '.sch')
                #add it back to kwargs
                kwargs['eagle_schematic_file_src'] = {}
                kwargs['eagle_schematic_file_src'][key] = eagle_schematic_file_src

            #do the same for the schematic
            eagle_schematic_file_dst = f'{directory}/oomp_documentation/src/{key}/working.sch'
            eagle_schematic_file_src_c = f'{directory}/git/{eagle_schematic_file_src[key]}'
            #copy using os
            shutil.copyfile(eagle_schematic_file_src_c, eagle_schematic_file_dst)
            


    #### if eagle sorc files convert to kicad
    if eagle_board_file_src:
        #go through each directory in {directory}oomp_documentation/src
        for dir in os.listdir(f'{directory}/oomp_documentation/src'):
            #call oomp_kicad.eagle_to_kicad with the board file
            eagle_board_file = f'{directory}/oomp_documentation/src/{dir}/working.brd'
            kicad_directory = f'{directory}/oomp_documentation/src/{dir}/working'
            #if kicad directory doesn't exist create it
            if not os.path.exists(kicad_directory):
                os.makedirs(kicad_directory)
            #check if src/dir/working/working.kicad_pcb exists if it does don't call this
            if not os.path.exists(f'{kicad_directory}/working.kicad_pcb'):
                oom_kicad.eagle_to_kicad(eagle_file=eagle_board_file,kicad_directory=kicad_directory)
            else:
                print(f'kicad file already exists for {kicad_directory}' )


    #######
    ####### kicad copy section
    #######

    #copy the kicad source diretory to src/working
    ###### untested
    if kicad_src_directory:
        #if kicad_src_directory is a string convert it to a dict with the string value as version_current
        if isinstance(kicad_src_directory, str):
            kicad_src_directory = {'version_current': kicad_src_directory}
            kwargs['kicad_src_directory'] = kicad_src_directory
        for dir in kicad_src_directory:
            import shutil
            #copy the kicad source directory to src/working
            kicad_src_directory_dst = f'{directory}/oomp_documentation/src/{dir}/working/'
            kicad_src_directory_src = f'{directory}/git/{kicad_src_directory[dir]}'
            #remove double slashes
            kicad_src_directory_dst = kicad_src_directory_dst.replace('//', '/')
            kicad_src_directory_src = kicad_src_directory_src.replace('//', '/')
            #go through each file and copy all kicad_pcb and kicad_sch files if the file already exists delete it first
            #make dst if it doesn't exist
            if not os.path.exists(kicad_src_directory_dst):
                os.makedirs(kicad_src_directory_dst)

            for file in os.listdir(kicad_src_directory_src):
                #if the file is a kicad_pcb or kicad_sch file copy it
                if file.endswith('.kicad_pcb') or file.endswith('.kicad_sch') or file.endswith('.sch') or file.endswith('.pcb'):
                    #replace.sch with kicad_sch and .pcb with kicad_pcb
                    file_out = file.replace('.sch', '.kicad_sch')
                    file_out = file_out.replace('.pcb', '.kicad_pcb')
                    #delete the file if it exists
                    if os.path.exists(f'{kicad_src_directory_dst}/{file}'):
                        os.remove(f'{kicad_src_directory_dst}/{file_out}')
                    #copy the file
                    shutil.copyfile(f'{kicad_src_directory_src}/{file}', f'{kicad_src_directory_dst}/{file_out}')


            
            #rename all the files in the destination directory to working
            #find the name of the file with the .kicad_pcb extension in the dst directory
            for file in os.listdir(kicad_src_directory_dst):
                if file.endswith('.kicad_pcb'):
                    file_prefix = file.replace('.kicad_pcb', '')
            #rename every file in the dst directory with the file_prefix to working
            for file in os.listdir(kicad_src_directory_dst):
                if file.startswith(file_prefix):
                    src_file = f'{kicad_src_directory_dst}/{file}'
                    src_removed = kicad_src_directory_dst.replace("src/", "")
                    
                    
            #add the eagle schematic file to the kwargs
            kwargs['kicad_directory'] = kicad_src_directory_dst

    
    #######
    ####### move from src to oomp section
    #######

    #### by this point a kicad directory should exist in src copy this to oomp directory with the version name like version_current
    #go through each directory in {directory}oomp_documentation/src
    for dir in os.listdir(f'{directory}/oomp_documentation/src'):
        #if there's a directory called working in dir copy it to base and dir
        if os.path.exists(f'{directory}/oomp_documentation/src/{dir}/working'):
            #copy the working directory to the base directory
            import shutil
            src = f'{directory}/oomp_documentation/src/{dir}/working'
            dst = f'{directory}/oomp_documentation/{dir}/working'
            #remove double slashes
            src = src.replace('//', '/')
            dst = dst.replace('//', '/')
            #make dst if it doesn't exist
            if not os.path.exists(dst):
                os.makedirs(dst)
            #copy files across if a check if each file exists if it does overwrite it
            #if working.kicad_pcb or working.kicad_sch exist delete them
            if os.path.exists(f'{dst}/working.kicad_pcb'):
                os.remove(f'{dst}/working.kicad_pcb')
            if os.path.exists(f'{dst}/working.kicad_sch'):
                os.remove(f'{dst}/working.kicad_sch')
            for file in os.listdir(src):
                #copy files from src to dst folder if they exist overwrite
                if f'{src}/{file}' != f'{dst}{file}':
                    if os.path.exists(f'{dst}/{file}'):
                        os.remove(f'{dst}/{file}')
                
                shutil.copyfile(f'{src}/{file}', f'{dst}/{file}')
            
            #count the number of files with the kicad_pcb extension in the dst directory
            kicad_pcb_count = 0
            for file in os.listdir(dst):
                if file.endswith('.kicad_pcb'):
                    kicad_pcb_count += 1
            #if there is only one kicad_pcb file in the dst directory rename it to working.kicad_pcb
            if kicad_pcb_count == 1:
                for file in os.listdir(dst):
                    if file.endswith('.kicad_pcb'):
                        dst_file = f'{dst}/working.kicad_pcb'
                        #if dst_file exists delete it
                        if f'{dst}/{file}' != dst_file:
                            if os.path.exists(dst_file):
                                os.remove(dst_file)
                        os.rename(f'{dst}/{file}', dst_file)
            else:
                raise Exception(f'Error: {kicad_pcb_count} kicad_pcb files in {dst} directory')
            #do the same for kicad_sch files
            kicad_sch_count = 0
            for file in os.listdir(dst):
                if file.endswith('.kicad_sch'):
                    kicad_sch_count += 1
            #if there is only one kicad_sch file in the dst directory rename it to working.kicad_sch
            if kicad_sch_count == 1:
                for file in os.listdir(dst):
                    if file.endswith('.kicad_sch') or file.endswith('.sch'):
                        os.rename(f'{dst}/{file}', f'{dst}/working.kicad_sch')
            else:
                raise Exception(f'Error: {kicad_sch_count} kicad_sch files in {dst} directory')
            
                
                
                
    ######
    ###### generate kicad file section
    ######
            
    #generate all the kicad files
    oom_kicad.generate_outputs(board_file = f'{directory}/oomp_documentation/version_current/working/working.kicad_pcb', **kwargs)

    ######
    ###### generate readme section
    ######

    #generate the readme
    # copy kwargs to readme_kwargs
    kwargs["oomp_in_output"] = True
    oom_kicad.generate_readme(**kwargs)


    ######
    ###### generate json section
    ######

    #dump a json file of the kwargs to /oomp directory
    import json
    with open(f'{directory}/oomp_documentation/oomp.json', 'w') as outfile:
        json.dump(kwargs, outfile)
    #dump a yaml file of the kwargs to /oomp directory
    import yaml        
    with open(f'{directory}/oomp_documentation/oomp.yaml', 'w') as outfile:
        yaml.dump(kwargs, outfile)

    #dump a oomp_config json and yaml file to /oomp directory
    with open(f'{directory}/oomp_documentation/oomp_config.json', 'w') as outfile:
        json.dump(kwargs_config, outfile)
    #dump a yaml file of the kwargs to /oomp directory
    with open(f'{directory}/oomp_documentation/oomp_config.yaml', 'w') as outfile:
        yaml.dump(kwargs_config, outfile)
    


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
    

    
