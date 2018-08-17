# List all volume `gluster volume list`
# For each volume, get info: Volume Name, Type, Brick(s)
# Sort and count by Volume Type

import csv

from gluster.cli import volume

def get_vol_list():
    return volume.vollist()

def get_bricks(vol_dict):
    """
    return list of brick dicts from vol_dict
    """
    brick_key = 'bricks'
    return vol_dict.get(brick_key)

def _get_from_brick(key, brick):
    """ get brick['key']"""
    return brick.get(key, None)

def get_type(vol):
    """
    Get vol type
    """
    type_key = 'type'

    return vol.get(type_key, None) 

def get_name(vol_dict):
    """
    Get vol name
    """
    name_key = 'name'

    return vol_dict.get('name', None)

def get_num_bricks(vol_dict):
    """ easy grab for num bricks"""
    num_bricks_key = 'num_bricks'
    return vol_dict.get(num_bricks_key, None)

def create_report_list():
    """
    generate report with name, volume type, number of bricks, 
    brick (hostnames), total size of bricks, and brick free size
    will return a list of dicts with columes:
    """
    total_size_key = 'size_total'
    free_size_key = 'size_free'
    name_key = 'name'


    report_list = []
    vol_list = get_vol_list()
    for vol in vol_list:
        report_row = {
                    'name': None,
                    'vol_type': None,
                    'num_bricks': None,
                    'brick_names': None,
                    'brick_total_size': None,
                    'brick_free_size': None,
                }
        # get vol_info 
        vol_status_list = volume.status_detail(volname=vol)
        for vol_dict in vol_status_list:
            vol_num_bricks = get_num_bricks(vol_dict) 
            vol_brick_names = [ _get_from_brick(name_key, brick) for brick in get_bricks(vol_dict) ]
            vol_total_size = list({ _get_from_brick(total_size_key, brick) for brick in get_bricks(vol_dict) })
            vol_free_size = list({ _get_from_brick(free_size_key, brick) for brick in get_bricks(vol_dict) })
            vol_type = get_type(vol_dict)
            vol_name = get_name(vol_dict)

            report_row['name'] = vol_name
            report_row['vol_type'] = vol_type
            report_row['num_bricks'] = vol_num_bricks
            report_row['brick_names'] = vol_brick_names
            report_row['brick_total_size'] = vol_total_size
            report_row['brick_free_size'] = vol_free_size

        report_list.append(report_row)
    return report_list

def create_csv(report_list, csv_file='test.csv'):
    column_names = [
                    'name',
                    'vol_type',
                    'num_bricks',
                    'brick_names',
                    'brick_total_size',
                    'brick_free_size',
                ]
    with open(csv_file, 'wb') as csvfile:
        report_writer = csv.DictWriter(csvfile, fieldnames=column_names)
        report_writer.writeheader()
        for row in report_list:
            report_writer.writerow(row)


def main():
    csv_file_name = 'gluster_volume_info.csv'
    report_list = create_report_list()
    create_csv(report_list, csv_file_name)

main()




# not related to this exercise but
'''
[root@gluster1 vagrant]# gluster volume create gv0 replica 2 gluster11:/bricks/brick1/gv0 gluster2:/bricks/brick1/gv0
Replica 2 volumes are prone to split-brain. Use Arbiter or Replica 3 to avoid this. See: http://docs.gluster.org/en/latest/Administrator%20Guide/Split%20brain%20and%20ways%20to%20deal%20with%20it/.

'''
