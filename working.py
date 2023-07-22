import oomp_documentation_bot as oomp_bot


def main():
    ps = []

    project_deets = {}
    project_deets['github'] = 'https://github.com/electrolama/minik'
    project_deets['eagle_board_file_src'] = {}
    project_deets['eagle_board_file_src']['current'] = 'module/Revision A2/minik-RevA2.brd'
    project_deets['eagle_schematic_file_src'] = {}
    project_deets['eagle_schematic_file_src']['current'] = 'module/Revision A2/minik-RevA2.sch'
    #set the kicad src directory
    #project_deets['kicad_src_directory'] = 'module/Revision A2'
    ps.append(project_deets)




    project_deets = {}
    project_deets['github'] = 'https://github.com/omerk/zig-a-zig-ah'
    project_deets['eagle_board_file_src'] = {}
    project_deets['eagle_board_file_src']['current'] = 'zzh/Revision A/zzh.brd'
    project_deets['eagle_schematic_file_src'] = {}
    project_deets['eagle_schematic_file_src']['current'] = 'zzh/Revision A/zzh.sch'
    #set the kicad src directory
    #project_deets['kicad_src_directory'] = {}
    #project_deets['kicad_src_directory']["current"] = "oomp/current/working"
    
    'module/Revision A2'
    ps.append(project_deets)




    for project_deets in ps:
        oomp_bot.document_project(**project_deets)











if __name__ == '__main__':
    main()
    