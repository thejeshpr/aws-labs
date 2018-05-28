import argparse
import boto3


class FooAction(argparse.Action):
	def __init__(self, option_strings, dest, nargs=None, **kwargs):
		#if nargs is not None:
		#	raise ValueError("nargs not allowed")
		super(FooAction, self).__init__(option_strings, dest, **kwargs)
	def __call__(self, parser, namespace, values, option_string=None):
		print('%r %r %r' % (namespace, values, option_string))
		#values = values.split(';')
		setattr(namespace, self.dest, values)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


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
	"""parser.add_argument('key_file_path', metavar='Key File',
									help='key file path')"""
	parser.add_argument('--create_new_key', metavar='Create New Key',
						default='true', type=str2bool,
						help='new Key will be created if not Found, default True')


	args = parser.parse_args()
	return args
	#print(args)
	#print(args.accumulate(args.integers))

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
		TagSpecifications=[
							{
								'ResourceType': 'instance',
								'Tags': tags
							}
						]
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
	#print(tags)
	#tags = [{tag.split(':')[0]:tag.split(':')[1]} for tag in args.tags]
	#print(tags)
	#for tag in args.tags:
	#	temp 
	print('Creating Instance...')
	instance = create_ec2_instance(args.image_id, args.key_name, tags, args.security_groups)
	print('Instance Created successfully, Public IP : {}'.format(instance.public_ip_address))

if __name__ == '__main__':
	main()
