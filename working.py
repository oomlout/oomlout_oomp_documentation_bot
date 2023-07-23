import oomp_documentation_bot as oomp_bot


def main():
    ps = []

    project_deets = {}
    project_deets['github'] = 'https://github.com/electrolama/minik'
    project_deets['eagle_board_file_src'] = 'module/Revision A2/minik-RevA2.brd'    
    #ps.append(project_deets)


    project_deets = {}
    project_deets['github'] = 'https://github.com/omerk/zig-a-zig-ah'
    project_deets['eagle_board_file_src'] = 'zzh/Revision A/zzh.brd'
    #ps.append(project_deets)


    project_deets = {}
    project_deets['github'] = 'https://github.com/oomlout/oomlout_electronics_oobb_led_matrix'
    project_deets['kicad_src_directory'] = "oomp/current/working"
    
    'module/Revision A2'
    ps.append(project_deets)


    for project_deets in ps:
        oomp_bot.document_project(**project_deets)











if __name__ == '__main__':
    main()
    
    