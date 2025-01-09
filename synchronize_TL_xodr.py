import xml.etree.ElementTree as ET

xodr_path = "C:\\Users\\pc\\Desktop\\20250106_temp\\example\\test_add_TLs_0108_case1.xodr"
output_xodr_path = "C:\\Users\\pc\\Desktop\\20250106_temp\\example\\test_add_TLs_0108_case1_modified.xodr"


if __name__ == "__main__":
    tree = ET.parse(xodr_path)
    root = tree.getroot()
    roads = root.findall("road")
    edit_roads = []
    for i in range(len(roads)):
        signals = roads[i].find("signals")
        if signals.text is not None:
            edit_roads.append(roads[i])

    for road in edit_roads:
        signals = road.find("signals")
        road_len = road.get("length")
        road_id = road.get("id")
        print(road_id)
        signals_elements = signals.findall("signal")
        remain_id = []
        remove_id = []
        signal_flag = 0
        for signal in signals_elements:
            if signal_flag == 0:
                remain_id.append(signal.get("id"))
            else:
                remove_id.append(signal.get("id"))
            signal_flag += 1
            signals.remove(signal)
            
        adjusted_element = ET.Element('signal', id=remain_id[0], name="Signal_3Light_Post01", s=str(float(road_len)-10), t="-4.4797897637266599e+0", zOffset="-6.9904327392578125e-1", roll="0.0000000000000000e+0", pitch="0.0000000000000000e+0", orientation="-", dynamic="yes", country="OpenDRIVE", type="1000001", subtype="-1", value="-1.0000000000000000e+0", text="", height="1.1595988571643829e+0", width="5.2492320205637566e-1")
        adjusted_element.append(ET.Element('validity', fromLane="-1", toLane="-1"))
        signals.append(adjusted_element)

        controller_id = remain_id[0].split("_")[0]
        linked_controller = root.findall(f".//controller[@id='{controller_id}']")[0]
        controllers = linked_controller.findall("control")
        for controller in controllers:
            if controller.get("signalId") in remove_id:
                linked_controller.remove(controller)

    tree.write(output_xodr_path, encoding='UTF-8', xml_declaration=True)