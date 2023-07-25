import oomp_documentation_bot as oomp_bot
import yaml

github_users = ["solderparty", "sparkfun","adafruit","omerk","electrolama","sparkfunx","DangerousPrototypes","oomlout"]

#github_users = ["solderparty"]

def dump_to_yaml():
    ps = []

    project_deets = {}
    project_deets['github'] = 'https://github.com/electrolama/minik'
    project_deets['eagle_board_file_src'] = 'module/Revision A2/minik-RevA2.brd'    
    ps.append(project_deets)


    project_deets = {}
    project_deets['github'] = 'https://github.com/omerk/zig-a-zig-ah'
    project_deets['eagle_board_file_src'] = 'zzh/Revision A/zzh.brd'
    ps.append(project_deets)


    project_deets = {}
    project_deets['github'] = 'https://github.com/oomlout/oomlout_electronics_oobb_led_matrix'    
    'module/Revision A2'
    ps.append(project_deets)


    
    #dump ps to yaml

    with open('projects_generated.yaml', 'w') as f:
        yaml.dump(ps, f, default_flow_style=False)



def generate_repo_yaml():

    
    for user in github_users:
        #only make if the generated yaml doesn't already exist
        import os
        if not os.path.exists(f'projects_generated_{user}.yaml'):
        
            #check if tmp/repos_{user}.yaml exists
            import os
            if os.path.exists(f'tmp/repos_{user}.yaml'):
                #load repos from yaml tmp/repos_{user}.yaml
                import yaml
                with open(f'tmp/repos_{user}.yaml', 'r') as ff:
                    repos = yaml.load(ff, Loader=yaml.FullLoader)
            else:
                repos = get_repos(user)
                #dump repos to yaml tmp/repos_{user}.yaml
                with open(f'tmp/repos_{user}.yaml', 'w') as ff:
                    import yaml
                    yaml.dump(repos, ff, default_flow_style=False)
            with open(f'projects_generated_{user}.yaml', 'w') as f:
                    #write '' to the file
                    f.write('')
            for repo in repos:
                #download repo to tmp/git_harvest
                #delete files in tmp/git_harvest using shutil
                import os
                import shutil
                #make a new git_harvest_index folder make the index unique            


                os.system(f'git clone {repo["clone_url"]} tmp/git_harvest/{repo["full_name"]}')
                #get eagle board file
                #empty the repo file fresh
                
                import glob
                try:
                    #find a file with type brd using a loop and set eagle_board_file_src don't use glob
                    eagle_board_file_src = ''
                    for file in glob.glob(f'tmp/git_harvest/{repo["full_name"]}/**/*', recursive=True):
                        if file.endswith('.brd'):
                            eagle_board_file_src = file
                            #replace  \\ with /
                            eagle_board_file_src = eagle_board_file_src.replace('\\', '/')
                            eagle_board_file_src = eagle_board_file_src.replace(f'tmp/git_harvest/{repo["full_name"]}/', '')
                            break
                        #check for kicad files
                        if file.endswith('.kicad_pcb'):

                            #kicad_src_directory equals the files directory
                            kicad_src_directory = file.replace('\\', '/')
                            kicad_src_directory = kicad_src_directory.replace(f'tmp/git_harvest/{repo["full_name"]}/', '')
                            #replace the filename and extension with ""
                            kicad_src_directory = kicad_src_directory.replace(kicad_src_directory.split('/')[-1], '')
                            if kicad_src_directory == '':
                                kicad_src_directory = '&&**'
                            pass



                    #print eagle_board_file_src
                    #if isn't empty
                    if eagle_board_file_src != '':                    
                        deets = {}
                        deets['github'] = repo['html_url'].replace(".github","")
                        deets['eagle_board_file_src'] = eagle_board_file_src
                        with open(f'projects_generated_{user}.yaml', 'a') as f:
                            yaml.dump(deets, f, default_flow_style=False)
                        #print adding to yaml
                        print(f'adding {repo["name"]} to yaml')
                    elif kicad_src_directory != '':
                        deets = {}
                        deets['github'] = repo['html_url'].replace(".github","")
                        if kicad_src_directory == '&&**':
                            kicad_src_directory = ''
                        deets['kicad_src_directory'] = kicad_src_directory
                        with open(f'projects_generated_{user}.yaml', 'a') as f:
                            yaml.dump(deets, f, default_flow_style=False)
                        #print adding to yaml
                        print(f'adding {repo["name"]} to yaml')

                except:
                    #write to log the repo name and no board found
                    with open('log.txt', 'a') as ff:
                        ff.write(f'{repo["name"]} no board found\n')


def get_repos(user):
    #print the user finding for
    print(f'finding repos for {user}')
    #get a list of repos for user from github add pauses to not get rate limited
    import requests
    import json
    import time    
    repos = []
    page = 1
    while True:
    #while page < 2:
        r = requests.get(f'https://api.github.com/users/{user}/repos?page={page}&per_page=100')
        if r.status_code == 200:
            repos += json.loads(r.text)
            #print how many repos found
            print(f'{len(repos)} repos found', end='\r')
            #prin
            page += 1
            #add a dot to show progress
            print('.', end='', flush=True)
            time.sleep(6)
            if json.loads(r.text) == []:
                break
        else:
            #print the error code with a message saying its fetching repo error
            print(f'error fetching repos {r.status_code}')
            
    print()
    return repos
        

def from_yaml():
    import yaml
    ps = []
    
    
    #load in all the generated yaml for github_users
    for user in github_users:
        with open(f'projects_generated_{user}.yaml', 'r') as f:
            ps += yaml.load(f, Loader=yaml.FullLoader)

    with open('projects.yaml', 'r') as f:
        pass
        #ps += yaml.load(f, Loader=yaml.FullLoader)

    
    with open('projects_generated.yaml', 'r') as f:
        #ps += yaml.load(f, Loader=yaml.FullLoader)
        pass
    #add prijects.yafbC:\GH\oomlout_oomp_documentation_bot\projects\solderparty\keyboard_featherwing_hw\oomp_documentation\version_current\working\working_bom.csvml to ps







    for project_deets in ps:
        #oomp_bot.document_project(**project_deets)
        try:
            oomp_bot.document_project(**project_deets)        
            pass
        except Exception as e:
            #log project deets and exception to a log file
            with open('log.txt', 'a') as f:
                f.write(str(project_deets) + '\n')
                f.write(str(e) + '\n\n\n')

    












if __name__ == '__main__':
    generate_repo_yaml()
    dump_to_yaml()
    from_yaml()
    
