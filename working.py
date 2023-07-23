import oomp_documentation_bot as oomp_bot


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
    import yaml
    with open('projects_generated.yaml', 'w') as f:
        yaml.dump(ps, f, default_flow_style=False)


def from_yaml():
    import yaml
    ps = []
    with open('projects.yaml', 'r') as f:
        ps += yaml.load(f, Loader=yaml.FullLoader)

    
    with open('projects_generated.yaml', 'r') as f:
        ps += yaml.load(f, Loader=yaml.FullLoader)
    #add prijects.yaml to ps
    

    for project_deets in ps:
        oomp_bot.document_project(**project_deets)











if __name__ == '__main__':
    dump_to_yaml()
    from_yaml()
    
