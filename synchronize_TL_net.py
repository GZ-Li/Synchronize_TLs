import xml.etree.ElementTree as ET

net_path = "C:\\Users\\pc\\Desktop\\20250106_temp\\example\\net\\test_add_TLs_0108_case1.net.xml"
output_opendrive = "C:\\Users\\pc\\Desktop\\20250106_temp\\example\\net\\test_add_TLs_0108_case1_modified.net.xml"
target_coor = ['1131.7', '678.29']


def get_junction_2_coor(root):
    all_junctions = root.findall("junction")
    junction_2_coor = {}
    for junc in all_junctions:
        if junc.get("type") == "priority":
            junction_2_coor[junc.get("id").strip(":")] = [junc.get("x"), junc.get("y")]
    return junction_2_coor
    
    
def get_nearest_junction(target_coor, junction_2_coor): # target_coor = ['x', 'y'], junction_2_coor = {junction_id: junction_coordinate}  
    min_dist = 1000000
    min_junc = ""
    for junc_id, junc_coor in junction_2_coor.items():
        dist = (float(target_coor[0]) - float(junc_coor[0])) * (float(target_coor[0]) - float(junc_coor[0])) + (float(target_coor[1]) - float(junc_coor[1])) * (float(target_coor[1]) - float(junc_coor[1]))
        if dist < min_dist:
            min_dist = dist
            min_junc = junc_id
    return min_junc, min_dist


def generate_phases(inclanes_times):
    state_1 = ""
    state_2 = ""
    state_3 = ""
    state_4 = ""
    state_flag = 1
    for inclane_id, times in inclanes_times.items():
        if state_flag % 2 == 1:
            state_1 += 'r' * times
        else:
            state_1 += 'g' * times
        state_flag += 1
    state_flag = 1
    for inclane_id, times in inclanes_times.items():
        if state_flag % 2 == 1:
            state_2 += 'r' * times
        else:
            state_2 += 'y' * times
        state_flag += 1
    state_flag = 1
    for inclane_id, times in inclanes_times.items():
        if state_flag % 2 == 1:
            state_3 += 'g' * times
        else:
            state_3 += 'r' * times
        state_flag += 1
    state_flag = 1
    for inclane_id, times in inclanes_times.items():
        if state_flag % 2 == 1:
            state_4 += 'y' * times
        else:
            state_4 += 'r' * times
        state_flag += 1 
    phases = [
    {'duration': '40', 'state': state_1},
    {'duration': '5',  'state': state_2},
    {'duration': '40', 'state': state_3},
    {'duration': '5',  'state': state_4}
    ]
    return phases


def main(net_path, output_opendrive, target_coor):
    
    tree = ET.parse(net_path)
    root = tree.getroot()
    junction_2_coor = get_junction_2_coor(root)
    junc_id, min_dist = get_nearest_junction(target_coor, junction_2_coor)
    
    junction = root.find(f".//junction[@id='{junc_id}']")
    if junction is None:
        print("Wrong Junction")
    else:
        junction.set("type", "traffic_light")
        inclanes = junction.get("incLanes").split(" ")
        inclanes_ = []
        for inclane in inclanes:
            inclane_ = inclane.split("_")[0]
            if inclane_ not in inclanes_:
                inclanes_.append(inclane_)
        inclanes = inclanes_
        inclanes_times = {}
        for inclane in inclanes:
            inclanes_times[inclane] = 0
        inclane_total = 0
        for inclane in inclanes:
            connections = root.findall(f".//connection[@from='{inclane}']")
            for connection in connections:
                connection.set("tl", junc_id)
                connection.set("linkIndex", str(inclane_total))
                inclane_total += 1
                inclanes_times[inclane] += 1
                
        phases = generate_phases(inclanes_times)
        tl_logic = ET.Element('tlLogic', id=junc_id, type='static', programID='0', offset='0')
        for phase_data in phases:
            phase = ET.Element('phase', duration=phase_data['duration'], state=phase_data['state'])
            tl_logic.append(phase)
        edges_num = len(root.findall(".//edge"))
        root.insert(edges_num+2, tl_logic)
        
        tree.write(output_opendrive, encoding='UTF-8', xml_declaration=True)
        
        

if __name__ == '__main__':
    main(net_path, output_opendrive, target_coor)




# if __name__ == '__main__':
#     # junc_id, min_dist = main(net_path)
#     # print(junc_id, min_dist)
#     tree = ET.parse(net_path)
#     root = tree.getroot()
#     junc_id = "7221412148"
#     print(root)
    
    
#     junction = root.find(f".//junction[@id='{junc_id}']")
#     if junction is None:
#         print("Wrong Junction")
#     else:
#         junction.set("type", "traffic_light")
#         inclanes = junction.get("incLanes").split(" ")
#         inclanes_ = []
#         for inclane in inclanes:
#             inclane_ = inclane.split("_")[0]
#             if inclane_ not in inclanes_:
#                 inclanes_.append(inclane_)
#         inclanes = inclanes_
#         inclanes_times = {}
#         for inclane in inclanes:
#             inclanes_times[inclane] = 0
#         inclane_total = 0
#         for inclane in inclanes:
#             connections = root.findall(f".//connection[@from='{inclane}']")
#             for connection in connections:
#                 connection.set("tl", junc_id)
#                 connection.set("linkIndex", str(inclane_total))
#                 inclane_total += 1
#                 inclanes_times[inclane] += 1
                
    
#     state_1 = ""
#     state_2 = ""
#     state_3 = ""
#     state_4 = ""
#     state_flag = 1
#     for inclane_id, times in inclanes_times.items():
#         if state_flag % 2 == 1:
#             state_1 += 'r' * times
#         else:
#             state_1 += 'g' * times
#         state_flag += 1
#     state_flag = 1
#     for inclane_id, times in inclanes_times.items():
#         if state_flag % 2 == 1:
#             state_2 += 'r' * times
#         else:
#             state_2 += 'y' * times
#         state_flag += 1
#     state_flag = 1
#     for inclane_id, times in inclanes_times.items():
#         if state_flag % 2 == 1:
#             state_3 += 'g' * times
#         else:
#             state_3 += 'r' * times
#         state_flag += 1
#     state_flag = 1
#     for inclane_id, times in inclanes_times.items():
#         if state_flag % 2 == 1:
#             state_4 += 'y' * times
#         else:
#             state_4 += 'r' * times
#         state_flag += 1
        
#     phases = [
#     {'duration': '40', 'state': state_1},
#     {'duration': '5',  'state': state_2},
#     {'duration': '40', 'state': state_3},
#     {'duration': '5',  'state': state_4}
# ]
#     tl_logic = ET.Element('tlLogic', id=junc_id, type='static', programID='0', offset='0')
#     for phase_data in phases:
#         phase = ET.Element('phase', duration=phase_data['duration'], state=phase_data['state'])
#         tl_logic.append(phase)
    
#     edges_num = len(root.findall(".//edge"))
#     root.insert(edges_num+2, tl_logic)

        
#     tree.write('traffic_modified.net.xml', encoding='UTF-8', xml_declaration=True)