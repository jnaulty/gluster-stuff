pem_file="/home/jnaulty/test/glusterfs/.vagrant/machines/gluster1/libvirt/private_key"
file="/home/jnaulty/workspace/gluster-vol-list/gluster-list-vols.py"
csv_file="/home/vagrant/gluster_volume_info.csv"
vagrant_host=vagrant@192.168.121.140

get_ssh() {
  vagrant ssh-config
}

send_file() {
scp -i $pem_file $file  ${vagrant_host}:~/
}

receive_csv() {
  scp -i $pem_file ${vagrant_host}:${csv_file} .
}

