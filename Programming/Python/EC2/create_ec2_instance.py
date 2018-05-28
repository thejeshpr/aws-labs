import argparse
import boto3

def process_args():
	""" Process command line arguments """
	parser = argparse.ArgumentParser(
		prog='CreateEC2Instance',
		description='Create EC2 instance'
	)
	parser.add_argument('image_id', metavar='ImageID',
						help='Image ID for Instance')	
	parser.add_argument('--tags', nargs='*',
						help="tags : key:value key:value")
	parser.add_argument('--security_groups', nargs='*',
						help="list of Security Groups : Security-Group1 Security-Group2")
	parser.add_argument('key_name', metavar='Key Name',
						help='key name to login')

	args = parser.parse_args()
	return args


def create_ec2_instance(image_id, key_name, tags, security_grp_ids):
	ec2 = boto3.resource('ec2')
	InstanceType = 't2.micro'

	instance = ec2.create_instances(
		ImageId=image_id,
		KeyName=key_name,
		MinCount=1,
		MaxCount=1,
		InstanceType='t2.micro',
		SecurityGroupIds=security_grp_ids,
		TagSpecifications=[{'ResourceType': 'instance','Tags': tags}]
	)[0]

	print('Waiting For instance to complete the installation....')
	instance.wait_until_running()
	instance.load()
	return instance


def main():
	args = process_args()	
	tags = []
	for tag in args.tags:
		key, value = tag.split(':')
		tags.append({"Key" : key, "Value":value})	
	print('Creating Instance...')
	instance = create_ec2_instance(args.image_id, args.key_name, tags, args.security_groups)
	print('Instance Created successfully, Public IP : {}'.format(instance.public_ip_address))

if __name__ == '__main__':
	main()
