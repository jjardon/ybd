import yaml
import os
import sys
import hashlib

def load_defs(path, definitions):
	for dirname, dirnames, filenames in os.walk("."):
		# print path to all subdirectories first.
		for filename in filenames:
			if filename.endswith('.def'):
				definition = load_def(dirname, filename)
				if get(definition, 'name') != []:
					definitions.append(definition)
					for dependency in get(definition, 'build-depends'):
						# print 'dependency is %s' % dependency
						if get(dependency, 'repo') != []:
							dependency['hash'] = definition['hash']
							definitions.append(dependency)

					for content in get(definition, 'contents'):
						# print 'content is %s' % content
						content['hash'] = definition['hash']
						definitions.append(content)

		if '.git' in dirnames:
			dirnames.remove('.git')

#	for i in definitions:
#		print
#		print i

def load_def(path, name):
	try:
		with open(path + "/" + name) as f:
			text = f.read()

		definition = yaml.safe_load(text)
		definition['hash'] = hashlib.sha256(path + "/" + name).hexdigest()[:8]

	except:
		return None

	return definition

def get_definition(definitions, this):
	if get(this, 'contents') != [] or get(this, 'repo') != [] and get(this, 'ref') != []:
		return this

	for definition in definitions:
		if definition['name'] == this:
			return definition

		if definition['name'].split('|')[0] == this:
			return definition

	print "Oh dear, where is the definition of %s?" % get(this, 'name')
	raise SystemExit

def get(thing, value):
	val = []
	try:
		val = thing[value]
	except:
		pass
	return val

def assemble(definitions, this):
	print 'assemble %s' % get(this,'name')

def touch(pathname):
    with open(pathname, 'w'):
        pass

def cache_key(definitions, this):
	definition = get_definition(definitions, this)
	# print 'cache_key %s' % definition
	return path + "/cache/" + definition['name'] + "|" + definition['hash'] + ".cache"


def cache(definitions, this):
	# print 'cache %s' % this
	touch(cache_key(definitions, this))

def is_cached(definitions, this):
	if os.path.exists(cache_key(definitions, this)):
		return True

	return False

	for cache in maybe_caches(this):
		ref = get_ref(cache)
		diff = git_diff(DTR, ref)
		if diff:
			for dependency in this['build-depends']:
				return

def build(definitions, target):
	print 'build %s' % target
	if is_cached(definitions, target):
		print '%s is cached' % target
		return

	this = get_definition(definitions, target)

	for dependency in get(this, 'build-depends'):
		build(definitions, dependency)

	# wait here for all the dependencies to complete 
	# how do we know when that happens?

	for content in get(this, 'contents'):
		build(definitions, content)

	assemble(definitions, this)
	cache(definitions, this)

definitions = []
path, target = os.path.split(sys.argv[1])
load_defs(path, definitions)
target = target.replace('.def', '')
build(definitions, target)
